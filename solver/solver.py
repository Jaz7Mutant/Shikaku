from solver.game_board import GameBoard
from utilities.point import Point
from utilities.rectangle import Rectangle


class Solver:
    def __init__(self, board: GameBoard):
        self.board = board

    def backtrack(self, block_pointer: int = 0):
        # if all blocks are visited the solution is found
        if block_pointer > len(self.board.blocks) - 1:
            return True

        curr_block = self.board.blocks[block_pointer]

        # go through all block's factors
        while curr_block.factor_pointer < len(curr_block.factors):
            curr_factor = curr_block.factors[curr_block.factor_pointer]

            # go through all rectangles
            # curr_factor * curr_block.value // curr_factor
            for i in range(curr_block.value // curr_factor):
                for j in range(curr_factor):
                    top_left = Point(
                        curr_block.col + i - curr_block.value // curr_factor+1,
                        curr_block.row - j)
                    bottom_right = Point(
                        curr_block.col + i,
                        curr_block.row + curr_factor - 1 - j)
                    try:
                        rect = Rectangle(
                            self.board, top_left, bottom_right, block_pointer)
                        if not rect.check_conflicts():
                            rect.draw_rectangle()
                            if self._is_area_full_covered(block_pointer):
                                # true means correct solution is found
                                if self.backtrack(block_pointer + 1):
                                    return True
                            # incorrect state -> reset changes
                            rect.clear()
                            # colorize cell
                            self.board.solution[
                                curr_block.row][curr_block.col] = block_pointer
                    except AssertionError:
                        continue
            self.board.blocks[block_pointer].factor_pointer += 1
        # if no rectangles are found, reset pointer
        if block_pointer > 0:
            self.board.blocks[block_pointer].factor_pointer = 0

    def _is_area_full_covered(self, block_pointer: int) -> bool:
        """Check if the block covers the maximum possible area"""
        for i in range(len(self.board.final_cells_values[block_pointer])):
            row = self.board.final_cells_values[block_pointer][i][0]
            col = self.board.final_cells_values[block_pointer][i][1]
            if self.board.solution[row][col] == -1:
                return False
        return True
