import argparse
import glob

import colorama

from Form.window import start
from Solver.cube_game_board import CubeGameBoard
from Solver.game_board import GameBoard
from Solver.solver import Solver
from Utilities.texture_factory import TextureFactory


def main():
    colorama.init()
    namespace = parse_args()
    file_names = sorted(
        glob.glob('Resources/puzzles/*.txt')) if not namespace.cube \
        else sorted(glob.glob('Resources/cube_puzzles/*.txt'))

    for filename in file_names:
        if namespace.cube:
            board = CubeGameBoard(filename)
            board.read_board()
            texture_factory = TextureFactory(board.boards)
            texture_factory.generate_textures()
            start(board.boards)
            continue
        board = GameBoard(filename)
        board.read_board()
        print(filename)
        solver = Solver(board)
        solver.backtrack()
        board.print_solution()
        if board.verify_solution():
            print('Solved')
        else:
            print('Not solved')


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        '--cube',
        help='2D rectangle or 3D cube shikaku',
        action='store_true'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
