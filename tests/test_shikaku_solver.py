import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from Solver.solver import Solver
from Solver.game_board import GameBoard


class TestSolver(unittest.TestCase):

    def test_no_name(self):
        board = GameBoard('tests/no_file.txt')
        self.assertRaises(FileNotFoundError, board.read_board)

    def test_common_puzzle(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        solver = Solver(board)
        solver.backtrack()
        self.assertEqual(board.solution, [[0, 1, 1], [0, 1, 1], [0, 2, 2]])

    def test_no_solution_puzzle(self):
        board = GameBoard('tests/test_no_solution_puzzle.txt')
        board.read_board()
        solver = Solver(board)
        solver.backtrack()
        self.assertFalse(board.verify_solution())
