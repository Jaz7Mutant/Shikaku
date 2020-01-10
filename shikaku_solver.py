import argparse
import glob

import colorama

from form.window import start
from solver.cube_game_board import CubeGameBoard
from solver.game_board import GameBoard
from solver.solver import Solver
from utilities.texture_factory import TextureFactory


def main():
    colorama.init()
    namespace = parse_args()
    file_names = sorted(
        glob.glob('resources/puzzles/*.txt')) if not namespace.cube \
        else sorted(glob.glob('resources/cube_puzzles/*.txt'))

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
