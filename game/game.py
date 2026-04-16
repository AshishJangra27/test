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