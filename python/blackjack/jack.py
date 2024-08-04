import random
from typing import Iterable, Optional, Self

class Card:
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
        @value: Number value, or a string if an Ace or face card.\
            Valid strings are `ace`, `jack`, `queen`, and `king`
        """
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

class Deck(list):
    """Represents a deck of cards as a `list` of `Card` objects."""
    def __init__(self, cards: Optional[Iterable[Card]]=None):
        super().__init__(cards or [])

    def shuffle(self):
        """Shuffles this deck in-place."""
        random.shuffle(self)

    @classmethod
    def standard_52(cls) -> Self:
        """Creates a standard 52-card deck, containing the numbers 2 through 10 of spades, hearts, clubs, and diamonds, as well as
            one jack, queen, king, and ace for each suit.
        """
        return cls([Card(suit, value) for value in [*range(2, 11), 'ace', 'jack', 'queen', 'king'] for suit in ['h', 'd', 's', 'c']])
