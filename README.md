# 🎬 DramaApp — Plataforma de Short Dramas en Español

Plataforma web de microdramas verticales en español. Descubre, reproduce y gestiona series cortas de romance, traición, suspenso, venganza y drama familiar.

![Vue 3](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vue.js)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.4-6DB33F?logo=springboot)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248?logo=mongodb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![Tailwind](https://img.shields.io/badge/Tailwind-3.x-06B6D4?logo=tailwindcss)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Inicio Rápido](#-inicio-rápido)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Desarrollo Local](#-desarrollo-local)
- [API REST](#-api-rest)
- [Panel Administrativo](#-panel-administrativo)
- [Scraper](#-scraper)
- [Gestión de Derechos](#-gestión-de-derechos)
- [SEO](#-seo)
- [Monetización](#-monetización)
- [Pruebas](#-pruebas)
- [Despliegue](#-despliegue)
- [Guías Adicionales](#-guías-adicionales)
- [Limitaciones y Pendientes](#-limitaciones-y-pendientes)

---

## ✨ Características

### Público
- 🎥 **Reproductor vertical 9:16** optimizado para móviles
- 📱 **Diseño mobile-first** con tema cinematográfico oscuro
- 🔍 **Búsqueda en tiempo real** con debounce
- 🏷️ **Filtros** por género, idioma y orden
- ❤️ **Favoritos e historial** en localStorage
- ▶️ **Continuar viendo** con recuperación de progreso
- 🔗 **SEO completo**: meta tags, Open Graph, sitemap XML, datos estructurados
- 🍪 **Consentimiento de cookies** integrado
- 📄 **Páginas legales** (Privacidad, Términos, Cookies)

### Administración
- 📊 **Dashboard** con métricas y accesos rápidos
- 🕷️ **Gestión de scrapers** y fuentes de datos
- 📋 **Catálogo descubierto** con importación selectiva
- ⚖️ **Auditoría de derechos** con flujo de aprobación/rechazo
- 🎬 **CRUD completo** de series y episodios
- 📹 **Gestión de videos** y sesiones de subida
- 🚫 **Reclamaciones DMCA/Takedown**
- 📈 **Analítica** de tráfico y popularidad

### Técnico
- 🔐 **JWT + Spring Security** con roles ADMIN/EDITOR
- 🛡️ **Rate limiting**, CORS, protección XSS/CSRF
- 📝 **Auditoría** de todas las acciones administrativas
- 🐳 **Docker Compose** listo para producción
- 📖 **OpenAPI/Swagger** documentación interactiva
- 🧪 **Tests automatizados** en los tres módulos

---

## 🏗 Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                      NGINX (proxy)                       │
│                  Puerto 80 → Frontend                    │
│                  /api → Backend :8080                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐   ┌────────────┐  │
│  │   Frontend    │    │   Backend    │   │  Scraper   │  │
│  │   Vue 3 +     │◄──►│  Spring Boot │◄──│  Python    │  │
│  │   Tailwind    │    │  + JWT       │   │  + httpx   │  │
│  │   Port: 5173  │    │  Port: 8080  │   │  Scheduled │  │
│  └──────────────┘    └──────┬───────┘   └────────────┘  │
│                              │                           │
│                     ┌────────▼────────┐                  │
│                     │    MongoDB 7    │                  │
│                     │   Port: 27017   │                  │
│                     └─────────────────┘                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Requisitos Previos

| Herramienta | Versión Mínima | Uso |
|---|---|---|
| **JDK 21** | 21.x | Backend Spring Boot |
| **Node.js** | 18+ | Frontend Vue |
| **Python** | 3.12+ | Scraper |
| **MongoDB** | 7.x | Base de datos |
| **Docker** *(opcional)* | 24+ | Desarrollo con contenedores |

---

## 🚀 Inicio Rápido

### Opción A: Desarrollo Local (sin Docker)

#### 1. Clonar y configurar

```bash
cd E:\DramaApp
copy .env.example .env
# Editar .env con tus valores
```

#### 2. Iniciar MongoDB

Instala MongoDB Community Server 7.x y ejecútalo:
```bash
mongod --dbpath=./data/db
```

O usa MongoDB Atlas (configura la URI en `.env`).

#### 3. Iniciar el Backend

```powershell
cd E:\DramaApp\backend
$env:JAVA_HOME = 'C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot'
.\mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=dev
```

El backend estará en http://localhost:8080  
Swagger UI: http://localhost:8080/swagger-ui.html

#### 4. Iniciar el Frontend

```powershell
cd E:\DramaApp\frontend
npm install   # Solo la primera vez
npm run dev
```

El frontend estará en http://localhost:5173

#### 5. Iniciar el Scraper

```powershell
cd E:\DramaApp\scraper
pip install -r requirements.txt   # Solo la primera vez
python -m src.main --once         # Ejecución única
# O con scheduler:
python -m src.main                # Ejecución periódica
```

### Opción B: Docker Compose

```bash
cd E:\DramaApp
copy .env.example .env
docker compose up -d --build
```

Servicios:
- Frontend: http://localhost
- Backend: http://localhost:8080
- Swagger: http://localhost:8080/swagger-ui.html
- MongoDB: localhost:27017

---

## 📁 Estructura del Proyecto

```
E:\DramaApp\
├── frontend/                    # Vue 3 + TypeScript + Tailwind
│   ├── src/
│   │   ├── assets/              # Estilos globales
│   │   ├── components/          # Componentes reutilizables
│   │   │   ├── common/          # Header, Footer, Search, Modal...
│   │   │   ├── catalog/         # SeriesCard, Grid, Filtros
│   │   │   ├── player/          # VideoPlayer 9:16, Nav, Progress
│   │   │   ├── admin/           # DataTable, StatsCard, Badge
│   │   │   └── ads/             # AdSlot configurable
│   │   ├── layouts/             # PublicLayout, AdminLayout
│   │   ├── pages/               # Todas las páginas (público + admin)
│   │   ├── router/              # Vue Router con guards
│   │   ├── stores/              # Pinia (auth, catalog, player, favs)
│   │   ├── services/            # API clients + mock data
│   │   ├── types/               # Interfaces TypeScript
│   │   └── utils/               # SEO, sitemap, helpers
│   ├── public/                  # robots.txt, favicon
│   ├── Dockerfile
│   └── package.json
│
├── backend/                     # Java 21 + Spring Boot 3.4
│   ├── src/main/java/com/dramaapp/
│   │   ├── config/              # Security, CORS, MongoDB, OpenAPI
│   │   ├── controller/
│   │   │   ├── pub/             # Endpoints públicos
│   │   │   └── admin/           # Endpoints administrativos
│   │   ├── model/               # 9 entidades MongoDB
│   │   ├── repository/          # Spring Data + queries custom
│   │   ├── service/             # Lógica de negocio
│   │   ├── dto/                 # DTOs con validación
│   │   ├── security/            # JWT, filtros, rate limiting
│   │   └── exception/           # Manejo global de errores
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── application-dev.yml
│   ├── Dockerfile
│   ├── mvnw / mvnw.cmd
│   └── pom.xml
│
├── scraper/                     # Python 3.12+ + httpx + BS4
│   ├── src/
│   │   ├── adapters/            # Base + Demo + Registry
│   │   ├── models/              # Pydantic v2 models
│   │   ├── core/                # Engine, Scheduler, Dedup, Security
│   │   ├── exporters/           # JSON + API exporters
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/                   # 47 tests con fixtures locales
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker/
│   ├── nginx/nginx.conf         # Proxy + gzip + seguridad
│   └── mongo/init-mongo.js      # Colecciones e índices
│
├── docs/                        # Guías adicionales
│   ├── STREAMING_PROVIDER.md
│   ├── ADDING_SCRAPER_SOURCE.md
│   └── DEPLOYMENT.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Configuración

Todas las credenciales se gestionan mediante variables de entorno. Copia `.env.example` a `.env` y ajusta los valores.

### Variables Principales

| Variable | Descripción | Default |
|---|---|---|
| `MONGO_HOST` | Host de MongoDB | `localhost` |
| `MONGO_PORT` | Puerto de MongoDB | `27017` |
| `MONGO_DATABASE` | Nombre de la BD | `dramaapp` |
| `JWT_SECRET` | Clave secreta JWT (mín. 64 chars) | *requerido* |
| `ADMIN_DEFAULT_USERNAME` | Usuario admin inicial | `admin` |
| `ADMIN_DEFAULT_PASSWORD` | Contraseña admin inicial | `changeme123!` |
| `VIDEO_PROVIDER` | Proveedor de video (`local`/`s3`) | `local` |
| `ADS_ENABLED` | Activar publicidad | `false` |
| `SCRAPER_SCHEDULE_HOURS` | Intervalo del scraper (horas) | `6` |
| `SCRAPER_ALLOWED_DOMAINS` | Dominios permitidos (coma) | *vacío* |

---

## 🔌 API REST

### Endpoints Públicos

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/series` | Listar series publicadas (paginado) |
| GET | `/api/series/{slug}` | Detalle de una serie |
| GET | `/api/series/{slug}/episodes` | Episodios de una serie |
| GET | `/api/episodes/{id}` | Detalle de un episodio |
| GET | `/api/episodes/{id}/playback` | URL de reproducción (verifica derechos) |
| GET | `/api/genres` | Lista de géneros |
| GET | `/api/search?q=` | Búsqueda full-text |
| POST | `/api/analytics/events` | Registrar evento anónimo |
| GET | `/sitemap.xml` | Sitemap XML |
| GET | `/robots.txt` | Robots.txt |

### Endpoints Administrativos (requieren JWT)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/admin/auth/login` | Iniciar sesión |
| CRUD | `/api/admin/sources` | Gestión de fuentes |
| POST | `/api/admin/sources/{id}/trigger-import` | Disparar scraping |
| GET | `/api/admin/imports` | Historial de importaciones |
| POST | `/api/admin/imports/discover` | Recibir datos del scraper |
| GET | `/api/admin/rights/pending` | Derechos pendientes |
| POST | `/api/admin/rights/{id}/approve` | Aprobar derechos |
| POST | `/api/admin/rights/{id}/reject` | Rechazar derechos |
| CRUD | `/api/admin/series` | Gestión de series |
| CRUD | `/api/admin/episodes` | Gestión de episodios |
| POST | `/api/admin/videos/upload-session` | Crear sesión de subida |
| POST | `/api/admin/takedowns/series/{id}` | Solicitar retirada |
| GET | `/api/admin/analytics/dashboard` | Métricas del dashboard |

Documentación interactiva: **http://localhost:8080/swagger-ui.html**

---

## 🖥️ Panel Administrativo

Accede al panel en: **http://localhost:5173/admin/login**

Credenciales por defecto:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Secciones:
1. **Dashboard** — Métricas globales y acciones rápidas
2. **Fuentes** — Gestión de scrapers con activación/desactivación
3. **Importaciones** — Historial de ejecuciones del scraper
4. **Catálogo Descubierto** — Series encontradas, importar o bloquear
5. **Derechos** — Auditoría y aprobación de licencias
6. **Series** — CRUD completo de producciones
7. **Episodios** — Gestión por serie
8. **Videos** — Subida y estado de procesamiento
9. **Takedowns** — Reclamaciones de derechos
10. **Analítica** — Tráfico, popularidad y tendencias

---

## 🕷️ Scraper

El scraper utiliza una arquitectura modular de adaptadores. Cada fuente tiene su propio adaptador independiente.

```bash
# Ejecución única (modo demo)
cd E:\DramaApp\scraper
python -m src.main --once

# Ejecución programada (cada 6 horas por defecto)
python -m src.main

# Tests
python -m pytest tests/ -v
```

### Adaptador Demo
Incluye un adaptador de demostración que parsea fixtures HTML locales y devuelve 5 series con 50 episodios, sin hacer peticiones reales a internet.

Para añadir un nuevo adaptador, consulta: [docs/ADDING_SCRAPER_SOURCE.md](docs/ADDING_SCRAPER_SOURCE.md)

---

## ⚖️ Gestión de Derechos

Cada serie y episodio pasa por un flujo de estados obligatorio:

```
DISCOVERED → METADATA_IMPORTED → RIGHTS_PENDING → APPROVED → PUBLISHED
                                                 ↗           ↓
                                            REJECTED      BLOCKED
                                                           ↓
                                                   TAKEDOWN_PENDING → REMOVED
```

- Solo se publican episodios con derechos `APPROVED`
- Las autorizaciones expiradas se bloquean automáticamente cada hora
- El playback verifica derechos en tiempo real
- Todas las acciones quedan registradas en el log de auditoría

---

## 🔍 SEO

- **URLs legibles**: `/series/el-secreto-del-millonario`
- **Meta tags dinámicos**: título, descripción, canonical por página
- **Open Graph**: para compartir en redes sociales
- **Sitemap XML**: generado dinámicamente en `/sitemap.xml`
- **robots.txt**: configurado correctamente
- **Datos estructurados**: JSON-LD para series y episodios
- **Mobile-first**: diseño adaptable a todos los dispositivos

---

## 💰 Monetización

La capa publicitaria está preparada pero **desactivada por defecto** (`ADS_ENABLED=false`).

Cuando se active:
- Slots publicitarios configurables (banner, pre-roll)
- Separación entre contenido y anuncios
- Compatible con redes de display y video
- Consentimiento de cookies integrado
- No se muestran anuncios en admin, errores o contenido no apto

Para activar, configura las variables `ADS_*` en `.env` y las credenciales de tu red publicitaria.

---

## 🧪 Pruebas

### Scraper (Python)
```bash
cd E:\DramaApp\scraper
python -m pytest tests/ -v
# 47 tests, todos pasando
```

### Backend (Java)
```bash
cd E:\DramaApp\backend
.\mvnw.cmd test
```

### Frontend (TypeScript)
```bash
cd E:\DramaApp\frontend
npm run build  # Verifica compilación TypeScript limpia
```

---

## 🚢 Despliegue

Consulta la guía completa: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Despliegue Económico Recomendado

| Componente | Opción Económica | Coste Estimado |
|---|---|---|
| Frontend | Cloudflare Pages / Vercel | Gratis |
| Backend | Railway / Render / Fly.io | ~$5-7/mes |
| MongoDB | MongoDB Atlas (M0 free tier) | Gratis (hasta 512 MB) |
| CDN/Video | Cloudflare R2 + Stream | Pago por uso |
| Dominio | Namecheap / Porkbun | ~$10/año |
| **Total** | | **~$5-17/mes** |

---

## 📖 Guías Adicionales

- [Integrar un proveedor de streaming](docs/STREAMING_PROVIDER.md)
- [Añadir una fuente al scraper](docs/ADDING_SCRAPER_SOURCE.md)
- [Guía de despliegue económico](docs/DEPLOYMENT.md)

---

## ⚠️ Limitaciones y Pendientes

### Implementado ✅
- [x] Frontend completo con 45+ componentes Vue
- [x] Backend con 30+ endpoints REST y JWT
- [x] Scraper modular con 47 tests
- [x] Docker Compose para desarrollo
- [x] SEO con meta tags, sitemap y Open Graph
- [x] Panel administrativo completo
- [x] Gestión de derechos con flujo de estados
- [x] Reproductor vertical 9:16
- [x] Favoritos e historial local
- [x] Búsqueda full-text
- [x] Rate limiting y seguridad
- [x] Auditoría de acciones admin
- [x] Capa de monetización preparada

### Pendiente / Mejoras Futuras 🔄
- [ ] Tests E2E con Playwright/Cypress
- [ ] Tests de integración frontend con Vitest + Testing Library
- [ ] SSR/SSG para SEO avanzado (Nuxt.js)
- [ ] Notificaciones push para nuevos episodios
- [ ] Sistema de comentarios/reacciones
- [ ] Recomendación personalizada con ML
- [ ] Multi-idioma completo (i18n)
- [ ] CDN para imágenes con transformación automática
- [ ] Monitoring con Prometheus + Grafana
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] App móvil nativa (Flutter/React Native)
- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Caché con Redis para endpoints populares
- [ ] Backup automático de MongoDB

---

## 📄 Licencia

Este proyecto es privado. Todos los derechos reservados.

---

Creado con ❤️ para la comunidad de dramas en español.
