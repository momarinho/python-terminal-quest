from chunker import DocChunk, chunk_document
from grounding import verify_grounded_answer
from retriever import HybridRetriever


class KeywordEmbedder:
    """Deterministic lightweight 4D feature embedder for offline tests."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for t in texts:
            low = t.lower()
            vectors.append(
                [
                    1.0 if "alembic" in low or "migration" in low else 0.0,
                    1.0 if "selectinload" in low or "eager" in low else 0.0,
                    1.0 if "circuit" in low or "breaker" in low else 0.0,
                    1.0 if "jwt" in low or "rbac" in low else 0.0,
                ]
            )
        return vectors


def test_sentence_overlap_chunking_preserves_boundary_sentence() -> None:
    text = (
        "SQLAlchemy 2.0 uses Mapped annotations. "
        "Use selectinload to prevent N+1 queries on collections. "
        "Alembic manages reversible schema upgrades."
    )
    chunks = chunk_document("orm-guide", text, max_chars=95, overlap_sentences=1)
    assert len(chunks) >= 2
    assert chunks[0].chunk_id == "orm-guide:0"
    assert "selectinload" in chunks[0].text
    assert "selectinload" in chunks[1].text


def test_hybrid_retriever_and_citation_grounding() -> None:
    chunks = [
        DocChunk("doc:0", "doc", "Use selectinload to eliminate N+1 SQL storms in SQLAlchemy."),
        DocChunk("doc:1", "doc", "Configure Alembic migrations for reversible schema changes."),
    ]
    retriever = HybridRetriever(chunks, KeywordEmbedder())
    hits = retriever.search("prevent N+1 queries with selectinload", top_k=1)
    assert len(hits) == 1
    assert hits[0][0].chunk_id == "doc:0"

    good = verify_grounded_answer("Prevent SQLAlchemy N+1 storms using selectinload [doc:0].", chunks)
    assert good.grounded is True
    assert good.cited_ids == ["doc:0"]

    fabricated = verify_grounded_answer("Use selectinload [ghost:99].", chunks)
    assert fabricated.grounded is False
    assert fabricated.invalid_citations == ["ghost:99"]

    unsupported = verify_grounded_answer("Deploy Kubernetes ingress controllers now [doc:0].", chunks)
    assert unsupported.grounded is False
