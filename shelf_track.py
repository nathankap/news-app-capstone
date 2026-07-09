import sqlite3
from pathlib import Path

DB_NAME = "ebookstore.db"
DB_PATH = Path(__file__).with_name(DB_NAME)


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def add_column_if_missing(connection, table_name, column_name, column_definition):
    existing_columns = {
        row[1] for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name not in existing_columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")


def initialize_database(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            country TEXT
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            authorID INTEGER NOT NULL,
            qty INTEGER NOT NULL CHECK (qty >= 0),
            isbn TEXT,
            publication_year INTEGER,
            publisher TEXT,
            FOREIGN KEY (authorID) REFERENCES author(id)
        )
        """
    )

    add_column_if_missing(connection, "book", "isbn", "TEXT")
    add_column_if_missing(connection, "book", "publication_year", "INTEGER")
    add_column_if_missing(connection, "book", "publisher", "TEXT")

    initial_authors = [
        ("Charles Dickens", "England"),
        ("J.K. Rowling", "England"),
        ("C.S. Lewis", "Ireland"),
        ("J.R.R. Tolkien", "South Africa"),
        ("Lewis Carroll", "England"),
    ]

    for author_name, author_country in initial_authors:
        connection.execute(
            "INSERT OR IGNORE INTO author(name, country) VALUES (?, ?)",
            (author_name, author_country),
        )

    initial_books = [
        ("A Tale of Two Cities", "Charles Dickens", 30, "9780141439600", 1859, "Penguin Classics"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40, "9780747532699", 1997, "Bloomsbury"),
        ("The Lion, the Witch, and the Wardrobe", "C.S. Lewis", 25, "9780064404990", 1950, "HarperCollins"),
        ("The Lord of the Rings", "J.R.R. Tolkien", 37, "9780261102385", 1954, "HarperCollins"),
        ("Alice's Adventures in Wonderland", "Lewis Carroll", 12, "9780147515872", 1865, "Penguin Classics"),
    ]

    for title, author_name, qty, isbn, publication_year, publisher in initial_books:
        author_row = connection.execute(
            "SELECT id FROM author WHERE name = ?", (author_name,)
        ).fetchone()
        if not author_row:
            continue

        connection.execute(
            """
            INSERT OR IGNORE INTO book(title, authorID, qty, isbn, publication_year, publisher)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, author_row["id"], qty, isbn, publication_year, publisher),
        )

    connection.commit()


def prompt_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be left blank. Please try again.")


def prompt_int(prompt, allow_blank=False, minimum=0):
    while True:
        response = input(prompt).strip()
        if allow_blank and response == "":
            return None
        try:
            value = int(response)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value < minimum:
            print(f"Please enter a value greater than or equal to {minimum}.")
            continue
        return value


def prompt_year(prompt):
    while True:
        value = prompt_int(prompt, allow_blank=True, minimum=0)
        if value is None:
            return None
        if 1000 <= value <= 9999:
            return value
        print("Please enter a valid four-digit year.")


def get_author_id(connection, author_name, author_country):
    existing_author = connection.execute(
        "SELECT id FROM author WHERE name = ?", (author_name,)
    ).fetchone()
    if existing_author:
        return existing_author["id"]

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO author(name, country) VALUES (?, ?)",
        (author_name, author_country or "Unknown"),
    )
    connection.commit()
    return cursor.lastrowid


def find_book(connection, book_id):
    return connection.execute(
        """
        SELECT b.id, b.title, b.authorID, b.qty, a.name AS author_name, a.country AS author_country
        FROM book AS b
        LEFT JOIN author AS a ON a.id = b.authorID
        WHERE b.id = ?
        """,
        (book_id,),
    ).fetchone()


def search_book_helper(connection):
    while True:
        book_id = prompt_int("Please enter the book ID of the book you'd like to search. ", minimum=1)
        book = find_book(connection, book_id)
        if book is None:
            print(f"Book with ID ({book_id}) was not found. Please try again.\n")
            continue

        print("\nSelected book:")
        print(f"Book ID: {book['id']}")
        print(f"Title: {book['title']}")
        print(f"Quantity: {book['qty']}")
        print(f"Author: {book['author_name'] or 'N/A'}")
        print(f"Author Country: {book['author_country'] or 'N/A'}")

        confirm = input("Proceed with this book? (y/n) ").strip().lower()
        if confirm in {"y", "yes"}:
            return book


