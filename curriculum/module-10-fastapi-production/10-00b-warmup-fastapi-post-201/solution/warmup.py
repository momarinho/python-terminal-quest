from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class NotePayload(BaseModel):
    title: str


@app.post("/notes", status_code=201)
def create_note(payload: NotePayload) -> dict[str, str]:
    return {"title": payload.title.strip()}
