import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from utilities.rectangle import Rectangle
from utilities.point import Point
from solver.game_board import GameBoard


class TestRectangle(unittest.TestCase):
    def test_rectangle_init(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        rect = Rectangle(board, Point(0, 1), Point(2, 2), 0)
        self.assertEqual(rect.board, board)
        self.assertEqual(rect.color, 0)
        self.assertEqual(rect.top_left, Point(0, 1))
        self.assertEqual(rect.bottom_right, Point(2, 2))

    def test_wrong_cords_init(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        self.assertRaises(
            AssertionError, Rectangle, board, Point(-1, 0), Point(2, 1), 0
        )
        self.assertRaises(
            AssertionError, Rectangle, board, Point(-5, -4), Point(4, 6), 0
        )
        self.assertRaises(
            AssertionError, Rectangle, board, Point(2, 2), Point(1, 1), 0
        )

    def test_draw_rect(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        rect = Rectangle(board, Point(0, 0), Point(2, 1), 4)
        rect.draw_rectangle()
        for y in range(2):
            for x in range(3):
                self.assertEqual(board.solution[y][x], 4)

    def test_clear_rect(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        rect = Rectangle(board, Point(0, 0), Point(2, 1), 4)
        rect.draw_rectangle()
        rect.color = - 1
        rect.draw_rectangle()
        for y in range(2):
            for x in range(3):
                self.assertEqual(board.solution[y][x], -1)

    def test_find_color(self):
        board = GameBoard('tests/test_puzzle.txt')
        board.read_board()
        rect = Rectangle(board, Point(0, 0), Point(0, 0), 3)
        rect.draw_rectangle()
        rect = Rectangle(board, Point(0, 0), Point(2, 2), 4)
        rect.find_color()
        self.assertEqual(rect.color, 3)
