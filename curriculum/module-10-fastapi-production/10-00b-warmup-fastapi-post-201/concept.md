## Beginner Warm-Up 2: `POST` Bodies & `status_code=201`

Pair `@app.post(..., status_code=201)` with a Pydantic `BaseModel` for clean request validation and `422` errors on bad input:

```python
class NotePayload(BaseModel):
    title: str

@app.post("/notes", status_code=201)
def create_note(payload: NotePayload) -> dict[str, str]:
    return {"title": payload.title.strip()}
```

### Challenge
Fix `@app.post("/notes", status_code=201)` and return `{"title": payload.title.strip()}` in `warmup.py`.
