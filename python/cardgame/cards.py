import random
import re
from abc import ABC
from itertools import chain
from textwrap import dedent
from typing import (Callable, Generic, Optional, Self, Sequence, SupportsIndex, Type,
                    TypeVar, overload)

class BaseCard(ABC):
    """The base of any playing card. Meant for use in subclasses, not to be used on its own.

    When subclassing `BaseCard`, you must define the `SUITS`, `NUMERAL_VALUES`, and `FACE_VALUES` attributes. `VALUES` is automatically created
    by combining the two.
    """

    SUITS: list[str]
    """Valid suits for this type of card. e.g. `['hearts', 'diamonds', 'spades', 'clubs']` for French-suited cards, or
    `['red', 'blue', 'green', 'yellow', 'wild']` for something like UNO cards."""

    NUMERAL_VALUES: list[int] = []
    """A list of numeral cards for this card type."""
    NAMED_VALUES: dict[str, int] = {}
    """A dictionary of non-numeral card names and their associated values."""
    VALUES: dict[int | str, int] = dict(chain.from_iterable(d.items() for d in ({n:n for n in NUMERAL_VALUES}, NAMED_VALUES)))
    """Valid values of this card, either an integer for regular numbers or a string for face cards.
    Automatically created from combining `NUMERAL_VALUES` and `FACE_VALUES`
    """

    def __init__(self, suit: str, value: int | str, face_up: bool=True):
        """
        @suit: The suit name of this card. Must be a valid suit for this type of card.
        @value: Number value, or a string. Must be a valid value for this type of card.
        @face_up: If `face_up` is `False`, the card's suit and value will be hidden in `__str__()` and `visual()`,
            but both of these are still accessible by the `suit` and `value`. Defaults to `True`.
        """
        if suit not in self.SUITS:
            raise ValueError(f'Invalid card suit ({suit!r}); valid suits: {', '.join(self.SUITS)}')
        self.suit = suit

        if value not in self.VALUES:
            raise ValueError(f'Invalid card value ({value!r}); valid options: {', '.join(map(str, self.VALUES))}')
        self.value = value
        """The value of this card as it would be shown physically. Use the `score` attribute to get what this card is actually worth in points."""
        self.score: int = self.VALUES[self.value]
        """The worth of this card in points. For the value that would be shown on a physical card, use `value`."""

        self.face_up = face_up
        """Whether this card is currently facing up or not.
        If `False`, any methods that show its value like `__str__` and `visual` will replace the card's suit and value with question marks.
        """

    def __repr__(self) -> str:
        return f'Card(suit={self.suit}, value={self.value}, face_up={self.face_up})'

    def __str__(self) -> str:
        return f'{str(self.value).title()} of {self.suit.title()}' if self.face_up else '??? of ???'

    def visual(self) -> str:
        """Returns a string formatting this card into a basic ASCII visual representation."""
        return dedent(f"""\
            |-----|
            |{(value_display := self.value if isinstance(self.value, int) else self.value[0].upper()):<5}|
            |  {self.suit[0].upper()}  |
            |{value_display:>5}|
            |-----|
            """ if self.face_up else """\
            |-----|
            |? ? ?|
            |? ? ?|
            |? ? ?|
            |-----|
            """).rstrip('\n')

    @staticmethod
    def visual_line(cards: Sequence['BaseCard']) -> str:
        """Returns a string formatting a collection of cards to be displayed in a horizontal line."""
        return '\n'.join([' '.join([card_img.split('\n')[n] for card_img in [card.visual() for card in cards]]) for n in range(5)])

    @staticmethod
    def flip(cards: Sequence['BaseCard'], face_up: Optional[bool]=None) -> None:
        """Changes the `face_up` attribute of every card in the given sequence.
            Sets to `face_up` if a value is specified, otherwise sets to the opposite of each individual card's `face_up` attribute.
        """
        for card in cards:
            card.face_up = (face_up) or (not card.face_up)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a `Card` from a string, formatted as `"[value] of [suit]"`, e.g. `2 of hearts`, `ace of spades`, `7 of diamonds`"""
        if matches := re.findall(r"(\d|\w+) of (\w+)", string, flags=re.IGNORECASE):
            return cls(*matches[0])
        else:
            raise ValueError(f'Invalid string format for {cls.__name__}.from_string()')

class FrenchSuitedCard(BaseCard):
    """A basic French-suited playing card."""
    SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
    NUMERAL_VALUES = [*range(2, 11)]
    FACE_VALUES = {'ace': 1, 'jack': 10, 'queen': 10, 'king': 10}

T_CARD = TypeVar('T_CARD', bound=BaseCard)

class Deck(Generic[T_CARD], list):
    """Represents a deck of cards as a `list` of `BaseCard`-derived objects."""
    def __init__(self, cards: Optional[list[T_CARD]]=None):
        if cards:
            super().__init__(cards)
        else:
            super().__init__()

    @overload
    def __getitem__(self, key: int) -> T_CARD: ...
    @overload
    def __getitem__(self, key: slice) -> 'Deck[T_CARD]': ...

    def __getitem__(self, key: int | slice) -> T_CARD | 'Deck[T_CARD]':
        if isinstance(key, slice):
            return Deck(list.__getitem__(self, key))
        else:
            return list.__getitem__(self, key)

    def __mul__(self, value: SupportsIndex):
        return Deck(list.__mul__(self, value))

    def __str__(self) -> str:
        return f'{', '.join(map(str, self))}'

    def point_total(self, map_func: Optional[Callable]=None) -> int:
        """Returns the total score of all cards in this deck. Score of each card can be altered with a supplied function
        that will be passed into `map()`. If a function is not given, `map()` is not used and the sum is calculated from
        a simple generator.
        @map_func: A function to apply to each card value before returning its score.
        """
        card_points: list[int] = [card.score for card in self]
        return sum(map(map_func, card_points) if map_func else card_points)

    def shuffle(self) -> None:
        """Shuffles this deck in-place."""
        random.shuffle(self)

    def draw(self, amount: int=1, face_up: Optional[bool]=None) -> list[T_CARD]:
        """Removes a given amount of `Card`s from the deck, and always returns them in a list, even if `amount` is 1.
        @face_up: Sets the `face_up` attribute of the drawn cards before popping and returning them.
            If left `None`, the cards are drawn and given with whatever `face_up` state they were already in.
        """
        if (amount < 1):
            raise ValueError('amount cannot be less than 1')
        if (amount > len(self)):
            raise ValueError('amount cannot be greater than the deck\'s size')
        cards: list[T_CARD] = []
        for i in range(amount): # pylint: disable=unused-variable
            card: T_CARD = self.pop(random.randint(0, len(self)))
            card.face_up = face_up or card.face_up
            cards.append(card)
        return cards

    def visual(self) -> str:
        """Returns a string formatting this deck into a horizontal line of cards."""
        return BaseCard.visual_line(self)

    @classmethod
    def standard_52(cls: Type['Deck[FrenchSuitedCard]']) -> 'Deck[FrenchSuitedCard]':
        """Creates a standard 52-card deck, containing the numbers 2 through 10 of spades, hearts, clubs, and diamonds, as well as
            one jack, queen, king, and ace for each suit.
        """
        return cls([FrenchSuitedCard(suit, value) for value in FrenchSuitedCard.VALUES for suit in FrenchSuitedCard.SUITS])
