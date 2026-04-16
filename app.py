from fastapi import FastAPI

from chatbot.app import app as chatbot_app
from game.app import app as game_app


app = FastAPI(title="Unified API", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "services": ["game", "chatbot"]}


app.mount("/game", game_app)
app.mount("/chatbot", chatbot_app)
