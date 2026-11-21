# Boss Fight — Socratic RAG Tutor Pipeline

Build the core architecture behind **Python Terminal Quest's** live Oracle across three clean modules:

1. **`indexer.py` (`CurriculumIndex`)**:
   - Indexes lesson `concept_md` documentation into searchable chunks (`[lesson_id]`).
   - Strictly rejects any document flagged as a solution or containing forbidden `solution/` source paths (`SolutionLeakError`), guaranteeing reference answers can never enter the retrieval corpus.
   - Scores candidate chunks with TF-IDF/lexical relevance + a boost when `chunk.lesson_id == active_lesson_id`.
2. **`guardrails.py`**:
   - Scrubs emails and API keys (`sk-...`, `AIza...`, `Bearer ...`) from incoming questions.
   - Detects prompt-injection or direct-solution requests (`"ignore previous instructions"`, `"reveal system prompt"`, `"give me the full solution"`, `"write the complete solution"`).
3. **`tutor.py` (`SocraticRagTutor`)**:
   - Scrubs the learner's question first.
   - Refuses blocked queries (`blocked=True`, non-empty refusal, empty `citations`, never calling an external `llm_client`).
   - Otherwise retrieves top grounded chunks and formats Socratic guidance citing `[lesson_id]` tags (via injectable `llm_client` if supplied, or deterministic grounded synthesis offline).
