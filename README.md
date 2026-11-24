# Python Terminal Quest

A calm Obsidian 16-bit RPG learning workspace for mastering modern **Python 3.13**, **Data Structures**, **OOP**, **Django/DRF**, **Architecture & Typing**, **Asyncio**, **Raw SQL**, **SQLAlchemy 2.0 & Alembic**, **FastAPI**, **Redis Caching/Rate Limiting**, **Distributed Resilience**, and **AI & Production Agentic RAG**.

**Complete Curriculum:** 12 modules • 75 interactive lessons (63 core + 12 Boss Fights, balanced from a gentle Day-1 warm-up to 2026 Dev Pleno patterns) • 3 Portfolio Guild PRDs (`CLI Financial Ledger Reconciler`, `High-Concurrency Inventory & Audit Service`, `Mini-Sidekiq Distributed Job Engine + AI Triage & AWS Mapping`).

---

## Architecture Overview

```mermaid
flowchart LR
    UI["React + TypeScript + Monaco UI"] -->|REST JSON /api/*| API["FastAPI App (src/pyquest/api/app.py)"]
    API --> Loader["CurriculumLoader (YAML + Markdown)"]
    API --> Store["ProgressStore (SQLite WAL)"]
    API --> Grader["PytestGrader (AST Pre-Check + Isolated Subprocess + JUnit XML)"]
    API --> Oracle["AgenticRagOracle (BM25 + Vector RRF + AST Inspector + Guardrails)"]
    Loader --> Disk["curriculum/module-* (75 Stages + 3 Guild PRDs)"]
```

### Engineering Highlights
- **Agentic Hybrid RAG Oracle (`src/pyquest/rag/`):** Okapi BM25 + Blake2b dense vectors fused with **Reciprocal Rank Fusion (RRF)**, adaptive query rewriting, zero-spoiler Python `ast` code gap inspection, Second-Brain retrieval across your saved Field Notes, multi-turn token-budgeted history, PII/injection & post-generation spoiler firewalls, transparent reasoning trace, and live `ollama` / `gemini` / `openai_compat` LLM adapters with zero-key `offline-rag` fallback.
- **Isolated `pytest` Grader (`src/pyquest/runner/grader.py`):** Pre-validates Python syntax via `ast.parse` for clickable line/column diagnostics in Monaco, blocks forbidden `conftest.py` / `tests/` path overrides, isolates environment variables, enforces POSIX CPU/file-size `rlimit`s + wall-clock timeouts, and parses JUnit XML + `stdout`/`stderr`.
- **SQLite WAL State & Spaced Review (`src/pyquest/persistence/store.py`):** Persists multi-file code drafts, study notes, flagged stages, daily streaks, 5-tier Hero Companion progression, **Cold Clear vs. Assisted (`needsReview`)** status, Portfolio Guild checklists, and full JSON export/import backups (`GET /api/progress/export`, `POST /api/progress/import`, `POST /api/progress/reset`).
- **Workspace Productivity (`web/src/`):** Split-pane Obsidian Monaco Editor with reference solution diffing, clickable syntax diagnostics, 1-click Battle Log AI diagnosis button, Quick-Action Oracle prompt chips, read-only **`Tests` (`pytest`)** inspector, global `Ctrl+K` command palette, 5-tier Hero Companion 2.0 + Armory + optional AFK mini-game, Boss Gate lock toggle, and Campfire LinkedIn reflection outlines.
- **Hardened Container & Demo Mode:** Multi-stage non-root `Dockerfile` (`USER pyquest`) and optional read-only `PYQUEST_DEMO_MODE=true` guard disabling arbitrary code execution and state imports for safe public previews.

---

## Project Roadmap & Feature Checklist

### Completed
- [x] **12-Module, 75-Lesson Curriculum (`01-01` .. `12-05`):** Progressive path from gentle Day-1 fundamentals (`01-01`–`01-03`) through FastAPI, Asyncio, SQLAlchemy 2.0/Alembic, Distributed Resilience, and Production RAG.
- [x] **3 Portfolio Guild Projects:** End-to-end PRDs, sprint checklists, code review criteria, and AWS mapping.
- [x] **Sandboxed `pytest` Grader & AST Diagnostics:** Isolated subprocess runner with POSIX `rlimit`s, forbidden path checks, and Monaco error markers.
- [x] **Obsidian Workspace UI:** Multi-file Monaco editor, Solution Diff viewer, Read-Only Test Inspector, Battle Log, Review Queue, Campfire LinkedIn cards, and `Ctrl+K` Quick-Jump Palette.
- [x] **Hero Companion 2.0, Armory & AFK Mini-Game:** 5-tier SVG sprites reacting dynamically to typing, runs, and stage mastery, plus optional Boss Gate progression lock.
- [x] **Live Agentic Hybrid RAG Oracle (`src/pyquest/rag/`):** Zero-leak indexer (`SolutionLeakError`), Okapi BM25 + Vector RRF retrieval, Adaptive Query Rewrite, TTL cache, `ast` code inspector, multi-turn memory, Second-Brain Field Notes retrieval, pre/post guardrails, and dual-mode LLM/offline execution.
- [x] **Automated RAG Evaluation Endpoint (`GET /api/oracle/eval`):** Measures `Recall@K`, `MRR@K`, `0%` solution leakage, `100%` guardrail block rate, and `p50`/`p95` latency.
- [x] **Hardened Docker & CI Pipeline:** Non-root multi-stage Dockerfile, read-only `PYQUEST_DEMO_MODE`, and GitHub Actions (`ruff`, `mypy`, `pytest`, `tsc`, Vite build).

