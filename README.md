<img align="right" src="https://i.imgur.com/EkmzUIf.png" alt="Crypto Dashboard" width="400" height="200">

## **Crypto Dashboard**

A FastAPI-based service to track, store, and manage cryptocurrency data using the CoinGecko API.

---

### 🧰 Overview

- Add cryptocurrencies by **name only** (e.g. `bitcoin`).
- Validates input via **CoinGecko API** and stores metadata in PostgreSQL.
- Supports **full CRUD** operations via both **API** and **Web UI**.
- Background job to **automatically update prices** every _n_ minutes (configurable via `.env`).
- Minimalistic **Jinja2-powered UI** with search, add, delete functionality.
- Redis-based caching to minimize external API calls.

---

### ⚙️ Technologies

- **Python 3.10**, **FastAPI**, **Jinja2**
- **PostgreSQL**, **SQLAlchemy**, **Alembic**
- **Redis** (used for caching CoinGecko data)
- **APScheduler** (background price updater)
- **Docker & Docker Compose**

---

### 🚀 Running Locally (via Docker)

> Requires `docker` and `docker compose`

1. **Clone and enter the project:**
   ```bash
   git clone <your_repo_url>
   cd crypto-dashboard
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

3. **Build and launch the app:**
   ```bash
   docker compose up --build
   ```

4. Open the app:
    - **Web UI**: http://localhost:8000/
    - **API docs (Swagger)**: http://localhost:8000/docs

---

### ✨ Key Features

- **Coin validation**: Accepts full coin names (e.g. `bitcoin`, `ethereum`).
- **Conflict detection**: Prevents duplicates when multiple coins share a symbol.
- **Caching**: Coin list from CoinGecko is cached in Redis for fast lookup.
- **Scheduler**: On startup and then every `UPDATE_INTERVAL_MINUTES`, updates prices.
- **Manual trigger**: Available via API (no JS button in UI).
- **CG ID**: All operations use CoinGecko ID (e.g. `bitcoin`) as identifier.

---

### 📃 API Endpoints

> Base URL: `http://localhost:8000/cryptos/`

| Endpoint          | Method | Description                                   |
|-------------------|--------|-----------------------------------------------|
| `/`               | GET    | Get all cryptos                               |
| `/`               | POST   | Add a crypto by name                          |
| `/{cg_id}`        | GET    | Retrieve single crypto by CoinGecko ID        |
| `/{cg_id}`        | PUT    | Update name/symbol manually                   |
| `/{cg_id}`        | DELETE | Delete a crypto                               |
| `/update-prices/` | POST   | Trigger price refresh manually (via API only) |

---

### 🗺 Web UI

- Powered by **Jinja2** templates with **Bootstrap 5**.
- Features:
    - Search cryptos by name, symbol, or ID
    - Add cryptos by name
    - Delete existing cryptos
    - Reset filters

---

### 🔄 Price Syncing

- Runs **on startup** and every `UPDATE_INTERVAL_MINUTES` (configurable via `.env`)
- Uses **APScheduler** in the background
- Manual trigger available via API `/cryptos/update-prices/`

---

### ⏱ Time Spent

- API and architecture: **~2h**
- Redis, scheduler, validation: **~1.5h**
- UI: **~2h**
- Dockerization, cleanup, testing, docs: **~1.5h**
- **Total**: ~7h

---

### 🔗 Future Ideas

- Add support for searching/adding by symbol
- Inline editing from dashboard
- Symbol conflict resolution UI
- Historical price charts
- Pagination, sorting, filters
- Move scheduler to **Celery** for better scalability and reliability
