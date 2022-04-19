from dataclasses import dataclass
import functools


@dataclass
class PlayingCard:
    """
    Examples
    -----------
    card = PlayingCard("ace", "black")
    """

    rank: str
    suit: str


if __name__ == "__main__":
    1
