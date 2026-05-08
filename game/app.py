from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from game.game import (
    build_standard_deck,
    draw_card,
    draw_unique_cards,
    flip_coin,
    flip_coins,
    pick_number,
    random_event,
    rock_paper_scissors,
    roll_custom_dice,
    roll_dice,
)

app = FastAPI(title="Game API", version="1.0.0")

active_deck = build_standard_deck()


class RPSRequest(BaseModel):
    move: str


class GuessRequest(BaseModel):
    guess: int


guess_target = pick_number(1, 100)


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


@app.get("/roll-dice/{sides}")
def roll_dice_sides(sides: int) -> dict:
    try:
        rolls = roll_custom_dice(sides, 1)
        return {"sides": sides, "roll": rolls[0]}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/roll-dice/{sides}/{count}")
def roll_dice_sides_count(sides: int, count: int) -> dict:
    try:
        rolls = roll_custom_dice(sides, count)
        return {"sides": sides, "count": count, "rolls": rolls, "total": sum(rolls)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/coin-flips/{count}")
def coin_flips(count: int) -> dict:
    try:
        flips = flip_coins(count)
        return {"count": count, "flips": flips, "heads": flips.count("Heads"), "tails": flips.count("Tails")}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/draw-cards/{count}")
def draw_cards(count: int) -> dict:
    global active_deck
    try:
        cards = draw_unique_cards(active_deck, count)
        return {"count": count, "cards": cards, "remaining": len(active_deck)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/shuffle-deck")
def shuffle_deck() -> dict:
    global active_deck
    active_deck = build_standard_deck()
    return {"status": "shuffled", "remaining": len(active_deck)}


@app.get("/deck/remaining")
def deck_remaining() -> dict:
    return {"remaining": len(active_deck)}


@app.get("/pick-number")
def random_number(min: int = 1, max: int = 100) -> dict:
    try:
        return {"min": min, "max": max, "number": pick_number(min, max)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/rock-paper-scissors")
def play_rps(body: RPSRequest) -> dict:
    try:
        bot_move, result = rock_paper_scissors(body.move)
        return {"user_move": body.move.lower(), "bot_move": bot_move, "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/guess-number")
def guess_number(body: GuessRequest) -> dict:
    global guess_target
    guess = body.guess
    if guess < guess_target:
        return {"result": "too low"}
    if guess > guess_target:
        return {"result": "too high"}
    guess_target = pick_number(1, 100)
    return {"result": "correct", "next_game": "started"}


@app.get("/random-event")
def get_random_event() -> dict:
    return {"event": random_event()}
