## Concept: Warm-Up & Quick Syntax Reveal (Module 10)

Before designing layered monoliths, RFC 7807 errors, and JWT RBAC, warm up with FastAPI's 3 signature idioms!

### Pattern Reveal #1 — `GET` Route with `Depends(...)`
```python
def get_app_version() -> str:
    return "1.0.0"

@app.get("/ping")
def ping(version: str = Depends(get_app_version)) -> dict[str, str]:
    return {"status": "pong", "version": version}
```

### Pattern Reveal #2 — `POST` Route with Explicit `status_code=201`
```python
class EchoPayload(BaseModel):
    message: str

@app.post("/echo", status_code=201)
def echo_item(payload: EchoPayload) -> dict[str, str]:
    return {"echo": payload.message.strip()}
```

### Challenge
Open `warmup.py` and wire `ping` and `echo_item` on the `app` instance.
