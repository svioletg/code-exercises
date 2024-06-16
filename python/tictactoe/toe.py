"""A game of Tic-Tac-Toe created as an exercise."""

import itertools
import random
import re
from copy import deepcopy
from string import ascii_lowercase
from time import sleep
from typing import Optional, Self, cast


class GameBoard:
    """A Tic-Tac-Toe board that handles anything strictly related to itself,
    like placing down markers or checking for a winning line.
    Does not handle things like player turns.
    """
    def __init__(self, size: int=3, players: Optional[list[str]]=None):
        """
        @size: Used for both rows and columns, board will always be square.
        @players: List of single-character strings used to represent each value that can be placed on the board.\
            'x' and 'o' by default.
        """
        self.size = size
        if self.size < 2:
            raise ValueError('Board size must be greater than 1.')

        self.mark_to_num: dict[str, int]
        self.num_to_mark: dict[int, str]
        self._set_players(players)

        self.empty_board: list[list[str]] = [[' ' for _ in range(size)] for _ in range(size)]
        self.board = deepcopy(self.empty_board)
        self._winning_lines = self._get_winning_lines()

    def __repr__(self) -> str:
        col_header: str = '  ' + ''.join([f'  {n} ' for n in range(self.size)])
        edge_bar = '  =' + ('====' * self.size)
        separator = '  |' + ('---|' * self.size)

        rows = [col_header, edge_bar]
        for row in range(self.size):
            row_str = ascii_lowercase[row] + ' |'
            for col in range(self.size):
                row_str += f' {self.board[row][col]} |'
            rows.append(row_str)
            rows.append(separator)
        rows[-1] = edge_bar
        return '\n'.join(rows)

    def __getitem__(self, item: int) -> list[str]:
        return self.board[item]

    def _set_players(self, players: Optional[list[str]]) -> None:
        players = players or ['x', 'o']
        if any((len(mark) > 1) or (mark.strip() == '') for mark in players):
            raise ValueError('Player marker strings can only be a single non-whitespace character each.')
        self.mark_to_num: dict[str, int] = {mark:n + 1 for n, mark in enumerate(players)}
        self.num_to_mark: dict[int, str] = {n:mark for mark, n in self.mark_to_num.items()}

    def _get_winning_lines(self) -> list[list[tuple[int, int]]]:
        prod = list(itertools.product(range(self.size), range(self.size)))

        h_lines: list[list[tuple[int, int]]] = []
        for n in itertools.count(0, self.size):
            if len(line := prod[n:n + self.size]) == self.size:
                h_lines.append(line)
                n += self.size
            else:
                break

        v_lines: list[list[tuple[int, int]]] = []
        for n, _ in enumerate(prod[0:self.size]):
            line = []
            while n < len(prod):
                line.append(prod[n])
                n += self.size
            v_lines.append(line)

        diagonal_right: list[tuple[int, int]] = [(n, n) for n in range(self.size)]
        diagonal_left: list[tuple[int, int]] = [(self.size - 1, 0)]
        while (last := diagonal_left[-1]) != (0, self.size - 1):
            diagonal_left.append((last[0] - 1, last[1] + 1))

        return h_lines + v_lines + [diagonal_right] + [diagonal_left]

    def _marker_from_player(self, marker_or_player: Optional[str | int]):
        """Returns a player's marker string if an integer is given, or the marker itself if a string is given."""
        if not isinstance(marker_or_player, (int, str)):
            raise TypeError(f'marker_or_player must be an integer or string: got {type(marker_or_player)} instead')

        if isinstance(marker_or_player, int):
            marker = self.num_to_mark[marker_or_player]
        elif isinstance(marker_or_player, str):
            marker = marker_or_player

        if marker not in self.mark_to_num:
            raise ValueError(f'Invalid player marker: {marker!r}')

        return marker

    def reset(self) -> None:
        """Resets the game board to a clear state."""
        self.board = deepcopy(self.empty_board)

    def get(self, row: int, col: int) -> str:
        """Returns the value of a board located at the given position."""
        return self.board[row][col]

    def str_to_point(self, point_string: str) -> tuple[int, int]:
        """Translates a valid point string (`"a3"`, `"3a"`, `"a 3"`, `"3 a"`, `"a, 3"`, `"3, a"`) into its equivalent
        tuple of integers.
        
        e.g. `"a3"` -> `(0, 3)`
        """
        letter_reg: list[str] = re.findall(r"([a-z])", point_string)
        num_reg: list[str] = re.findall(r"(\d+)", point_string)
        if len(letter_reg + num_reg) != 2:
            raise ValueError('Point string must contain 2 characters, either together, separated by space, or separated by comma.')

        return (ascii_lowercase.index(letter_reg[0]), int(num_reg[0]))

    def get_board_string(self) -> str:
        """Returns a special string format of the current game board, which can be used to recreate the same board from later."""
        game_string: str = f'P[{','.join(self.mark_to_num.keys())}]='
        for row in self.board:
            game_string += 'R[' + (','.join(['0' if mark == ' ' else str(self.mark_to_num[mark]) for mark in row])) + ']'

        return game_string

    def load_board_string(self, board_string: str) -> None:
        """Replaces the current board state with the given board string."""
        self._set_players(re.findall(r"P\[(.*?)\]", board_string)[0].split(','))
        print(self.num_to_mark)
        self.board = [[' ' if n == '0' else self.num_to_mark[int(n)] for n in cast(list[str], r.split(','))] \
            for r in re.findall(r"R\[(.*?)\]", board_string)]

    def find_occupied(self, marker_or_player: Optional[str | int] = None) -> list[tuple[int, int]]:
        """Looks for spaces on the board that are occupied by a marker, either a specific one, or any marker at all.

        @marker_or_player: Either the index of a player, or the player's associated string itself.\
            If none is provided, will return any occupied spaces regardless of marker type.
        """
        marker = self._marker_from_player(marker_or_player) if marker_or_player else None

        occupied: list[tuple[int, int]] = []

        for row, col in itertools.product(range(self.size), range(self.size)):
            if ((self.board[row][col] == marker) if marker else (self.board[row][col] != ' ')):
                occupied.append((row, col))

        return occupied

    def check_for_win(self) -> list[tuple[int, int]] | bool:
        """Checks if any winning line is found.
        A winning line must be a straight line (either horizontal or vertical) or a diagonal line.
        If one is found, the line is returned, otherwise False is returned.
        """
        for line in self._winning_lines:
            last_mark = None
            is_winner = True
            for point in line:
                if not last_mark:
                    last_mark = self.get(*point)
                    continue
                if last_mark != self.get(*point):
                    is_winner = False
                    break
            if is_winner and (last_mark != ' '):
                return line
        return False

    def place_at(self, row: int, col: int, marker_or_player: int | str) -> None:
        """Attempts to place something at the given position, raising an exception if a value already exists.
        An exception is also raised if the given marker is not a valid player.

        @marker_or_player: Either the index of a player, or the player's associated string itself.
        """
        marker = self._marker_from_player(marker_or_player)

        if (existing := self.board[row][col]) != ' ':
            raise ValueError(f'Something is already placed here: {existing}')
        self.board[row][col] = marker

    @classmethod
    def random_board(cls, *args, **kwargs) -> Self:
        """Generates a randomly-filled board with the given size and players."""
        board = cls(*args, **kwargs)
        size = board.size
        for _ in range(random.randint(0, size*size)):
            while True:
                try:
                    board.place_at(
                        random.randint(0, size - 1),
                        random.randint(0, size - 1),
                        random.choice(list(board.mark_to_num.keys()))
                        )
                    break
                except ValueError:
                    continue
        return board

    @classmethod
    def winning_board(cls, winner: Optional[int | str]=None, **kwargs) -> Self:
        """Generates a board with a randomly chosen winning line, with an optionally specified winner.
        If `winner` is not set, a random winning player will be chosen from the given list.
        """
        board = cls(**kwargs)
        winning_player = winner or random.choice(list(board.mark_to_num.keys()))
        for point in random.choice(board._winning_lines):
            board.place_at(*point, winning_player)
        return board

    @classmethod
    def from_string(cls, board_string: str, **kwargs) -> Self:
        """Returns a new board created from the given board string."""
        board = cls(**kwargs)
        board.load_board_string(board_string)
        return board

