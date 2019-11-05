"""
A class of board

It can read board from disc, store its states and print it
Example of board:

    4 4
    1 - - -
    - 4 - -
    - - - -
    2 - 2 -

First line contains numbers of rows and cols
'-' means empty space
numbers means the area of rectangle that should contain it cell
"""

from colorama import Back
from colorama import Fore
from block import Block


BACK_COLORS = {
    -1: Back.RESET,
    0: Back.RED,
    1: Back.BLUE,
    2: Back.GREEN,
    3: Back.YELLOW,
    4: Back.WHITE,
    5: Back.MAGENTA,
    6: Back.CYAN,
    7: Back.LIGHTWHITE_EX,
    8: Back.LIGHTBLACK_EX,
    9: Back.LIGHTYELLOW_EX,
    10: Back.LIGHTRED_EX,
    11: Back.LIGHTGREEN_EX,
    12: Back.LIGHTCYAN_EX,
    13: Back.LIGHTBLUE_EX,
    14: Back.LIGHTMAGENTA_EX,
}


class Board:
    """
    A game board

    board -- initial state of board

    solution -- end state of board

    blocks -- numbers that should be converted into rectangles

    rows, cols -- sizes of board
    """
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.board = list(list())
        self.solution = list(list())
        self.blocks = list()

    def read_board(self, filename: str) -> None:
        """
        Read board from disk using its filename

        :param filename: Name of the file
        :return:
        """
        with open(filename, "r") as input_file:
            self.rows, self.cols = map(int, input_file.readline().split(' '))
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError(
                    'Illegal board sizes: %r rows and %c cols'
                    % (self.rows, self.cols))
            self.board = [self.cols * [0] for i in range(self.rows)]
            for row, line in enumerate(input_file):
                for col, cell in enumerate(line.split()):
                    if cell == "-":
                        self.board[row][col] = -1
                    else:
                        self.board[row][col] = int(cell)
                        self.blocks.append(Block(row, col, int(cell), []))

    def print_solution(self) -> None:
        """
        Print solution with colors

        :return:
        """
        for row_num, row in enumerate(self.solution):
            current_row = ''
            for col_num, symbol in enumerate(row):
                color = int(symbol) % (len(BACK_COLORS) - 1)
                if self.board[row_num][col_num] == -1:
                    current_line = _get_colored_back(
                        ' '.center(4),
                        BACK_COLORS[color])
                    print(current_line, end='')
                    current_row += current_line
                else:
                    current_line = _get_colored_front(
                        _get_colored_back(
                            str(self.board[row_num][col_num]).center(4),
                            BACK_COLORS[color]),
                        Fore.BLACK)
                    print(current_line, end='')
                    current_row += _get_colored_back(' '.center(4), BACK_COLORS[color])
            print('\n' + current_row)


def _get_colored_back(line: str, color: Back) -> str:
    return color + line + Back.RESET


def _get_colored_front(line: str, color: Fore) -> str:
    return color + line + Fore.RESET
