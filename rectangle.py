from game_board import Board
from point import Point


class Rectangle:
    """
    A rectangle identified by top left and bottom right points.

    top_left -------              0 x --> +oo
       |           |              y
       |           |              |
       |-----bottom_right         V
                                 +oo
    """
    def __init__(self, board: Board,
                 position_1: Point,
                 position_2: Point,
                 color: int):
        assert position_1.y <= position_2.y
        assert position_1.x <= position_2.x
        assert position_2.y < board.rows
        assert position_2.x < board.cols
        assert position_1.x >= 0
        assert position_1.y >= 0
        self.board = board
        self.color = color
        self.top_left = position_1
        self.bottom_right = position_2

    def check_conflicts(self) -> bool:
        """
        Check intersections with other rectangles

        :return: True if inner area is not empty and it has a different color
        """
        for row in range(self.top_left.y, self.bottom_right.y + 1):
            for col in range(self.top_left.x, self.bottom_right.x + 1):
                if self.board.solution[row][col] != self.color and \
                        self.board.solution[row][col] != -1:
                    return True
        return False

    def clear(self):
        """Fill rectangle with -1"""
        self.color = -1
        self.draw_rectangle()

    def draw_rectangle(self):
        """Fill rectangle with color"""
        for row in range(self.top_left.y, self.bottom_right.y + 1):
            for col in range(self.top_left.x, self.bottom_right.x + 1):
                self.board.solution[row][col] = self.color
