from Solver.block import Block
from Solver.game_board import GameBoard


class CubeGameBoard:
    def __init__(self, filename: str):
        self.filename = filename
        self.boards = [GameBoard(filename) for i in range(6)]
        self.size = -1

    def read_board(self):
        with open(self.filename, "r") as input_file:
            self.size = int(input_file.readline())
            if self.size <= 0:
                raise ValueError(
                    'Illegal board sizes: %r rows and %c cols'
                    % (self.size, self.size))
            for curr_board in self.boards:
                curr_board.rows = self.size
                curr_board.cols = self.size
                curr_board.board = [self.size * [0] for i in range(self.size)]
                for row, line in enumerate(input_file):
                    for col, cell in enumerate(line.split()):
                        if cell == "-":
                            curr_board.board[row][col] = -1
                        else:
                            curr_board.board[row][col] = int(cell)
                            curr_board.blocks.append(
                                Block(row, col, int(cell)))
                        if col == curr_board.cols - 1:
                            break
                    if row == curr_board.cols - 1:
                        break

                input_file.readline()
                curr_board.initialize_board_solution()