### Up Next (Planned Evolutions)
- [ ] **SSE Token Streaming (`POST /api/oracle/stream`):** Stream live LLM tokens word-by-word into the workspace AI Oracle panel.
- [ ] **Optional Neural Embedding Cache (`SQLite`):** Support `nomic-embed-text` (Ollama) and `text-embedding-004` (Gemini) cached locally in SQLite alongside `LocalHashedEmbeddingClient`.
- [ ] **Pyodide (WASM) Pure-Browser Demo Mode:** Run beginner modules directly in-browser via WebAssembly so GitHub Pages / static previews can grade code with zero backend server.
- [ ] **Custom Curriculum Pack Loader:** Allow importing community YAML/Markdown lesson packs for DevOps, Data Engineering, or System Design.

---

## Curriculum Map (12 Modules • 75 Stages)

| Module | Topic Focus | Stages | Boss Fight |
|---|---|---|---|
| **01** | Python Fundamentals (`Decimal`, `match/case`, mutable traps, domain exceptions) | 9 | Fee & Policy Evaluator Engine |
| **02** | Data Structures & Core Algorithms (`deque`, `Counter`, `heapq`, BST) | 8 | Log Stream Sliding-Window & Top-K Tracker |
| **03** | Object-Oriented Programming (`@dataclass`, `@property`, `Protocol`, dunders) | 6 | Extensible Order Book Domain |
| **04** | Advanced Python (Decorators, `yield`/`batched`, context managers, atomic writes) | 7 | Streaming PII Log Redactor |
| **05** | Ecosystem & Web Base (NumPy, Pandas, Matplotlib, Flask, Requests, BS4, Django/DRF) | 8 | Automated Web Report Collector |
| **06** | Architecture, Typing & `pytest` (`src/` layout, PEP 695/Pydantic v2, test doubles) | 5 | Multi-Module Billing Core |
| **07** | Concurrency & `asyncio` (GIL/profiling, pools, `TaskGroup`, `httpx` backpressure) | 5 | Resilient Async Health Aggregator |
| **08** | Raw SQL Engineering (CTEs, `EXPLAIN QUERY PLAN`, keyset cursors, ACID/locks) | 5 | Inventory Reservation Engine |
| **09** | SQLAlchemy 2.0 & Alembic (Unit of Work/DTOs, `selectinload` zero-N+1, migrations) | 5 | Zero-N+1 Order Repository |
| **10** | FastAPI Production Systems (`Depends`, RFC 7807, PyJWT RBAC, `contextvars`, Redis) | 6 | Hardened Admin Gateway API |
| **11** | Distributed Resilience (Idempotency SHA-256, Circuit Breaker, Outbox, DLQ, HMAC) | 6 | Resilient Event Relay Engine |
| **12** | AI Engineering & Production RAG (PII scrubbing, Pydantic repair, hybrid citations, evals) | 5 | Socratic RAG Tutor Pipeline |

### Portfolio Guild Gates (`curriculum/projects.yaml`)
1. **Gate #1 (After Module 5):** *CLI Financial Ledger Reconciler* (`Decimal`, streaming CSV, atomic reports, CI)
2. **Gate #2 (After Module 9):** *High-Concurrency Inventory & Audit Service* (PostgreSQL 16, SQLAlchemy 2.0 zero-N+1, optimistic locking, Alembic)
3. **Gate #3 (After Module 12):** *Mini-Sidekiq Distributed Job Engine + AI Triage* (Outbox, Circuit Breaker, DLQ, RAG triage + evals, AWS RDS/SQS/S3/ECS mapping)

---

## Agentic Hybrid Socratic RAG Oracle (`src/pyquest/rag/`)

Out of the box, the in-app **AI Oracle** (`POST /api/oracle/ask`) runs in **zero-key `offline-rag` mode** with full BM25 + Vector RRF retrieval, `ast` code inspection, Field Notes recall, and Socratic guardrails.

To connect a generative LLM (optional), copy `.env.example` to `.env` and configure `PYQUEST_LLM_PROVIDER`:
```bash
cp .env.example .env
# PYQUEST_LLM_PROVIDER=ollama   # + OLLAMA_BASE_URL=http://127.0.0.1:11434
# PYQUEST_LLM_PROVIDER=gemini   # + GEMINI_API_KEY=AIza...
```

Inspect live RAG benchmark metrics anytime at `GET /api/oracle/eval` or see [`src/pyquest/rag/CAPSTONE_README.md`](src/pyquest/rag/CAPSTONE_README.md).

---

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

### Read-Only Demo Mode
To preview the UI safely without executing arbitrary learner code or accepting progress imports:
```bash
PYQUEST_DEMO_MODE=true uv run pyquest serve --port 8080
```

---

## Verification & Docker
```bash
uv run ruff check .
uv run mypy src
uv run pytest
cd web && npx tsc --noEmit && npm run build
```

```bash
docker compose up --build
```
