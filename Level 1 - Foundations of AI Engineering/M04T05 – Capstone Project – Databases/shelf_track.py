# IMPORTS
import sqlite3


# Create database
# Connect to or create a SQLite database file
db = sqlite3.connect('ebookstore.db')

'''

SETTING UP DATABASE & TABLE

'''
# Get a cursor object to interact with the database
cursor = db.cursor()

# Create the book table if it does not exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        authorID INTEGER,
        qty INTEGER
    )
    '''
)

# Create the author table if it does not exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY,
        name TEXT,
        country TEXT
    )
    '''
)

# Populate book table with values
# (id, title, authorID, qty)
books = [(3001, 'A Tale of Two Cities', 1290, 30),
         (3002, 'Harry Potter and the Stone', 8937, 40),
         (3003, 'The Lion, the Witch, and the Wardrobe', 2356, 25),
         (3004, 'The Lord of the Rings', 6380, 37),
         (3005, 'Alice Adventures in Wonderland', 5620, 12)]

# Populate auhor table with values
# (id, name, country)
authors = [(1290, 'Charles Dickens', 'England'),
           (8937, 'J.K. Rowling', 'England'),
           (2356, 'C.S. Lewis', 'Ireland'),
           (6380, 'J.R.R. Tolkien', 'South Africa'),
           (5620, 'Lewis Carroll', 'England')]

cursor.executemany(
    '''
    INSERT OR IGNORE INTO book(id, title, authorID, qty)
    VALUES(?, ?, ?, ?)
    ''',
    books
)

cursor.executemany(
    '''
    INSERT OR IGNORE INTO author(id, name, country)
    VALUES(?, ?, ?)
    ''',
    authors
)

'''

HELPER FUNCTIONS

'''
# Helper function for searching books
# (used by other functions)
def search_book_helper():
    while True:
        # Get user input
        id = try_int("Please enter the book ID of the book you'd like to search. ")

        # Search for book from ID
        cursor.execute('''SELECT id, title, authorID, qty FROM book WHERE id = ?''', (id,))

        # Fetch book
        book = cursor.fetchone()

        # Fetch authors
        cursor.execute('''SELECT * FROM author''')
        author_table = cursor.fetchall()
        
        # Build a lookup dict from author table: {authorID: (name, country)}
        author_lookup = {author[0]: (author[1], author[2]) for author in author_table}

        # Lookup author from book ID
        author_country = author_lookup.get(book[2])
        
        # Author & Country is N/A if needed
        if author_country is None:
            author_country = ("N/A", "N/A")
        elif not author_country[0]:
            author_country[0] = "N/A"
        elif not author_country[1]:
            author_country[1] = "N/A"

        # Ask for verification
        if book is not None:
            print("\nSelected book:\n"
                  f"Title: {book[1]}\n"
                  f"Book ID: {book[0]}\n"
                  f"Quantity: {book[2]}\n"
                  f"Author: {author_country[0]}\n"
                  f"Author Country: {author_country[1]}\n")
            
            cont = input("Proceed with selected book? (y/n) ")
            # Break loop if proceeding with selected book
            if cont.lower() in ['y', 'yes']:
                return book
            # Continue searching if not proceeding
            else:
                pass
        else:
            print(f"Book with ID ({id}) not found. Please try again.\n")

            
# Helper function for testing if user input can be converted to int
# Returns valid result
def try_int(prompt):
    while True:
        result = input(prompt)
        try:
            result = int(result)
            return result
        except Exception as e:
            print(f"Invalid input: {e}")


# Function for entering a new book
def enter_book():
    print('''
\n*****************\n
ENTER BOOK\n
*****************\n
          ''')
    
    # Get user input
    id = try_int("Please enter the book ID. ")
    title = input("Please enter the book title. ")
    author_ID = try_int("Please enter the author ID. ")
    qty = try_int("Please enter the book quantity. ")
    
    # Enter data into table
    cursor.execute('''
        INSERT INTO book(id, title, authorID, qty)
                   VALUES (?, ?, ?, ?)
                   ''', (id, title, author_ID, qty))
    db.commit()
    
    print("\nNew entry successful!")
    print("_________________________\n")
    print(f"ID: {id}\n"
          f"Title: {title}\n"
          f"Author ID: {author_ID}\n"
          f"Quantity: {qty}")
    print("_________________________\n")

    
    input("Please enter any character to continue.\n")
    print("*****************\n")


