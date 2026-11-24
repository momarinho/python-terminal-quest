from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "todo"}


@app.get("/items/{item_id}")
def read_item(item_id: int, tag: str = "default") -> dict[str, object]:
    return {}
