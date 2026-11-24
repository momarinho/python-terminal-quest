from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, tag: str = "default") -> dict[str, object]:
    return {"item_id": item_id, "tag": tag}