def add_book(connection):
    print("\n*****************\n")
    print("ENTER BOOK")
    print("*****************\n")

    title = prompt_text("Please enter the book title. ")
    author_name = prompt_text("Please enter the author's name. ")
    author_country = prompt_text("Please enter the author's country. ") or "Unknown"
    isbn = input("Please enter the ISBN (leave blank to skip). ").strip() or None
    publication_year = prompt_year("Please enter the publication year (leave blank to skip). ")
    publisher = input("Please enter the publisher (leave blank to skip). ").strip() or None
    qty = prompt_int("Please enter the book quantity. ", minimum=1)

    author_id = get_author_id(connection, author_name, author_country)

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO book(title, authorID, qty, isbn, publication_year, publisher)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, author_id, qty, isbn, publication_year, publisher),
    )
    connection.commit()

    print("\nNew entry successful!")
    print("_________________________\n")
    print(f"Book ID: {cursor.lastrowid}")
    print(f"Title: {title}")
    print(f"Author: {author_name}")
    print(f"Author Country: {author_country}")
    print(f"Quantity: {qty}")
    print("_________________________\n")


def update_book(connection):
    print("\n*****************\n")
    print("UPDATE BOOK")
    print("*****************\n")

    book = search_book_helper(connection)
    update_choice = input(
        "\nEnter 'q' to update the quantity, 't' to update the title, "
        "'a' to update the author's name, or 'c' to update the author's country.\n"
    ).strip().lower()

    if update_choice == "q":
        new_qty = prompt_int("Please enter the new quantity. ", minimum=0)
        connection.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, book["id"]))
        print(f"Successfully updated quantity to ({new_qty})!\n")
    elif update_choice == "t":
        new_title = prompt_text("Please enter the new title. ")
        connection.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, book["id"]))
        print(f"Successfully updated title to ({new_title})!\n")
    elif update_choice == "a":
        new_author_name = prompt_text("Please enter the new author name. ")
        connection.execute(
            "UPDATE author SET name = ? WHERE id = ?",
            (new_author_name, book["authorID"]),
        )
        print(f"Successfully updated author name to ({new_author_name})!\n")
    elif update_choice == "c":
        new_author_country = prompt_text("Please enter the new author country. ")
        connection.execute(
            "UPDATE author SET country = ? WHERE id = ?",
            (new_author_country, book["authorID"]),
        )
        print(f"Successfully updated author country to ({new_author_country})!\n")
    else:
        print("Invalid input. Please try again.\n")
        return

    connection.commit()


def delete_book(connection):
    print("\n*****************\n")
    print("DELETE BOOK")
    print("*****************\n")

    book = search_book_helper(connection)
    confirm = input("Proceed with deleting this book? (y/n) ").strip().lower()
    if confirm in {"y", "yes"}:
        connection.execute("DELETE FROM book WHERE id = ?", (book["id"],))
        connection.commit()
        print("\nSuccessfully deleted!\n")
    else:
        print("Deletion cancelled.\n")


def search_book(connection):
    print("\n*****************\n")
    print("SEARCH BOOK")
    print("*****************\n")

    book_id = prompt_int("Please enter the book ID of the book you'd like to search. ", minimum=1)
    book = find_book(connection, book_id)
    if book is None:
        print(f"Book with ID ({book_id}) was not found. Please try again.\n")
    else:
        print("Selected book:")
        print(f"Title: {book['title']}")
        print(f"Book ID: {book['id']}")
        print(f"Quantity: {book['qty']}")
        print(f"Author: {book['author_name'] or 'N/A'}")
        print(f"Author Country: {book['author_country'] or 'N/A'}")


def view_all_books(connection):
    print("\n*****************\n")
    print("VIEW DETAILS")
    print("*****************\n")

    books = connection.execute(
        """
        SELECT b.id, b.title, a.name AS author_name, a.country AS author_country, b.qty
        FROM book AS b
        JOIN author AS a ON a.id = b.authorID
        ORDER BY b.id
        """
    ).fetchall()

    if not books:
        print("No books found in the database.\n")
        return

    for book in books:
        print("__________________________________")
        print(f"Title: {book['title']}")
        print(f"Author's Name: {book['author_name'] or 'N/A'}")
        print(f"Author's Country: {book['author_country'] or 'N/A'}")
        print(f"Quantity: {book['qty']}")
        print("__________________________________")


def show_menu():
    print("""
    MAIN MENU

    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    5. View details of all books
    0. Exit

    Please select an option.
    """)


def main():
    with connect_db() as connection:
        initialize_database(connection)

        while True:
            try:
                show_menu()
                option = input("Please select an option. ").strip()
            except EOFError:
                print("\nGoodbye!\n")
                break

            if option in {"1", "1."}:
                add_book(connection)
            elif option in {"2", "2."}:
                update_book(connection)
            elif option in {"3", "3."}:
                delete_book(connection)
            elif option in {"4", "4."}:
                search_book(connection)
            elif option in {"5", "5."}:
                view_all_books(connection)
            elif option in {"0", "0."}:
                print("\nGoodbye!\n")
                break
            else:
                print("Invalid input. Please try again.\n")

            try:
                input("Please enter any character to continue.\n")
            except EOFError:
                break


if __name__ == "__main__":
    main()