import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from Solver.block import Block


class TestBlock(unittest.TestCase):
    def test_block_init(self):
        block = Block(2, 5, 6)
        self.assertEqual(block.row, 2)
        self.assertEqual(block.col, 5)
        self.assertEqual(block.value, 6)

    def test_block_find_factors(self):
        block = Block(4, 5, 6)
        self.assertEqual(block.factors, [1, 6, 2, 3])
