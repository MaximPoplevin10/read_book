from tracker import (
    add_book,
    author_stats,
    average_rating,
    delete_by_author_title,
    delete_by_index,
    list_books,
    load_books,
    parse_date,
    parse_rating,
    save_books,
)


def show_menu() -> None:
    print("\nТрекер прочитанных книг")
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Показать среднюю оценку")
    print("4. Статистика по авторам")
    print("5. Удалить книгу")
    print("6. Выход")


def handle_add(books: list[dict]) -> None:
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()

    try:
        rating = parse_rating(input("Введите оценку (1-5): ").strip())
        read_date = parse_date(input("Введите дату прочтения (YYYY-MM-DD): ").strip())
    except ValueError as error:
        print(error)
        return

    success, message = add_book(books, author, title, rating, read_date)
    if success:
        save_books(books)
    print(message)


def handle_list(books: list[dict]) -> None:
    print(list_books(books))


def handle_avg(books: list[dict]) -> None:
    avg = average_rating(books)
    if avg is None:
        print("Нет данных для расчёта средней оценки.")
        return
    print(f"Средняя оценка: {avg:.2f}")


def handle_author_stats(books: list[dict]) -> None:
    stats = author_stats(books)
    if not stats:
        print("Список книг пуст.")
        return

    print("Статистика по авторам:")
    for author, count in sorted(stats.items(), key=lambda item: item[0].lower()):
        print(f"- {author}: {count}")


def handle_delete(books: list[dict]) -> None:
    if not books:
        print("Удалять нечего: список пуст.")
        return

    print("Выберите способ удаления:")
    print("1. По индексу")
    print("2. По автору и названию")
    method = input("Ваш выбор: ").strip()

    if method == "1":
        try:
            index = int(input("Введите индекс книги: ").strip())
        except ValueError:
            print("Индекс должен быть целым числом.")
            return

        success, message = delete_by_index(books, index)
    elif method == "2":
        author = input("Введите автора: ").strip()
        title = input("Введите название: ").strip()
        success, message = delete_by_author_title(books, author, title)
    else:
        print("Неизвестный способ удаления.")
        return

    if success:
        save_books(books)
    print(message)


def main() -> None:
    books = load_books()
    actions = {
        "1": handle_add,
        "2": handle_list,
        "3": handle_avg,
        "4": handle_author_stats,
        "5": handle_delete,
    }

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "6":
            print("До встречи.")
            break

        action = actions.get(choice)
        if action is None:
            print("Неверный пункт меню, попробуйте снова.")
            continue

        action(books)


if __name__ == "__main__":
    main()
