import json
from datetime import datetime
from pathlib import Path


BOOKS_FILE = Path("books.json")


def load_books(path: Path = BOOKS_FILE) -> list[dict]:
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
        return []

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return data
    return []


def save_books(books: list[dict], path: Path = BOOKS_FILE) -> None:
    path.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split()).lower()


def is_duplicate(books: list[dict], author: str, title: str) -> bool:
    target_author = normalize_text(author)
    target_title = normalize_text(title)
    return any(
        normalize_text(book.get("author", "")) == target_author
        and normalize_text(book.get("title", "")) == target_title
        for book in books
    )


def parse_rating(raw_value: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as error:
        raise ValueError("Оценка должна быть целым числом от 1 до 5.") from error

    if value < 1 or value > 5:
        raise ValueError("Оценка должна быть в диапазоне от 1 до 5.")
    return value


def parse_date(raw_value: str) -> str:
    raw_value = raw_value.strip()
    try:
        datetime.strptime(raw_value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Дата должна быть в формате YYYY-MM-DD.") from error
    return raw_value


def add_book(
    books: list[dict], author: str, title: str, rating: int, read_date: str
) -> tuple[bool, str]:
    if is_duplicate(books, author, title):
        return False, "Такая книга уже есть в списке."

    books.append(
        {
            "author": author.strip(),
            "title": title.strip(),
            "rating": rating,
            "read_date": read_date.strip(),
        }
    )
    return True, "Книга добавлена."


def list_books(books: list[dict]) -> str:
    if not books:
        return "Список книг пуст."

    lines = []
    for index, book in enumerate(books, start=1):
        lines.append(
            f"{index}. {book.get('author', 'Неизвестно')} — "
            f"{book.get('title', 'Без названия')} "
            f"(оценка: {book.get('rating', '-')}, дата: {book.get('read_date', '-')})"
        )
    return "\n".join(lines)


def average_rating(books: list[dict]) -> float | None:
    ratings = [book.get("rating") for book in books if isinstance(book.get("rating"), int)]
    if not ratings:
        return None
    return sum(ratings) / len(ratings)


def author_stats(books: list[dict]) -> dict[str, int]:
    stats: dict[str, int] = {}
    for book in books:
        author = book.get("author", "").strip() or "Неизвестно"
        stats[author] = stats.get(author, 0) + 1
    return stats


def delete_by_index(books: list[dict], index: int) -> tuple[bool, str]:
    if index < 1 or index > len(books):
        return False, "Неверный индекс."

    removed = books.pop(index - 1)
    return (
        True,
        f"Удалена книга: {removed.get('author', 'Неизвестно')} — "
        f"{removed.get('title', 'Без названия')}",
    )


def delete_by_author_title(books: list[dict], author: str, title: str) -> tuple[bool, str]:
    target_author = normalize_text(author)
    target_title = normalize_text(title)

    for i, book in enumerate(books):
        if (
            normalize_text(book.get("author", "")) == target_author
            and normalize_text(book.get("title", "")) == target_title
        ):
            removed = books.pop(i)
            return (
                True,
                f"Удалена книга: {removed.get('author', 'Неизвестно')} — "
                f"{removed.get('title', 'Без названия')}",
            )

    return False, "Книга не найдена."
