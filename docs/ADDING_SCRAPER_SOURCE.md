# 🕷️ Guía: Añadir una Fuente al Scraper

Esta guía explica cómo crear un nuevo adaptador para el scraper de DramaApp.

---

## Arquitectura del Scraper

```
Engine → Registry → Adaptador (uno por fuente)
                         ↓
                   BeautifulSoup / httpx
                         ↓
                   Pydantic Models
                         ↓
                   Exporter (JSON / API)
```

Cada fuente tiene su **propio adaptador independiente**. Un adaptador es una clase Python que hereda de `BaseAdapter` e implementa dos métodos:

1. `discover_series()` → Lista de series descubiertas
2. `discover_episodes(series_url)` → Lista de episodios de una serie

---

## Paso 1: Crear el Adaptador

Crea un nuevo archivo en `scraper/src/adapters/`:

```python
# scraper/src/adapters/mi_fuente_adapter.py

from datetime import datetime, timezone
from bs4 import BeautifulSoup

from src.adapters.base import BaseAdapter
from src.models.series import DiscoveredSeries
from src.models.episode import DiscoveredEpisode


class MiFuenteAdapter(BaseAdapter):
    """Adaptador para MiFuente.com — catálogo público de dramas."""

    ADAPTER_TYPE = "mi_fuente"

    async def discover_series(self) -> list[DiscoveredSeries]:
        """Descubrir series desde el catálogo público."""
        # 1. Obtener HTML de la página del catálogo
        html = await self.fetch_html(f"{self.source.base_url}/catalogo")

        # 2. Parsear con BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        series_list = []

        for card in soup.select(".serie-card"):
            title = card.select_one(".title").get_text(strip=True)
            url = card.select_one("a")["href"]
            poster = card.select_one("img")["src"] if card.select_one("img") else None
            synopsis = card.select_one(".synopsis")
            genres_el = card.select(".genre-tag")

            series_list.append(DiscoveredSeries(
                source_id=self.source.id,
                source_url=url,
                title=title,
                synopsis=synopsis.get_text(strip=True) if synopsis else None,
                genres=[g.get_text(strip=True) for g in genres_el],
                language="es",
                poster_url=poster,
                extracted_at=datetime.now(timezone.utc),
            ))

        return series_list

    async def discover_episodes(self, series_url: str) -> list[DiscoveredEpisode]:
        """Descubrir episodios de una serie específica."""
        html = await self.fetch_html(series_url)
        soup = BeautifulSoup(html, "lxml")
        episodes = []

        for ep in soup.select(".episode-item"):
            ep_num = int(ep.get("data-episode", 0))
            title = ep.select_one(".ep-title").get_text(strip=True)
            duration_text = ep.select_one(".duration")

            episodes.append(DiscoveredEpisode(
                series_source_url=series_url,
                season_number=1,
                episode_number=ep_num,
                title=title,
                duration_seconds=self._parse_duration(duration_text.get_text()) if duration_text else None,
                thumbnail_url=ep.select_one("img")["src"] if ep.select_one("img") else None,
            ))

        return episodes

    @staticmethod
    def _parse_duration(text: str) -> int:
        """Convertir '12:34' a segundos."""
        parts = text.strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        return 0
```

---

## Paso 2: Registrar el Adaptador

Edita `scraper/src/adapters/registry.py`:

```python
from src.adapters.mi_fuente_adapter import MiFuenteAdapter

# En el dict de _adapters:
_adapters: dict[str, type[BaseAdapter]] = {
    "demo": DemoAdapter,
    "mi_fuente": MiFuenteAdapter,  # ← Añadir aquí
}
```

---

## Paso 3: Configurar la Fuente

Añade el dominio a la lista permitida en `.env`:

```env
SCRAPER_ALLOWED_DOMAINS=demo.dramaapp.local,mifuente.com
```

Luego crea la fuente desde el panel admin o la API:

```bash
curl -X POST http://localhost:8080/api/admin/sources \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Fuente",
    "baseUrl": "https://mifuente.com",
    "adapterType": "mi_fuente",
    "enabled": true
  }'
```

---

## Paso 4: Escribir Tests

Crea fixtures HTML y tests:

```python
# scraper/tests/test_mi_fuente.py

import pytest
from pathlib import Path
from unittest.mock import AsyncMock

from src.adapters.mi_fuente_adapter import MiFuenteAdapter
from src.models.source import SourceConfig


@pytest.fixture
def fixture_html():
    return Path("tests/fixtures/mi_fuente_catalog.html").read_text()


@pytest.fixture
def adapter():
    source = SourceConfig(
        id="test_mi_fuente",
        name="Test MiFuente",
        base_url="https://mifuente.com",
        adapter_type="mi_fuente",
    )
    mock_client = AsyncMock()
    return MiFuenteAdapter(source=source, http_client=mock_client)


@pytest.mark.asyncio
async def test_discover_series(adapter, fixture_html):
    adapter.fetch_html = AsyncMock(return_value=fixture_html)
    series = await adapter.discover_series()
    assert len(series) > 0
    assert all(s.source_id == "test_mi_fuente" for s in series)


@pytest.mark.asyncio
async def test_discover_episodes(adapter):
    fixture = Path("tests/fixtures/mi_fuente_series.html").read_text()
    adapter.fetch_html = AsyncMock(return_value=fixture)
    episodes = await adapter.discover_episodes("https://mifuente.com/series/1")
    assert len(episodes) > 0
    assert all(e.episode_number >= 1 for e in episodes)
```

---

## Checklist para Nuevos Adaptadores

- [ ] Hereda de `BaseAdapter`
- [ ] Define `ADAPTER_TYPE` como constante
- [ ] Implementa `discover_series()` y `discover_episodes()`
- [ ] Usa `self.fetch_html()` (que valida dominio y respeta rate limits)
- [ ] Devuelve modelos Pydantic validados
- [ ] Registrado en `registry.py`
- [ ] Dominio añadido a `SCRAPER_ALLOWED_DOMAINS`
- [ ] Tests con fixtures HTML locales (sin HTTP real)
- [ ] Manejo de errores (HTML inesperado, campos faltantes)
- [ ] Respetar robots.txt y condiciones de la fuente
- [ ] No eludir autenticación, CAPTCHA o anti-bot

---

## Reglas Importantes

1. **Solo fuentes públicas autorizadas** — Respeta siempre los ToS de cada sitio
2. **No scraping masivo** — Usa rate limiting y respeta robots.txt
3. **No descarga de contenido** — Solo metadatos (títulos, sinopsis, géneros)
4. **Fixtures para tests** — Nunca hagas HTTP real en tests
5. **Un adaptador = una fuente** — Mantén la separación
