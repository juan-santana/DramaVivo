# DramaApp Scraper Module

A modular, asynchronous web scraping and ingestion engine built for **DramaApp**, a short drama streaming platform.

The system is designed with a pluggable adapter pattern, strict domain and network security policies, intelligent deduplication, scheduled background execution via APScheduler, and multi-channel export capabilities (JSON files and REST backend APIs).

---

## 📁 Project Structure

```
E:\DramaApp\scraper\
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point and scheduler runner
│   ├── config.py            # Pydantic v2 settings loaded from env
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py         # Scraping engine orchestrator & fault isolation
│   │   ├── scheduler.py      # APScheduler periodic runner
│   │   ├── dedup.py          # Title normalization and URL deduplication
│   │   └── security.py       # Domain allowlist, SSRF & private IP blocker, robots.txt
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract BaseAdapter contract
│   │   ├── demo_adapter.py   # Demo adapter using local HTML fixtures
│   │   └── registry.py       # Pluggable adapter registry & factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── source.py         # SourceConfig Pydantic model
│   │   ├── series.py         # DiscoveredSeries Pydantic model  
│   │   ├── episode.py        # DiscoveredEpisode Pydantic model
│   │   ├── import_job.py     # ImportJobResult Pydantic model
│   │   └── rights.py         # ContentRights Pydantic model
│   └── exporters/
│       ├── __init__.py
│       ├── api_exporter.py   # HTTP client exporter to backend API
│       └── json_exporter.py  # Local JSON file exporter (for dev/testing)
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest shared fixtures
│   ├── fixtures/
│   │   ├── demo_catalog.html # Sample HTML page for demo adapter
│   │   ├── demo_series.html  # Sample series detail page
│   │   └── demo_data.json    # Expected parsed data
│   ├── test_adapters.py      # Unit tests for adapters and registry
│   ├── test_dedup.py         # Deduplication and title normalization tests
│   ├── test_models.py        # Pydantic model validation tests
│   ├── test_security.py      # Allowlist and SSRF prevention tests
│   └── test_engine.py        # Integration test with demo adapter and exporters
├── requirements.txt
├── pytest.ini
├── Dockerfile
└── README.md
```

---

## 🚀 Key Features

### 1. Modular Adapter Pattern
Each drama provider or catalog site is represented by an adapter extending `BaseAdapter`:
- `discover_series()`: Discovers series from catalog pages.
- `discover_episodes(series_url)`: Scrapes individual episode sequences, durations, video streams, and thumbnails.
- Adapters are registered in `AdapterRegistry` and dynamically instantiated based on the source configuration.

### 2. Multi-Layer Security & SSRF Protection
The `SecurityManager` safeguards against malicious links and web crawler abuse:
- **Domain Allowlist**: Only explicitly permitted domains (and subdomains) can be accessed.
- **SSRF & Private IP Blocking**: Rejects private, loopback, and link-local IP addresses (e.g., `127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`, `localhost`).
- **Scheme Validation**: Enforces `http` / `https` protocols; blocks `file://`, `ftp://`, `javascript:`, etc.
- **Robots.txt Adherence**: Caches and checks `robots.txt` rules per domain.
- **Rate Limiting**: Enforces minimum delay per host to prevent request floods.

### 3. Deduplication Logic
- **URL Canonicalization**: Normalizes URLs, stripping trailing slashes to prevent duplicate fetches.
- **Title Normalization**: Converts unicode accents (NFKD), removes punctuation, and collapses whitespace.
- **Fuzzy Duplicate Detection**: Detects similar drama titles using sequence matching.

### 4. Resilient Orchestration
- Individual source failures are isolated: if one source fails, other sources continue processing.
- Generates structured `ImportJobResult` summaries (status `COMPLETED`, `PARTIAL`, or `FAILED`).

---

## ⚙️ Configuration

Settings are managed via `src/config.py` using `pydantic-settings` and can be configured through `.env` or environment variables:

| Variable | Default | Description |
|---|---|---|
| `API_URL` | `http://localhost:8000/api/v1` | DramaApp backend API URL |
| `API_KEY` | `""` | Bearer token / API key for backend authentication |
| `SCHEDULE_HOURS` | `6` | Interval in hours between scheduled runs |
| `ALLOWED_DOMAINS` | `example.com,demo.dramaapp.local,shortdrama.local` | Comma-separated domain allowlist |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `OUTPUT_DIR` | `output` | Directory where JSON exports are saved |
| `REQUEST_TIMEOUT` | `30.0` | Default HTTP request timeout in seconds |

Example `.env`:
```ini
API_URL=http://localhost:8000/api/v1
API_KEY=your_secret_api_key_here
SCHEDULE_HOURS=6
ALLOWED_DOMAINS=demo.dramaapp.local,shortdrama.local,example.com
LOG_LEVEL=INFO
OUTPUT_DIR=output
```

---

## 📦 Installation & Setup

1. Clone or navigate to the scraper directory:
   ```bash
   cd E:\DramaApp\scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Running the Scraper

### One-Time Execution (`--once`)
Runs a single scrape cycle against configured sources and outputs results immediately:
```bash
python -m src.main --once
```

### Continuous Scheduled Background Service
Runs the APScheduler service according to configured hours (default: every 6 hours):
```bash
python -m src.main
```

Override schedule interval or log level via CLI flags:
```bash
python -m src.main --schedule-hours 4 --log-level DEBUG
```

---

## 🧪 Running Tests

The test suite contains comprehensive unit and integration tests covering models, adapters, deduplication, security, and the engine. Tests strictly use local fixtures and never execute external HTTP calls.

Run all tests with pytest:
```bash
python -m pytest tests/ -v
```

Run tests with coverage reporting:
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

---

## 🐳 Docker Deployment

Build and run using the included Dockerfile:
```bash
docker build -t dramaapp-scraper .
docker run -d --name dramaapp-scraper --env-file .env dramaapp-scraper
```
