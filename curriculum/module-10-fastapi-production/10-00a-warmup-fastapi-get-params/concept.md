## Beginner Warm-Up 1: FastAPI `GET` Routes & Params

FastAPI automatically validates path parameters (`/items/{item_id}`) and query parameters (`?verbose=true`) from function type annotations:

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/items/{item_id}")
def read_item(item_id: int, tag: str = "default") -> dict[str, object]:
    return {"item_id": item_id, "tag": tag}
```

### Challenge
Open `warmup.py` and implement `/health` and `/items/{item_id}`.
