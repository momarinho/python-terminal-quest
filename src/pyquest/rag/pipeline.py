from __future__ import annotations

import hashlib
import re
import time
from collections import OrderedDict

from pyquest.config import Settings
from pyquest.domain.models import LessonSpec, OracleCitation, OracleResponse
from pyquest.rag.guardrails import (
    detect_guardrail_violation,
    scrub_pii_and_secrets,
    verify_citations,
)
from pyquest.rag.indexer import index_curriculum_lessons
from pyquest.rag.interfaces import EmbeddingClient, LlmClient, RagPipeline, ScoredChunk
from pyquest.rag.llm_client import build_llm_client
from pyquest.rag.retriever import (
    HybridRrfVectorStore,
    LocalHashedEmbeddingClient,
    tokenize_for_search,
)

_IDENT_RE = re.compile(r"\b(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)\b")
_VAGUE_QUERY_PATTERNS = (
    "why is my test failing",
    "why does it fail",
    "what is wrong",
    "help me",
    "not working",
    "doesnt work",
    "doesn't work",
    "fix this",
    "debug",
)


class _ExactMatchTtlCache:
    """Bounded exact-match TTL cache (Week 6 pattern) for repeated Oracle queries."""

    def __init__(self, *, max_entries: int = 256, ttl_seconds: float = 300.0) -> None:
        self._max_entries = max_entries
        self._ttl_seconds = ttl_seconds
        self._store: OrderedDict[str, tuple[float, OracleResponse]] = OrderedDict()

    def get(self, key: str) -> OracleResponse | None:
        item = self._store.get(key)
        if item is None:
            return None
        expires_at, response = item
        if time.monotonic() > expires_at:
            self._store.pop(key, None)
            return None
        self._store.move_to_end(key)
        return response

    def put(self, key: str, response: OracleResponse) -> None:
        self._store[key] = (time.monotonic() + self._ttl_seconds, response)
        self._store.move_to_end(key)
        while len(self._store) > self._max_entries:
            self._store.popitem(last=False)


def _extract_code_symbols(files: dict[str, str]) -> list[str]:
    symbols: list[str] = []
    for content in files.values():
        for match in _IDENT_RE.findall(content):
            if match not in symbols:
                symbols.append(match)
    return symbols[:6]


def _needs_adaptive_rewrite(question: str, hits: list[ScoredChunk], last_diagnostics: str) -> bool:
    lowered = question.lower().strip()
    if any(pat in lowered for pat in _VAGUE_QUERY_PATTERNS):
        return True
    if not hits:
        return True
    q_tokens = set(tokenize_for_search(question))
    top_tokens = set(tokenize_for_search(hits[0].chunk.content))
    overlap = len(q_tokens & top_tokens)
    if bool(last_diagnostics.strip()) and hits[0].score < 0.65:
        return True
    return overlap == 0 and hits[0].score < 0.60


def _merge_hits(
    primary: list[ScoredChunk],
    secondary: list[ScoredChunk],
    *,
    top_k: int = 4,
) -> list[ScoredChunk]:
    best_by_id: dict[str, ScoredChunk] = {}
    for hit in [*primary, *secondary]:
        existing = best_by_id.get(hit.chunk.chunk_id)
        if existing is None or hit.score > existing.score:
            best_by_id[hit.chunk.chunk_id] = hit
    merged = sorted(best_by_id.values(), key=lambda item: item.score, reverse=True)
    return merged[:top_k]


