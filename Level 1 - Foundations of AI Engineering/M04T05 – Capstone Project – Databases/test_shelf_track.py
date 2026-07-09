import sqlite3
import subprocess
import sys
import unittest
from pathlib import Path

import shelf_track


class ShelfTrackTests(unittest.TestCase):
    def test_initialize_database_does_not_duplicate_books_on_repeat(self):
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row

        shelf_track.initialize_database(connection)
        shelf_track.initialize_database(connection)

        book_count = connection.execute("SELECT COUNT(*) AS count FROM book").fetchone()["count"]
        self.assertEqual(book_count, 5)

    def test_search_flow_uses_title_instead_of_book_id(self):
        script_path = Path(__file__).with_name('shelf_track.py')

        result = subprocess.run(
            [sys.executable, str(script_path)],
            input='4\nA Tale of Two Cities\ny\n0\n0\n',
            text=True,
            capture_output=True,
            timeout=30,
            cwd=script_path.parent,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn('Please enter the book title', result.stdout)
        self.assertNotIn('Please enter the book ID', result.stdout)

    def test_enter_book_flow_uses_user_friendly_prompts(self):
        script_path = Path(__file__).with_name('shelf_track.py')

        result = subprocess.run(
            [sys.executable, str(script_path)],
            input='1\nTest Book Unique\nTest Author Unique\nTest Country\n3\n0\n0\n',
            text=True,
            capture_output=True,
            timeout=30,
            cwd=script_path.parent,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn('Please enter the book title.', result.stdout)
        self.assertIn('New entry successful!', result.stdout)
        self.assertNotIn('Please enter the book ID.', result.stdout)
        self.assertNotIn('Please enter the author ID.', result.stdout)


if __name__ == '__main__':
    unittest.main()
