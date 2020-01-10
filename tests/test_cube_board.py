import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from solver.cube_game_board import CubeGameBoard
from solver.game_board import GameBoard


class TestCubeGameBoard(unittest.TestCase):
    def test_cube_game_board_init(self):
        board = CubeGameBoard('tests/test_cube_puzzle.txt')
        board.read_board()
        side = GameBoard('tests/test_puzzle.txt')
        side.read_board()
        self.assertEqual(board.boards[0].board, side.board)
        self.assertEqual(board.boards[0].solution, side.solution)
        self.assertEqual(board.boards[0].cols, side.cols)
        self.assertEqual(board.boards[0].rows, side.rows)
        self.assertEqual(board.boards[0].blocks[0].value, side.blocks[0].value)
        self.assertEqual(
            board.boards[0].final_cells_values, side.final_cells_values)
