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
from copy import deepcopy

from solver.block import Block
from utilities.colors import BACK_COLORS, colorize_back, colorize_front, \
    FORE_COLORS
from utilities.point import Point


class GameBoard:
    """
    A game board

    board -- initial state of board
    solution -- end state of board
    blocks -- numbers that should be converted into rectangles
    rows, cols -- sizes of board
    """

    def __init__(self, filename: str):
        self.rows = 0
        self.cols = 0
        self.board = list(list())
        self.solution = list(list())
        self.blocks = list()
        self.final_cells_values = list(list())
        self.filename = filename

    def print_solution(self):
        """
        Print solution with colors

        :return:
        """
        void = ' '.center(7)
        for row_num, row in enumerate(self.solution):
            current_row = ''
            curr_row_with_num = ''
            for col_num, symbol in enumerate(row):
                color = int(symbol) % (len(BACK_COLORS) - 1)
                if self.board[row_num][col_num] == -1:
                    current_line = colorize_back(void, BACK_COLORS[color])
                    curr_row_with_num += current_line
                    current_row += current_line
                else:
                    current_line = colorize_front(
                        colorize_back(
                            str(self.board[row_num][col_num]).center(7),
                            BACK_COLORS[color]),
                        FORE_COLORS[0])
                    curr_row_with_num += current_line
                    current_row += colorize_back(void, BACK_COLORS[color])
            print(current_row)
            print(curr_row_with_num)
            print(current_row)

    def read_board(self):
        """
        Read board from disk using its filename

        :param filename: Name of the file
        :return:
        """
        with open(self.filename, "r") as input_file:
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
                        self.blocks.append(Block(row, col, int(cell)))
        self.initialize_board_solution()

    def initialize_board_solution(self):
        from utilities.rectangle import Rectangle
        initial_solution_state = [[-1 for c in range(self.cols)] for r in
                                  range(self.rows)]
        for i in range(len(self.blocks)):
            initial_solution_state[self.blocks[i].row][self.blocks[i].col] = i

        self.solution = deepcopy(initial_solution_state)

        # cover the solution with all possible rectangles for all blocks
        for k in range(len(self.blocks)):
            curr_row = self.blocks[k].row
            curr_col = self.blocks[k].col
            curr_value = self.blocks[k].value
            for factor in self.blocks[k].factors:
                for i in range(curr_value // factor):
                    for j in range(factor):
                        top_left = Point(
                            curr_col + i - curr_value // factor + 1,
                            curr_row - j)
                        bottom_right = Point(
                            curr_col + i,
                            curr_row + factor - 1 - j)
                        try:
                            rect = Rectangle(self, top_left, bottom_right, k)
                            rect.draw_rectangle()
                        except AssertionError:
                            continue
        self._update_final_cells_values()
        self.solution = initial_solution_state

    def verify_solution(self) -> bool:
        # Verify every block
        for i, block in enumerate(self.blocks):
            # solution[row][col] should equal block number (i)
            if self.solution[block.row][block.col] != i:
                return False

            # Get all positions where solution is equal to i.
            i_positions = [
                (r, c) for r in range(self.rows)
                for c in range(self.cols) if self.solution[r][c] == i
            ]
            block_number = len(i_positions)

            # Block number should equal its value.
            if block_number != block.value:
                return False

            # Number should form a rectangle.
            left = min(i_positions, key=lambda x: x[0])[0]
            right = max(i_positions, key=lambda x: x[0])[0]
            top = min(i_positions, key=lambda x: x[1])[1]
            bottom = max(i_positions, key=lambda x: x[1])[1]
            area = (right - left + 1) * (bottom - top + 1)
            if area != block_number:
                return False

        return True

    def _update_final_cells_values(self):
        self.final_cells_values = [[] for i in range(len(self.blocks))]
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.solution[row][col]
                self.final_cells_values[value].append([row, col])
