"""A CLI-based game of the card game Blackjack.

Rules based on Bicycle's page for Blackjack: https://bicyclecards.com/how-to-play/blackjack

Some rules that only serve in-person gameplay, like including a blank card to indicate reshuffling, are omitted,
since they will not be relevant a game without a real dealer.

The game involves one dealer and one or more players. A combined six standard 52-card decks are used, shuffled together.
The objective is to beat the dealer by having cards totalling as close to 21 as possible, without going over.

Face cards are worth 10, and aces are either 1 or 11, whichever is most beneficial to the player at the time.
"""

from typing import Optional
import cards

class Player:
    def __init__(self, hand: list[cards.FrenchSuitedCard], name: Optional[str]='Player'):
        self.name = name
        self.hand = hand

class Game:
    """States of the game Blackjack:
    Betting -> Dealing -> 
    """
    DEALER: int = 0
    PLAYER: int = 1

    def __init__(self, player_names: list[str]):
        self.deck = cards.Deck.standard_52() * 6
        self.players: list[Player] = [Player(hand=[], name=name) for name in player_names]
        self.turn: int = self.DEALER
        self.round: int = 0

if __name__ == '__main__':
    # Enter CLI loop
    pass
