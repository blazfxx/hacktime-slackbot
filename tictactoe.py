import random


class TicTacToe:
    WINS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def __init__(self):
        self.board = [" "] * 9

    def player_move(self, pos: int) -> tuple[bool, str]:
        if self.board[pos] != " ":
            return False, "You cant place this here"
        self.board[pos] = "X"
        return True, ""

    def bot_move(self) -> int:
        pos = self._find_winning_move("O")
        if pos is not None:
            self.board[pos] = "O"
            return pos

        pos = self._find_winning_move("X")
        if pos is not None:
            self.board[pos] = "O"
            return pos

        if self.board[4] == " ":
            self.board[4] = "O"
            return 4

        for corner in [0, 2, 6, 8]:
            if self.board[corner] == " ":
                self.board[corner] = "O"
                return corner

        empty = [i for i, v in enumerate(self.board) if v == " "]
        pos = random.choice(empty)
        self.board[pos] = "O"
        return pos

    def _find_winning_move(self, mark: str):
        for a, b, c in self.WINS:
            cells = [self.board[a], self.board[b], self.board[c]]
            if cells.count(mark) == 2 and cells.count(" ") == 1:
                return [a, b, c][cells.index(" ")]
        return None

    def check_winner(self, mark: str) -> bool:
        return any(
            self.board[a] == self.board[b] == self.board[c] == mark
            for a, b, c in self.WINS
        )

    def is_draw(self) -> bool:
        return " " not in self.board


MARKS = {" ": "⬜", "X": "❌", "O": "⭕"}


def format_board(board: list[str]) -> str:
    rows = []
    for row in range(3):
        cells = [MARKS[board[row * 3 + col]] for col in range(3)]
        rows.append("".join(cells))
    return "\n".join(rows)