import random
import re
from enum import Enum
from typing import Iterable, Optional, Self, SupportsIndex


class BaseCard:
    """The base of any playing card. Meant for use in subclasses, not to be used on its own."""

    SUITS: list[str]
    """Valid suits for this type of card. e.g. `['hearts', 'diamonds', 'spades', 'clubs']` for French-suited cards, or
    `['red', 'blue', 'green', 'yellow', 'wild']` for something like UNO cards."""
    VALUES: list[int | str]
    """Valid values of this card, can be integers for actual numbers or strings for things like face cards.
    The order of this list can be used for comparisons between two instances of this class, for example:
    ```
    # NewCard.__init__
    VALUES = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']
    # Later outside of class
    my_card = NewCard('spades', 'ace')
    your_card = NewCard('clubs', 4)
    print(my_card > your_card) # Output: False
    ```
    Default less-than and greater-than behavior can be used by simply referencing the card's value directly (`my_card.value`)
    """

    def __init__(self, suit: str, value: int | str):
        """
        @suit: The first letter of this card's suit: `h` for hearts, `d` for diamonds, etc.
            The full name can also be used; only the first letter of the given string is used
        @value: Number value, or a string if an Ace or face card.\
            Valid strings are `ace`, `jack`, `queen`, and `king`
        """
        suit = suit[0]
        if suit not in self.SUITS:
            raise ValueError(f'Invalid suit given; valid suits: {', '.join(self.SUITS)}')
        self.suit = suit

        if value not in self.VALUES:
            raise ValueError(f'Invalid card value; valid options: {', '.join(self.VALUES)}')
        self.value = value

    def __repr__(self) -> str:
        return f'Card(suit={self.suit}, value={self.value})'

    def __str__(self) -> str:
        return f'{str(self.value).title()} of {self.suit_names[self.suit].title()}'

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a `Card` from a string, formatted as `2 of hearts`, `ace of spades`, `7 of diamonds`, etc."""
        if matches := re.findall(r"(\d|\w+) of (\w+)", string, flags=re.IGNORECASE):
            return cls(*matches[0])
        else:
            raise ValueError('Invalid string format for Card.from_string()')

class FrenchSuitedCard:
    """A basic playing card. Can be one of four suits - (h)earts, (d)iamonds, (s)pades, or (c)lubs -
        and must be given a value of either 2 - 10, or the name of a face card.
    Since many card games use differing values for aces and face cards, their value is not hard-coded into
    the card object, and instead left as a string for the game to interpret as it sees fit.
    """
    suit_names: dict[str, str] = {'h': 'hearts', 'd': 'diamonds', 's': 'spades', 'c': 'clubs'}
    valid_value_ints: list[int] = [*range(2, 11)]
    valid_value_strings: list[str] = ['ace', 'jack', 'queen', 'king']

    def __init__(self, suit: str, value: int | str):
        """
        @suit: The first letter of this card's suit: `h` for hearts, `d` for diamonds, etc.
            The full name can also be used; only the first letter of the given string is used
        @value: Number value, or a string if an Ace or face card.\
            Valid strings are `ace`, `jack`, `queen`, and `king`
        """
        suit = suit[0]
        if suit not in self.suit_names:
            raise ValueError(f'Invalid suit given; valid suits: {', '.join(self.suit_names.keys())}')
        self.suit = suit

        if value not in self.valid_value_ints + self.valid_value_strings:
            raise ValueError(f'card value must be an integer between 2 and 10, or one of these strings: {', '.join(self.valid_value_strings)}')
        self.value = value

    def __repr__(self) -> str:
        return f'Card(suit={self.suit}, value={self.value})'

    def __str__(self) -> str:
        return f'{str(self.value).title()} of {self.suit_names[self.suit].title()}'

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a `Card` from a string, formatted as `2 of hearts`, `ace of spades`, `7 of diamonds`, etc."""
        if matches := re.findall(r"(\d|\w+) of (\w+)", string, flags=re.IGNORECASE):
            return cls(*matches[0])
        else:
            raise ValueError('Invalid string format for Card.from_string()')

class Deck(list):
    """Represents a deck of cards as a `list` of `Card` objects."""
    def __init__(self, cards: Optional[Iterable[FrenchSuitedCard]]=None):
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

    def draw(self, amount: int=1) -> FrenchSuitedCard | list[FrenchSuitedCard]:
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
        return cls([FrenchSuitedCard(suit, value) for value in [*range(2, 11), 'ace', 'jack', 'queen', 'king'] for suit in ['h', 'd', 's', 'c']])