class AgenticRagOracle(RagPipeline):
    """Production Agentic Hybrid RAG Oracle (Guardrail -> Hybrid BM25+Vector RRF -> Grade/Rewrite -> Cache -> Socratic Generate)."""

    def __init__(
        self,
        lessons: list[LessonSpec],
        *,
        embedder: EmbeddingClient | None = None,
        store: HybridRrfVectorStore | None = None,
        llm_client: LlmClient | None = None,
        cache_ttl_seconds: float = 300.0,
    ) -> None:
        self._lessons_by_id = {lesson.id: lesson for lesson in lessons}
        self._embedder = embedder or LocalHashedEmbeddingClient()
        self._store = store or HybridRrfVectorStore()
        self._llm_client = llm_client
        self._cache = _ExactMatchTtlCache(ttl_seconds=cache_ttl_seconds)

        chunks = index_curriculum_lessons(lessons)
        if chunks:
            embeddings = self._embedder.embed([chunk.content for chunk in chunks])
            self._store.upsert(chunks, embeddings)

    def _build_cache_key(
        self,
        lesson_id: str,
        scrubbed_question: str,
        scrubbed_files: dict[str, str],
        scrubbed_diagnostics: str,
    ) -> str:
        provider_tag = self._llm_client.provider_name if self._llm_client else "offline-rag"
        files_digest = hashlib.blake2b(
            "\n".join(f"{k}:{v}" for k, v in sorted(scrubbed_files.items())).encode("utf-8"),
            digest_size=12,
        ).hexdigest()
        raw = f"{provider_tag}|{lesson_id}|{scrubbed_question.lower()}|{files_digest}|{scrubbed_diagnostics}"
        return hashlib.blake2b(raw.encode("utf-8"), digest_size=16).hexdigest()

    def _retrieve_hybrid(self, query_text: str, *, active_lesson_id: str, top_k: int = 4) -> list[ScoredChunk]:
        query_vec = self._embedder.embed([query_text])[0]
        return self._store.hybrid_query(
            query_text,
            query_vec,
            top_k=top_k,
            active_lesson_id=active_lesson_id,
        )

    def _rewrite_query(
        self,
        lesson: LessonSpec,
        scrubbed_question: str,
        scrubbed_files: dict[str, str],
        scrubbed_diagnostics: str,
    ) -> str:
        parts = [scrubbed_question, lesson.title, *lesson.tags]
        if scrubbed_diagnostics:
            first_line = scrubbed_diagnostics.splitlines()[0][:200]
            parts.append(first_line)
        symbols = _extract_code_symbols(scrubbed_files)
        if symbols:
            parts.extend(symbols)
        return " ".join(part for part in parts if part).strip()

    def _build_offline_socratic_answer(
        self,
        lesson: LessonSpec,
        scrubbed_question: str,
        hits: list[ScoredChunk],
        scrubbed_diagnostics: str,
        *,
        rewrote_query: bool,
        fallback_reason: str | None = None,
    ) -> str:
        lines: list[str] = [
            f"**Socratic Guidance for `[{lesson.id}] {lesson.title}`**"
        ]
        if fallback_reason:
            lines.append(
                f"_Upstream LLM unavailable (`{fallback_reason}`); switched seamlessly to deterministic offline RAG._"
            )

        if scrubbed_diagnostics:
            diag_line = scrubbed_diagnostics.splitlines()[0][:240]
            lines.append(f"\n**Latest Verification Signal:**\n> `{diag_line}`")

        if hits:
            lines.append("\n**Relevant Concept Grounding:**")
            seen_lessons: set[str] = set()
            for hit in hits[:3]:
                lid = hit.chunk.metadata.get("lesson_id", lesson.id)
                section = hit.chunk.metadata.get("section", "Concept")
                snippet = " ".join(hit.chunk.content.split())
                if len(snippet) > 260:
                    snippet = snippet[:257].rstrip() + "..."
                tag = f"[{lid}]" if lid not in seen_lessons else f"[{lid} · {section}]"
                seen_lessons.add(lid)
                lines.append(f"- **{tag}**: {snippet}")

        nudge = lesson.hints[0] if lesson.hints else lesson.objective
        lines.append(f"\n**Next Step to Check (`[{lesson.id}]`):** {nudge}")
        if rewrote_query:
            lines.append(
                "_Agentic retrieval note: broadened search using your active stage tags and test diagnostics._"
            )
        elif scrubbed_question:
            lines.append(
                f"_Focused on your question:_ `{scrubbed_question[:120]}`"
            )
        return "\n".join(lines)

    def _build_live_prompts(
        self,
        lesson: LessonSpec,
        scrubbed_question: str,
        scrubbed_files: dict[str, str],
        scrubbed_diagnostics: str,
        hits: list[ScoredChunk],
    ) -> tuple[str, str]:
        system_prompt = (
            "You are the Socratic Staff Python Mentor inside Python Terminal Quest.\n"
            "Rules:\n"
            "1. Ground every explanation in the retrieved lesson context and cite lesson IDs like [09-02].\n"
            "2. Diagnose the learner's active code and latest pytest failure concisely.\n"
            "3. NEVER provide a full copy-paste solution to the exercise; guide with targeted hints or tiny 2-4 line illustrative snippets."
        )
        context_block = "\n".join(
            f"[{h.chunk.metadata.get('lesson_id', lesson.id)} | {h.chunk.metadata.get('section', 'Concept')}]: {h.chunk.content}"
            for h in hits
        )
        files_block = "\n".join(
            f"--- {fname} ---\n{code[:1500]}"
            for fname, code in sorted(scrubbed_files.items())
        )
        user_prompt = (
            f"Active Stage: [{lesson.id}] {lesson.title}\n"
            f"Objective: {lesson.objective}\n"
            f"Learner Question: {scrubbed_question}\n"
            f"Latest Diagnostic: {scrubbed_diagnostics or 'None'}\n\n"
            f"Learner Draft Files:\n{files_block or '(none)'}\n\n"
            f"Retrieved Curriculum Concept Chunks:\n{context_block}"
        )
        return system_prompt, user_prompt

    def ask(
        self,
        lesson: LessonSpec,
        question: str,
        files: dict[str, str],
        last_diagnostics: str = "",
    ) -> OracleResponse:
        started = time.perf_counter()

        # Node 1: Pre-flight PII/Secret Scrubbing + Prompt-Injection & Spoiler Guardrail
        scrubbed_question = scrub_pii_and_secrets(question.strip())
        scrubbed_diagnostics = scrub_pii_and_secrets(last_diagnostics.strip())
        scrubbed_files = {name: scrub_pii_and_secrets(code) for name, code in files.items()}

        violation = detect_guardrail_violation(scrubbed_question)
        if violation is not None:
            elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
            provider_label = self._llm_client.provider_name if self._llm_client else "offline-rag"
            return OracleResponse(
                answer=(
                    f"**Socratic Guardrail Triggered (`{violation}`)**\n\n"
                    f"I cannot bypass system guardrails or dump the complete reference solution for `[{lesson.id}]`. "
                    "Share which assertion or concept is blocking you and we'll reason through it step by step."
                ),
                provider=provider_label,
                mode="offline-rag",
                citations=[],
                cited_sources=[],
                reasoning_steps=[f"guardrail_check: blocked ({violation})"],
                guardrail_triggered=True,
                latency_ms=elapsed_ms,
            )

        # Week 6 Optimization: Exact-match TTL cache lookup
        cache_key = self._build_cache_key(
            lesson.id, scrubbed_question, scrubbed_files, scrubbed_diagnostics
        )
        cached = self._cache.get(cache_key)
        if cached is not None:
            elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
            cached_steps = [*cached.reasoning_steps, "ttl_cache: hit"]
            return cached.model_copy(update={"latency_ms": elapsed_ms, "reasoning_steps": cached_steps})

        reasoning_steps = [
            "guardrail_check: passed (PII/secrets scrubbed)",
            "ttl_cache: miss",
        ]

        # Node 2: Initial Hybrid BM25 + Vector RRF Retrieval
        query_seed = scrubbed_question or f"{lesson.title} {scrubbed_diagnostics}"
        hits = self._retrieve_hybrid(query_seed, active_lesson_id=lesson.id, top_k=4)
        reasoning_steps.append(
            f"hybrid_retrieve: Okapi BM25 + dense vector RRF top-{len(hits) or 0}"
        )

        # Node 3 & 4: Document Grader + Adaptive Query Rewriter (Week 7 Agentic pattern)
        rewrote_query = False
        if _needs_adaptive_rewrite(scrubbed_question, hits, scrubbed_diagnostics):
            rewritten_query = self._rewrite_query(
                lesson, scrubbed_question, scrubbed_files, scrubbed_diagnostics
            )
            secondary_hits = self._retrieve_hybrid(
                rewritten_query, active_lesson_id=lesson.id, top_k=4
            )
            hits = _merge_hits(hits, secondary_hits, top_k=4)
            rewrote_query = True
            reasoning_steps.append(
                "document_grader: Triggered adaptive query rewrite with diagnostics & code symbols"
            )
        else:
            reasoning_steps.append("document_grader: High-confidence direct match")

        # Deduplicate citations cleanly by lesson_id while keeping top-scoring snippet
        citations_by_lesson: dict[str, OracleCitation] = {}
        cited_sources: list[str] = []
        for hit in hits:
            lid = hit.chunk.metadata.get("lesson_id", lesson.id)
            title = hit.chunk.metadata.get("title", lesson.title)
            snippet = " ".join(hit.chunk.content.split())[:220]
            if lid not in citations_by_lesson:
                citations_by_lesson[lid] = OracleCitation(
                    lesson_id=lid,
                    title=title,
                    snippet=snippet,
                    score=hit.score,
                )
            if hit.chunk.source not in cited_sources:
                cited_sources.append(hit.chunk.source)

        citations = list(citations_by_lesson.values())
        if not citations:
            citations = [
                OracleCitation(
                    lesson_id=lesson.id,
                    title=lesson.title,
                    snippet=lesson.objective,
                    score=0.5,
                )
            ]
            cited_sources = [f"curriculum/{lesson.module_id}/{lesson.id}/concept.md"]

        # Node 5: Dual-Mode Generation (Live LLM with seamless Offline RAG fallback)
        mode = "offline-rag"
        provider = "offline-rag"
        answer = ""
        fallback_reason: str | None = None

        if self._llm_client is not None:
            sys_prompt, user_prompt = self._build_live_prompts(
                lesson, scrubbed_question, scrubbed_files, scrubbed_diagnostics, hits
            )
            try:
                raw_llm = self._llm_client.generate(sys_prompt, user_prompt)
                valid_cites = verify_citations(raw_llm, set(self._lessons_by_id.keys()))
                answer = raw_llm
                if not valid_cites and citations:
                    answer = f"{raw_llm}\n\n_Grounded reference: `[{citations[0].lesson_id}]`._"
                mode = "live-llm"
                provider = self._llm_client.provider_name
            except Exception as exc:
                fallback_reason = type(exc).__name__

        if not answer:
            answer = self._build_offline_socratic_answer(
                lesson,
                scrubbed_question,
                hits,
                scrubbed_diagnostics,
                rewrote_query=rewrote_query,
                fallback_reason=fallback_reason,
            )

        reasoning_steps.append(f"socratic_generator: {mode} ({provider})")
        elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
        response = OracleResponse(
            answer=answer,
            provider=provider,
            mode=mode,  # type: ignore[arg-type]
            citations=citations,
            cited_sources=cited_sources,
            reasoning_steps=reasoning_steps,
            guardrail_triggered=False,
            latency_ms=elapsed_ms,
        )
        self._cache.put(cache_key, response)
        return response


def build_rag_oracle(
    lessons: list[LessonSpec],
    settings: Settings | None = None,
    llm_client: LlmClient | None = None,
) -> AgenticRagOracle:
    """Factory wiring the Agentic Hybrid RAG Oracle with configured LLM + offline fallback."""
    cfg = settings or Settings()
    resolved_llm = llm_client if llm_client is not None else build_llm_client(cfg)
    return AgenticRagOracle(lessons, llm_client=resolved_llm)
