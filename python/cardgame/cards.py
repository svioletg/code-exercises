import random
import re
from typing import Iterable, Optional, Self, SupportsIndex


class BaseCard:
    """The base of any playing card. Meant for use in subclasses, not to be used on its own."""

    SUITS: list[str]
    """Valid suits for this type of card. e.g. `['hearts', 'diamonds', 'spades', 'clubs']` for French-suited cards, or
    `['red', 'blue', 'green', 'yellow', 'wild']` for something like UNO cards."""
    VALUES: list[int | str]
    """Valid values of this card, can be integers for actual numbers or strings for things like face cards.

    The order of this list can be used for comparisons between two instances of this class.
    Default less-than and greater-than behavior can be used by simply referencing the card's value directly (`my_card.value`)
    """

    def __init__(self, suit: str, value: int | str):
        """
        @suit: The first letter of this card's suit: `h` for hearts, `d` for diamonds, etc.
            The full name can also be used; only the first letter of the given string is used
        @value: Number value, or a string if an Ace or face card.\
            Valid strings are `ace`, `jack`, `queen`, and `king`
        """
        if suit not in self.SUITS:
            raise ValueError(f'Invalid card suit ({suit!r}); valid suits: {', '.join(self.SUITS)}')
        self.suit = suit

        if value not in self.VALUES:
            raise ValueError(f'Invalid card value ({value!r}); valid options: {', '.join(map(str, self.VALUES))}')
        self.value = value

    def __repr__(self) -> str:
        return f'Card(suit={self.suit}, value={self.value})'

    def __str__(self) -> str:
        return f'{str(self.value).title()} of {self.suit.title()}'

    def show(self) -> str:
        """Returns a string formatting this card into a basic ASCII visual representation."""
        return f"""\
|---|
|{(value_display := self.value if isinstance(self.value, int) else self.value[0].upper()):<2} |
| {self.suit[0].upper()} |
| {value_display:>2}|
|---|\
"""

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a `Card` from a string, formatted as `2 of hearts`, `ace of spades`, `7 of diamonds`, etc."""
        if matches := re.findall(r"(\d|\w+) of (\w+)", string, flags=re.IGNORECASE):
            return cls(*matches[0])
        else:
            raise ValueError('Invalid string format for Card.from_string()')

class FrenchSuitedCard(BaseCard):
    """A basic French-suited playing card."""
    SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
    VALUES = ['ace', *range(2, 11), 'jack', 'queen', 'king']

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a `Card` from a string, formatted as `2 of hearts`, `ace of spades`, `7 of diamonds`, etc."""
        if matches := re.findall(r"(\d|\w+) of (\w+)", string, flags=re.IGNORECASE):
            return cls(*matches[0])
        else:
            raise ValueError('Invalid string format for Card.from_string()')

class Deck(list):
    """Represents a deck of cards as a `list` of `Card` objects."""
    def __init__(self, cards: Optional[Iterable[BaseCard]]=None):
        super().__init__(cards or [])

    def __getitem__(self, key: SupportsIndex | slice):
        if isinstance(key, slice):
            return Deck(list.__getitem__(self, key))
        else:
            return list.__getitem__(self, key)

    def __mul__(self, value: SupportsIndex):
        return Deck(list.__mul__(self, value))

    def __str__(self) -> str:
        return f'Deck: {', '.join(map(str, self))}'

    def shuffle(self) -> None:
        """Shuffles this deck in-place."""
        random.shuffle(self)

    def draw(self, amount: int=1) -> BaseCard | list[BaseCard]:
        """Removes a given amount of `Card`s from the deck, and returns them in a list if `amount` is more than 1.
        If `amount` is 1, which is its default value, a single `Card` is returned. `amount` cannot be lower than 1 or
        greater than the deck's size.
        """
        if (amount < 1):
            raise ValueError('amount cannot be less than 1')
        if (amount > len(self)):
            raise ValueError('amount cannot be greater than the deck\'s size')
        return [self.pop(random.randint(0, len(self))) for i in range(amount)] if amount > 1 else self.pop(random.randint(0, len(self)))

    @classmethod
    def standard_52(cls) -> Self:
        """Creates a standard 52-card deck, containing the numbers 2 through 10 of spades, hearts, clubs, and diamonds, as well as
            one jack, queen, king, and ace for each suit.
        """
        return cls([FrenchSuitedCard(suit, value) for value in FrenchSuitedCard.VALUES for suit in FrenchSuitedCard.SUITS])
