import unittest
from minesweeper import minesweeper

class TestMinesweeper(unittest.TestCase):

    # Test a board with mines in different locations
    def test_board_with_mines(self):
        board = [
            ['-', '-', '-', '#', '#'],
            ['-', '#', '-', '-', '-'],
            ['-', '-', '#', '-', '-'],
            ['-', '#', '#', '-', '-'],
            ['-', '-', '-', '-', '-']
        ]

        expected = [
            [1, 1, 2, '#', '#'],
            [1, '#', 3, 3, 2],
            [2, 4, '#', 2, 0],
            [1, '#', '#', 2, 0],
            [1, 2, 2, 1, 0]
        ]

        result = minesweeper(board)

        self.assertEqual(result, expected)

    # Test a board with no mines
    def test_board_with_no_mines(self):
        board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ]

        expected = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        result = minesweeper(board)

        self.assertEqual(result, expected)

    # Test a board with all mines
    def test_board_with_all_mines(self):
        board = [
            ['#', '#'],
            ['#', '#']
        ]

        expected = [
            ['#', '#'],
            ['#', '#']
        ]

        result = minesweeper(board)

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()