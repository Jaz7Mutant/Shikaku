import argparse
import glob
from Solver.game_board import GameBoard
from Solver.cube_game_board import CubeGameBoard
import colorama
from Utilities.rectangle import Rectangle
from Utilities.point import Point
from Utilities.texture_factory import TextureFactory
from Form import form


def main():
    colorama.init()
    namespace = parse_args()
    namespace.cube = True # todo
    filenames = sorted(
        glob.glob('puzzles/*.txt')) if not namespace.cube else sorted(
        glob.glob('cube_puzzles/*.txt'))
    for filename in filenames:
        if namespace.cube:
            board = CubeGameBoard(filename)
            board.read_board()
            for curr_board in board.boards:
                backtrack(0, curr_board)
            texture_factory = TextureFactory(board.boards)
            texture_factory.generate_textures()
            form.main()
            return
        board = GameBoard(filename)
        board.read_board()
        print(filename)
        backtrack(0, board)
        board.print_solution()


def backtrack(block_pointer: int, board: GameBoard):
    # if all blocks are visited the solution is found
    if block_pointer > len(board.blocks) - 1:
        return True

    curr_block = board.blocks[block_pointer]

    # go through all block's factors
    while curr_block.factor_pointer < len(curr_block.factors):
        curr_factor = curr_block.factors[curr_block.factor_pointer]

        # go through all rectangles
        # curr_factor * curr_block.value // curr_factor
        for i in range(curr_block.value // curr_factor):
            for j in range(curr_factor):
                top_left = Point(
                    curr_block.col + i - curr_block.value // curr_factor + 1,
                    curr_block.row - j)
                bottom_right = Point(
                    curr_block.col + i,
                    curr_block.row + curr_factor - 1 - j)
                try:
                    rect = Rectangle(
                        board, top_left, bottom_right, block_pointer)
                    if not rect.check_conflicts():
                        rect.draw_rectangle()
                        if _is_area_full_covered(board, block_pointer):
                            # true means correct solution is found
                            if backtrack(block_pointer + 1, board):
                                return True
                        # incorrect state -> reset changes
                        rect.clear()
                        # colorize cell
                        board.solution[curr_block.row][curr_block.col] = \
                            block_pointer
                except AssertionError:
                    continue
        board.blocks[block_pointer].factor_pointer += 1
    # if no rectangles are found, reset pointer
    if block_pointer > 0:
        board.blocks[block_pointer].factor_pointer = 0


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        '-cube',
        help='2D rectangle or 3D cube shikaku',
        action='store_true'
    )
    return parser.parse_args()


def _is_area_full_covered(board: GameBoard, block_pointer: int) -> bool:
    """Check if the block covers the maximum possible area"""
    for i in range(len(board.final_cells_values[block_pointer])):
        row = board.final_cells_values[block_pointer][i][0]
        col = board.final_cells_values[block_pointer][i][1]
        if board.solution[row][col] == -1:
            return False
    return True


if __name__ == '__main__':
    main()
