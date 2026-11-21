# Socratic RAG Oracle — Hands-On Capstone Spec (`src/pyquest/rag/`)

The live AI Oracle backing `POST /api/oracle/ask` is intentionally wired to `StubOracleService` so **you** can build the production RAG engine by hand after finishing Module 12!

## 1. Pluggable Interfaces (`src/pyquest/rag/interfaces.py`)

Implement these clean ABCs without altering the API contract in `OracleResponse`:

- `EmbeddingClient.embed(texts: list[str]) -> list[list[float]]`
- `VectorStore.upsert(...)` and `VectorStore.query(...) -> list[ScoredChunk]`
- `LlmClient.generate(system_prompt: str, user_prompt: str) -> str`
- `RagPipeline.ask(lesson, question, files, last_diagnostics) -> OracleResponse`

## 2. Corpus & Security Invariants

1. **Index ONLY `concept.md` + `lesson.yaml` metadata:** NEVER index `curriculum/**/solution/` or `curriculum/**/tests/` files—your Oracle must never leak reference solutions.
2. **Pre-Flight PII & Secret Scrubbing:** Redact emails, CPF/SSN-style IDs, `Bearer` tokens, and API keys (`sk-`, `AIza`, `ghp_`) before logging or calling an upstream LLM.
3. **Prompt-Injection Guardrails:** Detect and refuse instruction overrides (`"ignore previous instructions"`, `"reveal system prompt"`, `"give me the full solution"`), returning `guardrailTriggered=True` with empty `citations`.
4. **Scoped Hybrid Retrieval:** Combine lexical keyword/BM25 matching with vector cosine similarity, boosting chunks matching the learner's active `lesson.id` while still allowing cross-lesson citations (`OracleCitation`).

## 3. Dual-Mode Environment Variables (`PYQUEST_LLM_*`)

Add these optional `pydantic-settings` fields in `src/pyquest/config.py`:

- `PYQUEST_LLM_PROVIDER`: `offline` (default) | `gemini` | `ollama` | `openai_compat`
- `PYQUEST_LLM_API_KEY`: Provider API key (when not local)
- `PYQUEST_LLM_MODEL`: e.g., `gemini-2.0-flash`, `llama3.2`, `gpt-4o-mini`
- `PYQUEST_LLM_BASE_URL`: Custom endpoint (e.g., `http://127.0.0.1:11434` for Ollama)

On any upstream timeout/error, fall back gracefully to `mode="offline-rag"`.

## 4. Wiring into FastAPI (`src/pyquest/api/app.py`)

Replace `StubOracleService()` in `create_app(...)`:

```python
oracle: RagPipeline = oracle_service or build_your_rag_oracle(curriculum.lessons, cfg)
```

Then unskip the acceptance blueprint in `tests/test_oracle_rag.py` and run `uv run pytest -v tests/test_oracle_rag.py`!
