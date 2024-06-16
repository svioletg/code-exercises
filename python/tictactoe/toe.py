"""A game of Tic-Tac-Toe created as an exercise."""

import itertools
import random
from copy import deepcopy
from typing import Optional


class GameBoard:
    """A Tic-Tac-Toe board that handles anything strictly related to itself,
    like placing down markers or checking for a winning line.
    Does not handle things like player turns.
    """
    def __init__(self, size: int=3, players: list[str]=['x', 'o']):
        """
        @size: Used for both rows and columns, board will always be square.
        @players: List of strings used to represent each value that can be placed on the board.\
            'x' and 'o' by default.
        """
        self.size = size
        self.empty_board: list[list[str]] = [[' ' for _ in range(size)] for _ in range(size)]
        self.board = deepcopy(self.empty_board)
        self.players = players

    def __repr__(self) -> str:
        h_border = '=' + ('====' * self.size)
        rows = [h_border]
        for row in range(self.size):
            row_str = '|'
            for col in range(self.size):
                row_str += f' {self.board[row][col]} |'
            rows.append(row_str)
            rows.append('|' + ('---|' * self.size))
        rows[-1] = h_border
        return '\n'.join(rows)

    def __getitem__(self, item: int) -> list[str]:
        return self.board[item]

    def _winning_lines(self) -> list[list[tuple[int, int]]]:
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
        
        diagonal: list[tuple[int, int]] = [(n, n) for n in range(self.size)]

        return h_lines + v_lines + [diagonal] + [list(reversed(diagonal))]

    def _marker_from_player(self, marker_or_player: str | int):
        """Returns a player's marker string if an integer is given, or the marker itself if a string is given."""
        if not isinstance(marker_or_player, (int, str)):
            raise TypeError(f'marker_or_player must be an integer or string: got {type(marker_or_player)} instead')

        if isinstance(marker_or_player, int):
            marker = self.players[marker_or_player]
        elif isinstance(marker_or_player, str):
            marker = marker_or_player

        return marker

    def reset(self) -> None:
        """Resets the game board to a clear state."""
        self.board = deepcopy(self.empty_board)

    def get(self, row: int, col: int) -> str:
        """Returns the value of a board located at the given position."""
        return self.board[row][col]

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

    def check_for_win(self):
        """Checks if there exists any horizontal, vertical, or diagonal lines of one marker type."""
        # TODO: Finish!
        for line in w:
            mark = None
            is_winner = True
            for point in line:
                if mark and (mark != (mark := b.get(*point))):
                    break

    def place_at(self, row: int, col: int, marker_or_player: int | str) -> None:
        """Attempts to place something at the given position, raising an exception if a value already exists.
        An exception is also raised if the given marker is not a valid player.

        @marker_or_player: Either the index of a player, or the player's associated string itself.
        """
        marker = self._marker_from_player(marker_or_player)

        if marker not in self.players:
            raise ValueError(f'{marker:r} is not a valid player. This game board\'s players are: {', '.join(self.players)}')
        if (existing := self.board[row][col]) != ' ':
            raise ValueError(f'Something is already placed here: {existing}')
        self.board[row][col] = marker

def test_board(size):
    board = GameBoard(size=size)
    for _ in range(random.randint(0, size*size)):
        while True:
            try:
                board.place_at(random.randint(0, size-1), random.randint(0, size-1), random.randint(0, 1))
                break
            except ValueError:
                continue
    return board
