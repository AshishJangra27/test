from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chatbot.chatbot import funny_answer, sarcastic_answer, serious_answer


app = FastAPI(title="Chatbot API", version="1.0.0")


class MessageRequest(BaseModel):
    message: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/funny")
def reply_funny(body: MessageRequest) -> dict:
    try:
        return {"reply": funny_answer(body.message)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/serious")
def reply_serious(body: MessageRequest) -> dict:
    try:
        return {"reply": serious_answer(body.message)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/sarcastic")
def reply_sarcastic(body: MessageRequest) -> dict:
    try:
        return {"reply": sarcastic_answer(body.message)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