def play_game(game_rounds: int, **kwargs):
    """Initiates a game of Tic-Tac-Toe. Repeats the game for the given number of rounds,
    keeping track of the winners of each one, printing and returning the results once rounds are exhausted.

    @game_rounds: Any whole number that is more than 0.
    @board_size: Size of the board to play off of.
    """
    game_results: dict[int, str] = {}
    for game_round in range(1, game_rounds + 1):
        board = GameBoard(**kwargs)
        winner = 'draw'
        game_turns = 1
        print(f'\n===== Round {game_round} of {game_rounds} =====')
        for player in itertools.cycle(board.mark_to_num):
            print(f'\nTurn {game_turns}: It\'s {player}\'s turn.')
            print(board)
            while True:
                try:
                    board.place_at(*board.str_to_point(input('Place where? ')), player)
                    break
                except Exception as e:
                    print(e)
                    continue
            if board.check_for_win():
                winner = player
                break
            game_turns += 1
        game_results[game_round] = winner
        if winner != 'draw':
            print(f'{winner} wins round {game_round}!')
            print(board)
            sleep(1)
        else:
            print(f'Round {game_round} is a draw!')
            print(board)
            sleep(1)

    return game_results

def main():
    while True:
        try:
            board_size = int(input('Board size? '))
            if board_size < 2:
                print('Board can\'t be smaller than 1.')
                continue
        except ValueError:
            print('Please give a single whole number.')
            continue
        try:
            rounds = int(input('How many rounds? '))
            if rounds < 1:
                print('Can\'t have less than one round.')
                continue
        except ValueError:
            print('Please give a single whole number.')
            continue
        players_input = input('Write out your players, separated by comma. e.g., "x, o"\n'+
            'Your "players" are a list of single characters, which will be used to mark spaces.\n'+
            'Press ENTER to use the default of "x" and "o".\n'+
            'Players? ').strip()
        players: Optional[list[str]] = [p.strip() for p in players_input.split(',')] if players_input else None
        break
    play_game(rounds, size=board_size, players=players)

if __name__ == '__main__':
    main()