# Function for update book data
def update_book(): 
    print('''
\n*****************\n
UPDATE BOOK\n
*****************\n
          ''')
    
    # Find book
    book = search_book_helper()
    
    update_choice = input("\nPlease enter new quantity of the book\n"
                            "or enter 't' to update the title\n"
                            "or enter 'id' to update the AuthorID\n"
                            "or enter 'a' to update the author's name\n"
                            "or enter 'c' to update the author's country.\n\n")
    
    while True:
        # update quantity
        if update_choice.isdigit():
            cursor.execute('''UPDATE book SET qty = ? WHERE id = ?''', (update_choice, book[0]))
            print(f"Successfully updated quantity to ({update_choice})!\n")
            break

        # update title
        elif update_choice == 't':
            title = input("Please enter new title of the book. ")
            cursor.execute('''UPDATE book SET title = ? WHERE id = ?''', (title, book[0]))
            print(f"Successfully updated title to ({title})!\n")
            break

        # update authorid
        elif update_choice == 'id':
            author_id = try_int("Please enter new AuthorID of the book. ")
            cursor.execute('''UPDATE book SET authorID = ? WHERE id = ?''', (author_id, book[0]))
            print(f"Successfully updated AuthorID to ({author_id})!\n")
            break

        # update author name
        elif update_choice == 'a':
            author_name = input("Please enter new author name. ")
            cursor.execute('''UPDATE author SET name = ? WHERE id = ?''', (author_name, book[2]))
            print(f"Successfully updated author name to ({author_name})!\n")
            break

        elif update_choice == 'c':
            author_country = input("Please enter new author country. ")
            cursor.execute('''UPDATE author SET country = ? WHERE id = ?''', (author_country, book[2]))
            print(f"Successfully updated author country to ({author_country})!\n")
            break

        else:
            print("Invalid input. Please try again.\n")

    db.commit()
    input("Please enter any character to continue.\n")
    print("*****************\n")


# Function for deleting book data
def delete_book(): 
    print('''
\n*****************\n
DELETE BOOK\n
*****************\n
          ''')
    
    while True:
        book = search_book_helper()
        cont = input("Proceed with deleting selected book? (y/n) ")
        # Break loop if proceeding with deleting selected book
        if cont.lower() in ['y', 'yes']:
            break
        # Continue searching if not proceeding
        else:
            pass
    
    # Delete book from book table
    cursor.execute('''DELETE FROM book WHERE id = ?''', (book[0],))
    db.commit()

    print("\nSuccessfully deleted!\n")
    input("Please enter any character to continue.\n")
    print("*****************\n")
        

# Function for searching books
def search_book():
    print('''
\n*****************\n
SEARCH BOOK
*****************\n
          ''')
    while True:
        # Get user input
        id = try_int("Please enter the book ID of the book you'd like to search. ")

        # Search for book from ID
        cursor.execute('''SELECT title, qty, authorID FROM book WHERE id = ?''', (id,))

        # Fetch book
        book = cursor.fetchone()

        # Ask for verification
        if book is not None:
            print("Selected book:\n"
                  f"Title: {book[1]}\n"
                  f"Book ID: {book[0]}\n"
                  f"Quantity: {book[2]}\n"
                  f"Author ID: {book[3]}\n")
            break
        else:
            print(f"Book with ID ({id}) not found. Please try again.\n")
    
    input("Please enter any character to continue.\n")
    print("*****************\n")

    return book

def details_book():
    print('''
\n*****************\n
VIEW DETAILS
*****************\n
          ''')
    cursor.execute('''SELECT * FROM book''')
    book_table = cursor.fetchall()
    cursor.execute('''SELECT * FROM author''')
    author_table = cursor.fetchall()
    
    # Build a lookup dict from author table: {authorID: (name, country)}
    author_lookup = {author[0]: (author[1], author[2]) for author in author_table}

    for book in book_table:
        author_country = author_lookup.get(book[2])

        # Author & Country is N/A if needed
        if author_country is None:
            author_country = ("N/A", "N/A")
        elif not author_country[0]:
            author_country[0] = "N/A"
        elif not author_country[1]:
            author_country[1] = "N/A"

        print("__________________________________\n")
        print(f"Title: {book[1]}\n"
              f"Author's Name: {author_country[0]}\n"
              f"Author's Country: {author_country[1]}")
        print("__________________________________")

    input("Please enter any character to continue.\n")
    print("*****************\n")

while True:
    option = input('''
    MAIN MENU\n
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    5. View details of all books
    0. Exit\n
    Please select an option.\n
    ''')
    
    if option in ['1', '1.']:
        enter_book()
    elif option in ['2', '2.']:
        update_book()
    elif option in ['3', '3.']:
        delete_book()
    elif option in ['4', '4.']:
        search_book()
    elif option in ['5', '5.']:
        details_book()
    elif option in ['0', '0.']:
        print("\n\nGoodbye!\n")
        db.commit()
        db.close()
        exit()
    else:
        print("Invalid input. Please try again.\n")