import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from solver.game_board import GameBoard


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        self.assertEqual(board.rows, 3)
        self.assertEqual(board.cols, 3)
        self.assertEqual(board.board, [[3, 4, -1], [-1, -1, -1], [-1, 2, -1]])
        self.assertEqual(len(board.blocks), 3)
        self.assertEqual(board.blocks[0].row, 0)
        self.assertEqual(board.blocks[0].col, 0)
        self.assertEqual(board.blocks[0].value, 3)
        self.assertEqual(board.blocks[0].factors, [1, 3])
        self.assertEqual(board.blocks[0].factor_pointer, 0)
        self.assertEqual(board.final_cells_values,
                         [[], [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]],
                          [[1, 1], [2, 0],
                           [2, 1], [2, 2]]])
        self.assertEqual(
            board.solution, [[0, 1, -1], [-1, -1, -1], [-1, 2, -1]])

    def test_verify_solution(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        board.solution = [[0, 1, 1], [0, 1, 1], [0, 2, 2]]
        self.assertTrue(board.verify_solution())
