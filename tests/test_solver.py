import os
import sys
import unittest
from unittest import mock

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from shikaku_solver import backtrack
from Solver.game_board import GameBoard


class TestSolver(unittest.TestCase):

    def test_no_name(self):
        board = GameBoard('tests/no_file.txt')
        self.assertRaises(FileNotFoundError, board.read_board)

    def test_common_puzzle(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        backtrack(0, board)
        self.assertEqual(board.solution, [[0, 1, 1], [0, 1, 1], [0, 2, 2]])

    def test_no_solution_puzzle(self):
        board = GameBoard('tests/test_no_solution_puzzle.txt')
        board.read_board()
        backtrack(0, board)
        self.assertFalse(board.verify_solution())

    def test_argument_parsing(self):
        class FakeParser:
            self.cube = True
        with mock.patch('shikaku_solver.parse_args', lambda *_: FakeParser):
            with mock.patch('Form.window.start', lambda *_: None):
                self.assertEqual(sys.exc_info(), (None, None, None))
