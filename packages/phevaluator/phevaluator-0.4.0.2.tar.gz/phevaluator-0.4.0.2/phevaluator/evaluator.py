from typing import Iterable, Union

from .card import Card
from .evaluator5 import evaluate_5cards
from .evaluator6 import evaluate_6cards
from .evaluator7 import evaluate_7cards
from .evaluator_omaha import evaluate_omaha_cards


def evaluate_cards(*args: Iterable[Union[int, str, Card]]) -> int:
    cards = list(map(Card, args))

    if len(cards) == 5:
        return evaluate_5cards(*cards)

    elif len(cards) == 6:
        return evaluate_6cards(*cards)

    elif len(cards) == 7:
        return evaluate_7cards(*cards)

    elif len(cards) == 9:
        return evaluate_omaha_cards(*cards)
