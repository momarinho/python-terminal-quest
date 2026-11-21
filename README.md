# Python Terminal Quest

A calm Obsidian 16-bit RPG workspace for mastering modern **Python 3.13**, **Data Structures**, **FastAPI**, **Pydantic v2**, and **AI Engineering**.

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
