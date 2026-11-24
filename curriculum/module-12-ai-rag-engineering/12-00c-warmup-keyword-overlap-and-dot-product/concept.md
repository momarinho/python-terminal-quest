## Beginner Warm-Up 3: Keyword Overlap & Vector Dot Product

Hybrid RAG simply mixes **word overlap** + **vector similarity**:

```python
def keyword_overlap(query: str, doc: str) -> float:
    q_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    d_words = set(re.findall(r"[a-z0-9]+", doc.lower()))
    return len(q_words & d_words) / len(q_words) if q_words else 0.0

def dot_product(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))
```

### Challenge
Implement `keyword_overlap` and `dot_product` in `warmup.py`.
