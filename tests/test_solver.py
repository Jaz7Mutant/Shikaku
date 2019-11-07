import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from game_board import Board
import shikaku_solver



class TestSolver(unittest.TestCase):

    def test_no_name(self):
        self.assertRaises(FileNotFoundError, Board, 'tests/no_file.txt')

    def test_common_puzzle(self):
        board = Board('tests/test_puzzle.txt')
        shikaku_solver.backtrack(0, board)
        self.assertEqual(board.solution, [[0, 1, 1], [0, 1, 1], [0, 2, 2]])

    def test_no_solution_puzzle(self):
        # board = Board('test_no_solution_puzzle.txt')
        # shikaku_solver.backtrack(0, board)
        # self.assertTrue(board.check_solution())
        pass

