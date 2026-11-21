# Python Terminal Quest

A calm Obsidian 16-bit RPG workspace for mastering modern **Python 3.13**, **Data Structures**, **OOP**, **Django/DRF**, **Architecture**, **Asyncio**, **Raw SQL**, **SQLAlchemy 2.0**, **FastAPI**, **Redis Caching/Rate Limiting**, **Distributed Resilience**, and **AI & Production RAG**.

**Complete Curriculum:** 12 modules • 75 interactive lessons (63 core + 12 Boss Fights) • 3 Portfolio Guild PRDs (`CLI Financial Ledger Reconciler`, `High-Concurrency Inventory & Audit Service`, `Mini-Sidekiq Distributed Job Engine + AI Triage & AWS Mapping`).

## Quick Start (Local Development)

### 1. Backend (Python + `uv`)
```bash
uv sync
uv run pyquest serve --port 8080
```

### 2. Frontend (Vite + React + Monaco)
```bash
cd web
npm install
npm run dev
```

Or build the frontend once and let FastAPI serve the entire app at `http://localhost:8080`:
```bash
cd web && npm run build && cd ..
uv run pyquest serve --port 8080
```

## DIY Socratic RAG Capstone (`src/pyquest/rag/`)

By default, the in-app **Oracle** (`POST /api/oracle/ask`) runs in **DIY Capstone Stub mode** (`StubOracleService`, `mode="stub"`) so **you** can implement your own grounded hybrid RAG engine after finishing Module 12!

See [`src/pyquest/rag/CAPSTONE_README.md`](src/pyquest/rag/CAPSTONE_README.md) for:
- The pluggable `VectorStore`, `EmbeddingClient`, `LlmClient`, and `RagPipeline` contracts in `src/pyquest/rag/interfaces.py`.
- Zero-solution-leak indexing rules, PII scrubbing, and prompt-injection guardrails.
- Blueprint acceptance tests waiting in `tests/test_oracle_rag.py`.

## Verification
```bash
uv run ruff check .
uv run pytest
cd web && npx tsc --noEmit && npm run build
```

## Docker
```bash
docker compose up --build
```
