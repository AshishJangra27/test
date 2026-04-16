from fastapi import FastAPI
from game.game import draw_card, flip_coin, roll_dice

app = FastAPI(title="Game API", version="1.0.0")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/head-or-tail")
def head_or_tail() -> dict:
    return {"result": flip_coin()}


@app.get("/roll-dice")
def roll_single_dice() -> dict:
    return {"roll": roll_dice()}


@app.get("/draw-card")
def draw_random_card() -> dict:
    return {"card": draw_card()}