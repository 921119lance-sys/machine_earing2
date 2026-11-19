"""Run with: python -m unittest discover -s src -p 'test_*.py' -v"""
import csv
import tempfile
import unittest
from pathlib import Path

from clean_data import clean_csv, clean_rows


class CleanDataTests(unittest.TestCase):
    def test_cleaning(self):
        header, rows, count = clean_rows(
            " Name , Age\n Alice , NA\n Alice , NA\n , \n Bob , 22\n"
        )
        self.assertEqual(header, ["name", "age"])
        self.assertEqual(rows, [("Alice", ""), ("Bob", "22")])
        self.assertEqual(count, 4)

    def test_original_file_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "original.csv"
            destination = Path(directory) / "processed" / "clean.csv"
            original = " Name , Age\n Ann , 19\n Ann , 19\n"
            source.write_text(original, encoding="utf-8")
            self.assertEqual(clean_csv(source, destination), (2, 1))
            self.assertEqual(source.read_text(encoding="utf-8"), original)
            with destination.open(newline="", encoding="utf-8") as file:
                self.assertEqual(list(csv.reader(file)), [["name", "age"], ["Ann", "19"]])

    def test_same_path_is_not_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "test.csv"
            file.write_text("a\n1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                clean_csv(file, file)


if __name__ == "__main__":
    unittest.main()
