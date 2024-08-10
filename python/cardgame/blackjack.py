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
        self.hand = hand
        self.name = name
        self.bet: int = 0

class Game:
    """States of the game Blackjack:
    Betting -> Dealing -> Players' Turns -> Dealer's Turn
    """
    MIN_BET: int = 2
    MAX_BET: int = 500

    def __init__(self, player_names: list[str]):
        self.deck = cards.Deck.standard_52() * 6
        self.dealer: Player = Player(hand=[], name='Dealer')
        self.players: list[Player] = [Player(hand=[], name=name) for name in player_names]
        self.round: int = 0

    def play(self) -> Player:
        """Begins the game loop. Does not return until the game has finished, returns the winning `Player`
        or `False` if the dealer won.
        """
        # Betting
        print('The game will begin with each player placing their bet. (Minimum $2, maximum $500)')
        for player in self.players:
            while True:
                bet = input(f'{player.name}, place your bet: ').strip(' $')
                try:
                    bet = int(bet)
                except ValueError:
                    print('Not a number. Please try again.')
                    continue
                if bet not in range(self.MIN_BET, self.MAX_BET + 1):
                    print('Bet must be between $2 and $500. Please try again.')
                    continue
                player.bet = bet
                break
        print('Bets have been placed:', ', '.join([f'{player.name} with ${player.bet}' for player in self.players]))

        # Dealing
        print('Shuffling and dealing...')
        self.deck.shuffle()
        self.dealer.hand.append(*self.deck.draw(2))
        for player in self.players:
            player.hand.append(*self.deck.draw(2))

        # Players' Turns
        print('Players\' hands are as follows:')
        '\n'.join([f'{player.name}: {player.hand}'])


if __name__ == '__main__':
    winner = Game(['1', '2']).play()
    print(winner)
