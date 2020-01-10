import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from utilities.point import Point


class TestPoint(unittest.TestCase):
    def test_point_init(self):
        self.assertEqual(Point(2, 3).x, 2)
        self.assertEqual(Point(2, 3).y, 3)

    def test_sum(self):
        self.assertEqual(Point(2, 3) + Point(3, 0), Point(5, 3))

    def test_sub(self):
        self.assertEqual(Point(2, 3) - Point(3, 0), Point(-1, 3))

    def test_change_coordinates(self):
        point = Point(3, 4)
        point.move_to(2, 0)
        self.assertEqual(point.x, 2)
        self.assertEqual(point.y, 0)

    def test_point_to_string(self):
        self.assertEqual(str(Point(2, 3)), '(2, 3)')

    def test_clone(self):
        point = Point(2, 4)
        new_point = point.clone()
        self.assertEqual(point, new_point)
        point.move_to(0, 0)
        self.assertNotEqual(point, new_point)
