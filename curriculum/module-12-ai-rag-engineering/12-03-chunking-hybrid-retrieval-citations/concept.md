# Chunking, Hybrid Retrieval & Verified Grounding Citations

Naive fixed-character splitting cuts sentences in half and breaks semantic context. Dense embeddings alone also miss exact error codes (`HTTP_429`, `selectinload`), while lexical search alone misses synonyms.

## Three Pillars of Reliable RAG

1. **Overlapping Sentence Chunking (`chunker.py`):** Group complete sentences up to `max_chars` and retain `overlap_sentences` trailing sentences in the next chunk so boundary facts are never orphaned.
2. **Hybrid Scoring (`retriever.py`):** Combine vector cosine similarity with normalized lexical keyword overlap (`alpha * cosine + (1 - alpha) * lexical`).
3. **Post-Generation Citation Verification (`grounding.py`):** Parse inline citations like `[doc-1:0]`:
   - Reject answers with zero valid citations or unknown `[fake-id]` tags.
   - Verify non-trivial content word overlap between the answer and the cited chunks.

```python
import math

def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    denom = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / denom if denom > 0 else 0.0
```
