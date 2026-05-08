import numpy as np

rng = np.random.default_rng()


def flip_coin() -> str:
    """Return one random side of a coin: Heads or Tails."""
    return "Heads" if int(rng.integers(0, 2)) == 0 else "Tails"


def draw_card() -> str:
    """Pick one random card from a standard 52-card deck."""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return f"{ranks[int(rng.integers(0, len(ranks)))]} of {suits[int(rng.integers(0, len(suits)))]}"


def roll_dice() -> int:
    """Roll one 6-sided die."""
    return int(rng.integers(1, 7))


def roll_custom_dice(sides: int, count: int = 1) -> list[int]:
    if sides < 2:
        raise ValueError("sides must be >= 2")
    if count < 1:
        raise ValueError("count must be >= 1")
    return [int(x) for x in rng.integers(1, sides + 1, size=count)]


def flip_coins(count: int) -> list[str]:
    if count < 1:
        raise ValueError("count must be >= 1")
    return [flip_coin() for _ in range(count)]


def build_standard_deck() -> list[str]:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]


def draw_unique_cards(deck: list[str], count: int) -> list[str]:
    if count < 1:
        raise ValueError("count must be >= 1")
    if count > len(deck):
        raise ValueError("not enough cards in deck")
    rng.shuffle(deck)
    cards = deck[:count]
    del deck[:count]
    return cards


def pick_number(min_value: int, max_value: int) -> int:
    if min_value > max_value:
        raise ValueError("min must be <= max")
    return int(rng.integers(min_value, max_value + 1))


def rock_paper_scissors(user_move: str) -> tuple[str, str]:
    valid_moves = ["rock", "paper", "scissors"]
    move = user_move.lower().strip()
    if move not in valid_moves:
        raise ValueError("move must be one of: rock, paper, scissors")
    bot_move = valid_moves[int(rng.integers(0, 3))]
    if move == bot_move:
        result = "draw"
    elif (move == "rock" and bot_move == "scissors") or (move == "paper" and bot_move == "rock") or (move == "scissors" and bot_move == "paper"):
        result = "win"
    else:
        result = "lose"
    return bot_move, result


def random_event() -> str:
    events = ["Common loot", "Nothing happens", "Find a clue", "Minor trap", "Rare treasure"]
    probabilities = [0.35, 0.25, 0.20, 0.15, 0.05]
    return str(rng.choice(events, p=probabilities))
