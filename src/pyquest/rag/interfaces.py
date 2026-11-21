from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pyquest.domain.models import LessonSpec, OracleResponse


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source: str
    content: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoredChunk:
    chunk: DocumentChunk
    score: float


class EmbeddingClient(ABC):
    """Pluggable embedding model interface for RAG indexing and retrieval."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate dense embedding vectors for a batch of texts."""


class VectorStore(ABC):
    """Pluggable vector storage interface (e.g. sqlite-vec, pgvector, Qdrant)."""

    @abstractmethod
    def upsert(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        """Persist document chunks alongside their embedding vectors."""

    @abstractmethod
    def query(
        self,
        embedding: list[float],
        *,
        top_k: int = 5,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[ScoredChunk]:
        """Return the top-k most similar chunks."""


class LlmClient(ABC):
    """Pluggable LLM completion interface (Gemini, Ollama, OpenAI-compatible)."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a grounded response from the configured LLM."""


class RagPipeline(ABC):
    """Top-level RAG Oracle pipeline interface."""

    @abstractmethod
    def ask(
        self,
        lesson: LessonSpec,
        question: str,
        files: dict[str, str],
        last_diagnostics: str = "",
    ) -> OracleResponse:
        """Answer a learner's question grounded in lesson context without spoiling the solution."""
