# Socratic Agentic Hybrid RAG Oracle (`src/pyquest/rag/`)

The live AI Oracle backing `POST /api/oracle/ask` is powered by `AgenticRagOracle`, combining Module 12's security and retrieval invariants with production hybrid + agentic RAG patterns.

## 1. Architecture Overview

1. **Zero-Leak Curriculum Indexer ([indexer.py](indexer.py)):**
   - Indexes ONLY `curriculum/**/concept.md` + `lesson.yaml` metadata into section-aware `DocumentChunk`s with 1-sentence overlap.
   - Enforces `validate_safe_corpus_path()` (`SolutionLeakError`) so `solution/` and `tests/` files are strictly rejected.
2. **Pre-Flight Guardrails & PII Scrubbing ([guardrails.py](guardrails.py)):**
   - Redacts API keys (`sk-`, `AIza`, `ghp_`, `jina_`), `Bearer` tokens, emails, and CPF/SSN IDs before caching or calling upstream LLMs.
   - Blocks prompt-injection overrides, system-prompt exfiltration, and full-solution dump prompts (`guardrailTriggered=True`, empty citations).
3. **Hybrid Okapi BM25 + Vector RRF Retriever ([retriever.py](retriever.py)):**
   - `LocalHashedEmbeddingClient` provides deterministic zero-dependency 256-dim dense vectors alongside `HybridRrfVectorStore` (Okapi BM25 `k1=1.5, b=0.75` + cosine similarity fused with Reciprocal Rank Fusion and active-lesson boosting).
4. **Agentic Adaptive Rewrite & TTL Cache ([pipeline.py](pipeline.py)):**
   - Grades initial retrieval quality; on vague queries (`"why is my test failing?"`) or low-confidence diagnostic errors, automatically rewrites the query using `last_diagnostics` + editor symbols (`def`/`class`) + stage tags for a second retrieval pass.
   - Caches exact matches with a 300s TTL for instant repeated queries.
5. **Dual-Mode LLM Generation ([llm_client.py](llm_client.py)):**
   - Supports `offline` (default zero-key deterministic Socratic RAG), `ollama`, `gemini`, and `openai_compat` via `PYQUEST_LLM_*` settings in `src/pyquest/config.py`.
   - Falls back gracefully to `mode="offline-rag"` on any upstream LLM error or timeout.
