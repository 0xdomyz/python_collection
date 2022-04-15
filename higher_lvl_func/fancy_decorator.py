from dataclasses import dataclass
import math


@dataclass
class PlayingCard:
    rank: str
    suit: str


if __name__ == "__main__":
    card = PlayingCard("ace", "black")
