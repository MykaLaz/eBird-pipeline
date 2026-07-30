# eBird Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.5.4+-yellow.svg)](https://duckdb.org/)
[![uv](https://img.shields.io/badge/uv-0.5+-purple.svg)](https://github.com/astral-sh/uv)
[![Licence: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

A data engineering learning project: an end-to-end pipeline that pulls bird observation data from the eBird API and prepares it for analytics — raw lake → warehouse → data marts.

## Contents
1. [Description](#description)
2. [Status](#status)
3. [Architecture](#architecture)
4. [Used Tools](#used-tools)
5. [Project Structure](#project-structure)
6. [Setup](#setup)
7. [Design Notes](#design-notes)
8. [Learning Goals](#learning-goals)
9. [Future Work](#future-work)
10. [Contacts](#contacts)
11. [Licence](#licence)

### Description
This is a personal project built to learn core data engineering concepts hands-on (API ingestion, data lakes, dimensional modeling, orchestration) rather than to hide them behind managed cloud services. Everything runs locally with free, open-source tools.

### Status
 
🚧 **In progress.** Currently: ingestion layer complete, warehouse and orchestration in progress.
 
- [x] **Phase 1 — Ingestion**: authenticated eBird API client, raw data lake (partitioned JSON)
- [x] **Phase 2 — Landing**: load raw JSON into DuckDB
- [x] **Phase 3 — Transform**: dbt staging + core (star schema) models
- [ ] **Phase 4 — Marts**: analytics-ready aggregated views
- [ ] **Phase 5 — Orchestration**: Airflow DAG tying it all together
- [ ] **Phase 6 — Consumption**: BI dashboard on top of the marts

### Architecture
The project is realised according to the Medallion Architecture.
```mermaid
graph LR
    A[eBird API] -->|Ingest (Python)| B[Raw Data Lake <br> Partitioned JSON]
    subgraph Orchestrated with Airflow
        B -->|DuckDB + dbt| C[Staging + Warehouse]
        C -->|dbt| D[Data Marts]
    end
    D -->|Apache SuperSet| E[Dashboard]

    style B fill:#f9d5b0,stroke:#333
    style C fill:#b0d9f9,stroke:#333
    style D fill:#b0f9b0,stroke:#333
```

### Used Tools
 
| Layer | Tool |
|---|---|
| Package/dependency management | uv |
| Ingestion | Python, `requests` |
| Raw data lake | Local filesystem, partitioned by ingestion date |
| Warehouse | DuckDB (planned) |
| Transformations | dbt-core (planned) |
| Visualization | Apache Superset (planned) |
| Orchestration | Airflow (planned) |
| Linting/formatting | Ruff |

### Project Structure

```
eBird-pipeline/
├── src/
│   └── ingest/
│       ├── __init__.py
│       ├── config.py      # loads API key + base URL from environment
│       ├── client.py      # EBirdClient: authenticated wrapper around the eBird API
│       └── extract.py     # orchestration: fetch + write to raw data lake
├── data/
│   └── raw/                # gitignored — the raw data lake
├── tests/
├── .env                     # gitignored — holds EBIRD_API_KEY
├── pyproject.toml
└── README.md
```

### Setup
 
1. Get a free eBird API key from the [eBird API documentation](https://documenter.getpostman.com/view/664302/S1ENwy59).
2. Clone the repo and install dependencies:
```bash
   uv sync
```
3. Create a `.env` file in the project root:
```
   EBIRD_API_KEY=your_key_here
```
4. Run the ingestion script:
```bash
   uv run python -m src.ingest.extract
```
   This fetches recent observations for a region and writes them to
   `data/raw/observations/date=YYYY-MM-DD/<region>.json`.
 
### Design Notes
 
A few deliberate decisions worth calling out, since they reflect the DE concepts this project is meant to practice:
 
- **Client/extraction separation**:
  - `EBirdClient` only knows how to talk to the API;
  - `extract.py` decides what to do with the data (write to disk). This keeps the client
  reusable and independently testable.
- **Raw zone stays untouched**: JSON is written to the lake exactly as the API returns it (schema-on-read). Parsing/validation happens later, at the staging layer — not here.
- **Fail-fast config**: missing environment variables raise immediately at import time, rather than surfacing as a confusing error deep into a pipeline run.
- **Retryable HTTP session**: the client uses a `requests.Session` with mounted retry/backoff
  logic for transient failures (429/5xx), rather than treating every failed call as fatal.
- **Data modeling"**: fact_observation's primary key is (checklist_id, species_code); location_id was verified redundant in the key since each checklist maps to exactly one location

### Learning Goals
 
This project is being built incrementally, pairing each implementation step with the
underlying concept it's meant to teach (OOP design, HTTP fundamentals, dimensional
modeling, orchestration, OLTP vs. OLAP tradeoffs). Design decisions and their reasoning
are documented as the project evolves.

### Future Work

This project is being deliberately built in two versions to compare two different approaches to the warehouse layer. v1 (current) uses DuckDB with dbt for batch, scheduled transformations — a straightforward, well-established pattern for a solo analytics pipeline. v2 will migrate the warehouse to ClickHouse, re-implementing the Medallion architecture (Bronze → Silver → Gold) using Materialized Views instead of dbt models — trading scheduled batch runs for automatic, incremental transformations that trigger on insert. The goal isn't just tool exposure: building both versions is meant to make the batch-vs-incremental tradeoff concrete, and to understand firsthand when a column-store OLAP engine with native streaming-style transforms is worth the added operational complexity over a simpler batch pipeline.

### Contacts
**Author:** Marina Lazareva

**GitHub:** [github.com/MykaLaz](https://github.com/MykaLaz)

**Telegram:** @MykaLaz

**Email:** myka.lazareva@icloud.com

### Licence
MIT © 2026
