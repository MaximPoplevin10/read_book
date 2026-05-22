import tempfile
import unittest
from pathlib import Path

from tracker import (
    add_book,
    author_stats,
    average_rating,
    delete_by_author_title,
    delete_by_index,
    is_duplicate,
    load_books,
    parse_date,
    parse_rating,
    save_books,
)


class TrackerTests(unittest.TestCase):
    def test_parse_rating_valid(self) -> None:
        self.assertEqual(parse_rating("5"), 5)

    def test_parse_rating_invalid(self) -> None:
        with self.assertRaises(ValueError):
            parse_rating("9")

    def test_parse_date_valid(self) -> None:
        self.assertEqual(parse_date("2026-05-22"), "2026-05-22")

    def test_duplicate_detection(self) -> None:
        books = [{"author": "Лем", "title": "Солярис", "rating": 5, "read_date": "2026-01-01"}]
        self.assertTrue(is_duplicate(books, "лем", "  солярис "))

    def test_add_and_delete(self) -> None:
        books: list[dict] = []
        success, _ = add_book(books, "Оруэлл", "1984", 5, "2026-05-22")
        self.assertTrue(success)
        self.assertEqual(len(books), 1)

        success, _ = delete_by_index(books, 1)
        self.assertTrue(success)
        self.assertEqual(len(books), 0)

    def test_delete_by_author_title(self) -> None:
        books = [{"author": "Оруэлл", "title": "1984", "rating": 5, "read_date": "2026-05-22"}]
        success, _ = delete_by_author_title(books, "орУэлл", "1984")
        self.assertTrue(success)
        self.assertEqual(books, [])

    def test_average_and_author_stats(self) -> None:
        books = [
            {"author": "A", "title": "X", "rating": 4, "read_date": "2026-01-01"},
            {"author": "A", "title": "Y", "rating": 2, "read_date": "2026-01-02"},
            {"author": "B", "title": "Z", "rating": 5, "read_date": "2026-01-03"},
        ]
        self.assertAlmostEqual(average_rating(books), 11 / 3)
        self.assertEqual(author_stats(books), {"A": 2, "B": 1})

    def test_load_save_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "books.json"
            books = [{"author": "A", "title": "B", "rating": 4, "read_date": "2026-01-01"}]
            save_books(books, path)
            loaded = load_books(path)
            self.assertEqual(loaded, books)


if __name__ == "__main__":
    unittest.main()
