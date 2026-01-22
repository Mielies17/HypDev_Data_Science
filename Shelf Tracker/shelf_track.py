# Capstone Project Databases M04T05

# Import sqlite3 module
import sqlite3


def create_db1():
    '''
    Create and connect to SQLite database 'ebookstore.db'.
    
    Create the first table 'book' with following attributes:
    - id (4 digit integer and primary key)
    - title (text)
    - authorID (4 digit integer and foreign key to 'author' table)
    - qty (quantity of books)
    
    Inserts books into the table.

    Saves the changes to database and closes the database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    # Create table 'book'
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY CHECK (id >= 1000 AND id <= 9999),
            title TEXT,
            authorID INTEGER CHECK (authorID >= 1000 AND authorID <= 9999),
            qty INTEGER,
            FOREIGN KEY (authorID) REFERENCES author(id)
        )
        '''
    )

    # Populate table with values
    book_data = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12),
        (3006, "Hidden Nature", 1234, 5),
        (3007, "Inheritance", 5678, 7),
        (3008, "The Mirror", 1357, 9)
    ]

    # Insert values into table
    cursor.executemany(
        '''
        INSERT OR IGNORE INTO book (id, title, authorID, qty)
        VALUES (?, ?, ?, ?)
        ''',
        book_data
    )

    # Commit changes to database
    db.commit()
    print("Books successfully inserted.")

    # Close database
    db.close()


def create_db2():
    '''
    Create and connect to SQLite database 'ebookstore.db'.
    
    Create the second table 'author' with following attributes:
    - id (4 digit integer and primary key)
    - name (text)
    - country (text)
    
    It then inserts author details into the table.
    
    Saves the changes to database and closes the database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    # Create table 'author'
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY CHECK (id >= 1000 AND id <= 9999),
            name TEXT,
            country TEXT
        )
        '''
    )

    # Populate table with values
    author_data = [
        (1290, 'Charles Dickens', 'England'),
        (8937, 'J.K. Rowling', 'England'),
        (2356, 'C.S. Lewis', 'Ireland'),
        (6380, 'J.R.R. Tolkien', 'South Africa'),
        (5620, 'Lewis Carroll', 'England'),
        (1234, 'Nora Roberts', 'USA'),
        (5678, 'Aron Strebor', 'USA'),
        (1357, 'A.S. Ronbor', 'USA'),
        (2468, 'Dan Brown', 'USA')
    ]

    # Insert values into table
    cursor.executemany(
        '''
        INSERT OR IGNORE INTO author(id, name, country)
        VALUES (?, ?, ?)
        ''',
        author_data
    )

    # Commit changes to database
    db.commit()
    print("Author data successfully inserted.")

    # Close database
    db.close()


def enter_book():
    '''
    Add new book to database.

    Request user input:
    - new_id = ID number of the new book (4 digit integer)
        - checks if this ID already exists
    - new_title = Title of new book
    - new_authorID = Author ID of new book (4 digit integer)
    - new_author_name = name of author
    - new_author_country = country of author
    - new_qty = quantity of books to add

    Insert these values into the tables 'book' and 'author'.

    Save changes and close database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    while True:
            while True:
                try:
                    # Prompt user input for new book ID
                    new_id = int(
                        input(
                            "\nPlease enter the 4-digit ID of the book you "
                            "want to add (enter '-1' to exit): "
                        ).strip()
                    )

                    # Check if book ID is 4 digits
                    if len(str(new_id)) != 4:
                        if new_id == -1:
                            print("Exiting to main menu.")
                            return
                        print(
                            "ID number must be 4 digits and " 
                            "cannot start with '0'."
                        )
                        continue  # Reprompts for book ID

                except ValueError:
                    print("Book ID must be a numerical value")
                    continue  # Reprompts for book ID

                # Query to check if ID number already exists
                cursor.execute("SELECT * FROM book WHERE id = ?", (new_id,))

                # Get results of query
                id_exist = cursor.fetchone()

                # Inform user if ID exist then reprompts for ID
                if id_exist:
                    print(
                        f"There is already a book with ID number: {new_id}."
                    )
                else:
                    break  # Break out of loop with valid ID

            # Prompt user for new book title and format
            new_title = input(
                "\nPlease enter the title of the book you would like to add: "
            ).strip().title()

            while True:
                try:
                    # Prompt user for new authorID
                    new_authorID = int(
                        input(
                            "\nPlease enter the 4-digit author ID of the "
                            "book you want to add: "
                        )
                    )

                    # Check if authorID is 4 digits
                    if len(str(new_authorID)) != 4:
                        print(
                            "AuthorID must be 4 digits and cannot start " 
                            "with 0."
                        )
                        continue  # Reprompts for authorID

                    else:
                        # Prompt user for name and country of authorID
                        # to update 'author' table as well
                        new_author_name = input(
                            "\nPlease enter the author's name: "
                        ).strip().title()
                        new_author_country = input(
                            "\nPlease enter the author's country: "
                        ).strip().title()

                        # Query to check of new author name and country
                        # is matches that of existing authorID
                        cursor.execute(
                            "SELECT name, country FROM author WHERE id = ?",
                            (new_authorID,)
                        )

                        # Fetch results of query and format
                        name_country_exist = cursor.fetchone()

                        if name_country_exist:
                            # Format fetched results
                            name_exist = name_country_exist[0]
                            country_exist = name_country_exist[1]

                            # Check if new entries are the same as
                            # existing entries
                            if (
                                name_exist != new_author_name 
                                or country_exist != new_author_country
                            ): 
                                print(
                                    f"The authorID '{new_authorID} already "
                                    "has different existing author details:\n"
                                    f"Name: {name_exist}\n"
                                    f"Country: {country_exist}\n"
                                )
                                # Asks user if they want to use
                                # existing values
                                use_or_diff = input(
                                    "Would you like to:\n"
                                    "a) Use existing values for new book?\n" 
                                    "b) Use a different authorID?\n"
                                ).strip().lower()

                                if use_or_diff == "a":
                                    # Change the new entry values to
                                    # that of the existing values
                                    new_author_name = name_exist
                                    new_author_country = country_exist
                                    break
                                else:  # If user chooses 'b'
                                    print(
                                        "You have chosen to use a different "
                                        "authorID"
                                    )
                                    continue  # Reprompts for different authorID

                        break  # Break out loop with valid input

                except ValueError:
                    print("AuthorID must be a numerical value.")
                    continue  # Reprompts for authorID

            while True:
                try:
                    new_qty = int(
                        input(
                            "\nHow many copies of this book would " 
                            "you like to enter?: "
                        )
                    )
                    break  # Break out of loop with valid entry
                except ValueError:
                    print("Quantity must be a numerical value.")
                    continue  # Reprompts for quantity

            # Query to add new book's ID, title, authorID and quantity 
            # into 'book' table
            cursor.execute(
                '''
                INSERT INTO book(id, title, authorID, qty)
                VALUES (?, ?, ?, ?)
                ''',
                (new_id, new_title, new_authorID, new_qty)
            )
                
            # Query to add new book's authorID, author name and country 
            # into 'author' table
            cursor.execute(
                '''
                INSERT OR IGNORE INTO author(id, name, country)
                VALUES (?, ?, ?)
                ''',
                (new_authorID, new_author_name, new_author_country)
            )

            # Commit changes to database
            db.commit()
            print("\nNew book successfully added.")
            break  # Exit loop
    
    # Close database
    db.close()


def update_book():
    '''
    Ask user for the ID of the book they want to update.
    It then joins the 'book' and 'author' table by using the 'id'
    attribute in the 'author' table as a foreign key - linking it to
    'authorID' in 'book' table.

    prints the book details.

    Asks if user wants to update the quantity of book or look at
    other options.
    - Yes - update quantity by default
    - No - gives other options to update (title, authorID, author 
    name and author country)
    
    Requests new details for selected book depending on user's choice 
    and checks if entries are valid.

    Updates both tables.

    Save changes to database and close database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    while True:
        try:
            # Prompt for book ID
            update_id = int(
                input(
                    "\nEnter the 4-digit ID of the book you want to "
                    "update (enter '-1' to exit this menu)?: ")
            )

            if len(str(update_id)) != 4:
                print(
                    "ID number must be 4 digits and " 
                    "cannot start with '0'."
                )
                continue  # Reprompts for ID

            break
        except ValueError:
            print("Invalid input. Book ID must be a numerical value.")

    # Query to select and show details of selected book
    cursor.execute(
        '''
        SELECT book.id, book.title, book.authorID, book.qty, 
        author.name, author.country
        FROM book
        JOIN author
        ON book.authorID = author.id
        WHERE book.id = ?
        ''',
        (update_id,)
    )

    # Fetch the query results and print book details
    book = cursor.fetchone()

    # Get column names
    details = cursor.description
    detail = [item[0] for item in details]

    # Print book if it exists
    if book:
        # Create a dictionary by pairing each value with its attribute
        # and print
        book_info = dict(zip(detail, book))
        print("-" * 30)  # Border for clarity
        print(f"Book ID: {book_info['id']}")
        print(f"Title: {book_info['title']}")
        print(
            f"Author's Name(AuthorID): {book_info['name']}"
            f"({book_info['authorID']})"
            )
        print(f"Author's Country: {book_info['country']}")
        print(f"Book quantity: {book_info['qty']}")
        print("-" * 30)  # Border
        
        while True:
            # Ask user if they want to update quantity of book or look
            # at other options
            update_choice = input(
                "\nWould you like to update the quantity of this book?. "
                "If so, please enter 'Yes'.\nIf you want to look at other "
                "options, please enter 'No'.(enter 'e' to exit):\n"
            ).strip().lower()
            
            # If they want to update the quantity
            if update_choice == "yes":
                while True:
                    try:
                        # Ask for new quantity
                        add_qty = int(
                            input(
                                "\nHow many copies of the book would you like "
                                "to add?: "
                            )
                        )

                        # Calculate updated quantity
                        updated_qty = book[3] + add_qty

                        # Query to update quantity
                        cursor.execute(
                            "UPDATE book SET qty = ? WHERE id = ?",
                            (updated_qty, update_id)
                        )

                        # Commit changes to database
                        db.commit()
                        print(
                            f"\nQuantity of book with ID '{update_id}' has "
                            f"been incremented by: {add_qty}"
                        )
                        break

                    except ValueError:
                        print(
                            "Invalid input. Quantity must be a " 
                            "numerical value."
                        )
                        continue  # Reprompts for quantity

            # If user wants to look at other options
            elif update_choice == "no":
                # Menu with other options
                second_update_choice = input(
                    "\nPlease select what you would like to update:\n"
                    "a) Title of the book\n"
                    "b) Author ID\n"
                    "c) Author name\n"
                    "d) Author country\n"
                    "e) Exit\n"
                ).strip().lower()
                
                # If user wants to update title
                if second_update_choice == "a":
                    # Ask user for new titles
                    updated_title = input(
                        "\nPlease enter new book title: "
                    ).strip().title()

                    # Query to update title
                    cursor.execute(
                        "UPDATE book SET title = ? WHERE id = ?",
                        (updated_title, update_id)
                    )

                    # Commit changes to database
                    db.commit()
                    print(
                        f"\nThe title of the book with ID '{update_id}' "
                        f"has been updated to: {updated_title}."
                    )
                    
                # If user wants to update author ID
                elif second_update_choice == "b":
                    while True:
                        try:
                            # Ask user for new author ID 
                            updated_authorID = int(
                                input(
                                    "\nPlease enter the new 4-digit "
                                    "author ID: "
                                ).strip()
                            )
                            
                            if len(str(updated_authorID)) != 4:
                                print(
                                    "New authorID must be 4 digits " 
                                    "and cannot start with 0."
                                )
                                continue  # Reprompts for authorID
                            
                            # Query to check if new authorID already 
                            # exists in 'author' table
                            cursor.execute(
                                "SELECT * FROM author WHERE id = ?",
                                (updated_authorID,)
                            )

                            # Fetch results of query
                            authorID_exists = cursor.fetchone()

                            # Query to get current authorID from 'book'
                            # table to link to 'author' table
                            cursor.execute(
                                "SELECT authorID " 
                                "FROM book " 
                                "WHERE id = ?",
                                (update_id,)
                            )

                            # Fetch results of query and format
                            authorID_book = cursor.fetchone()
                            authorID_current = authorID_book[0]

                            # Query to update authorID in 'book' table
                            cursor.execute(
                                "UPDATE book SET authorID = ? "
                                "WHERE id = ?",
                                (updated_authorID, update_id)
                            )
                        
                            if not authorID_exists:
                                # Query to update authorID in 'author'
                                # table
                                cursor.execute(
                                    "UPDATE author SET id = ? "
                                    "WHERE id = ?",
                                    (updated_authorID, authorID_current)
                                )  

                            # Commit changes to database
                            db.commit()
                            print(
                                "\nThe Author ID of the book "
                                f"with ID {update_id} has been updated "
                                f"to {updated_authorID}."
                            )
                            break

                        except ValueError:
                            print(
                                "Invalid input. "
                                "Author ID must be a numerical value."
                            )

                # If user wants to update author name
                elif second_update_choice == "c":
                    # Ask user for new author name
                    updated_name = input(
                        "\nPlease enter the new author name: "
                    ).strip().title()

                    # Query to get that authorID from 'book' table of
                    #  selected book
                    cursor.execute(
                        "SELECT authorID FROM book WHERE id = ?",
                        (update_id,)
                    )

                    # Fetch results of query and format
                    authorID_result = cursor.fetchone()
                    authorID_key = authorID_result[0]

                    # Query to change the name of the author with that
                    # author ID
                    cursor.execute(
                        "UPDATE author SET name = ? WHERE id = ?",
                        (updated_name, authorID_key)
                    )

                    # Commit changes to database
                    db.commit()
                    print(
                        "\nThe author name of the book with ID "
                        f"'{update_id}' has been updated to: "
                        f"{updated_name}."
                    )
                
                # If user wants to update author country
                elif second_update_choice == "d":
                    # Ask user for new country name
                    updated_country = input(
                        "\nPlease enter the new country name: "
                    ).strip().title()

                    # Query to get that authorID from 'book' table of
                    # selected book
                    cursor.execute(
                        "SELECT authorID FROM book WHERE id = ?",
                        (update_id,)
                    )

                    # Fetch results of query and format
                    authorID_result = cursor.fetchone()
                    authorID_key = authorID_result[0]

                    # Query to change the country of the author with
                    # that authorID
                    cursor.execute(
                        "UPDATE author SET country = ? WHERE id = ?",
                        (updated_country, authorID_key)
                    )

                    # Commit changes to database
                    db.commit()
                    print(
                        f"\nThe author's country of the book with "
                        f"ID '{update_id}' has been updated "
                        f"to: {updated_country}.")
                
                elif second_update_choice == "e":
                    print("Exiting to main menu")
                    return 

                else:
                    print(
                        "Invalid selection. "
                        "Please choose 'a', 'b', 'c', 'd' or 'e'."
                    )
            
            elif update_choice == "e":
                print("Exiting update menu.")
                return  # Exit loop to main menu
            
            else:
                print(
                    "Invalid selection. Please enter 'Yes', 'No' or 'e'."
                )

    elif update_id == -1:
        print("Exiting update menu.")
        return  # Exit loop to main menu

    else:
        # Inform user if book does not exist
        print(f"Book with ID: {update_id} does not exist.")
    
    # Close database
    db.close()


def delete_book():
    '''
    Prints the book ID and title of all the books in the database
    then asks user to input the ID of the book they want to delete.

    It then gets the authorID for that specific book and deletes
    the book's details from the 'book' table and deletes the 
    author details from the 'author' table.

    Saves changes to database and close database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    # Query to get each book from table
    cursor.execute("SELECT * FROM book")

    # Fetch results of query
    books = cursor.fetchall()

    print("\nBelow is a list of book IDs with their titles:")
    # Print each book with its details
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}")

    while True:
        try:
            # Ask user for ID of book they want to delete
            delete_id = int(
                input(
                    "\nPlease enter the 4-digit ID of the book you want to " 
                    "delete (enter '-1' to exit to main menu): "
                )
            )

            if len(str(delete_id)) != 4:
                if delete_id == -1:
                    print("Exiting to main menu.")
                    break  # Exit loop to main menu
                print("Book ID must be 4 digits and cannot start with 0.")
                continue  # Reprompts for book ID

            # Query to check if book ID exists
            cursor.execute(
                "SELECT * FROM book WHERE id = ?", (delete_id,)
            )

            # Get results of query
            id_not_del = cursor.fetchone()

            # Check if ID exists 
            if id_not_del:
                # Get authorID from 'book' table to link with 'author'
                # table 
                cursor.execute(
                    "SELECT authorID FROM book WHERE id = ?", (delete_id,)
                )

                # Fetch results from query and format
                del_from_author = cursor.fetchone()
                del_authorID = del_from_author[0]

                # Query to check how many books belong to author
                # with this authorID
                cursor.execute(
                    "SELECT COUNT (*) FROM book WHERE authorID = ?",
                    (del_authorID,)
                )

                # Fetch results of query and format
                count_result = cursor.fetchone()
                author_count = count_result[0]

                # Query to delete book details from 'book' table
                cursor.execute("DELETE FROM book WHERE id = ?", (delete_id,))

                if author_count == 1:
                    # Query to delete author details from 'author' table
                    # if this is the only book by this author
                    cursor.execute(
                        "DELETE FROM author WHERE id = ?", (del_authorID,)
                    )

                # Commit changes to database
                db.commit()
                print(f"Book with ID '{delete_id}' has been deleted.")
                break

            else:
                # Inform user if book does not exist
                print(f"Book with ID '{delete_id}' does not exist.")

        except ValueError:
            print("Invalid input. ID must be numerical.")
    
    # Close database
    db.close()


def search_book():
    '''
    Asks user what they want to use to search for specific book:
    - ID - ID of book
    - Title - Title of book
    - AuthorID - Author ID of book

    Joins the 'book' and 'author' table by using the 'id' column 
    in the 'author' table as a foreign key linking it to the 'authorID'
    column in the 'book' table.

    Checks if the user entries are valid and if the book that is
    being searched exists.

    Prints all the details of the book.

    Does not save changes to the database as nothing is 
    being modified but closes the database.
    '''
    # Connects to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()   
    
    while True:
        # Ask user how they want to search for book
        search_choice = input(
            "\nPlease choose what property you want to use to "
            "search for the book:\n"
            "1. ID\n"
            "2. Title\n"
            "3. AuthorID\n"
            "-1. Exit search\n"
        ).strip()

        # Search by ID
        if search_choice == "1":
            while True:
                try:
                    # Ask for the book ID
                    search_id = int(
                        input(
                            "\nPlease enter the 4-digit ID of the book you "
                            "want to search for: "
                        ).strip()
                    )

                    if len(str(search_id)) != 4:
                        print(
                            "Book ID must be 4 digits and cannot start with 0."
                        )
                        continue  # Reprompts user for ID

                    # Query to search for the book
                    cursor.execute(
                        '''
                        SELECT book.id AS book_id, book.title, book.authorID,
                        book.qty, author.id AS author_id, author.name, 
                        author.country
                        FROM book 
                        JOIN author
                        ON book.authorID = author.id
                        WHERE book.id = ?
                        ''',
                        (search_id,)
                    )
                    break  # Breaks out loop with valid ID

                except ValueError:
                    print(f"Invalid input. ID must be numerical value")

        # Search by Title
        elif search_choice == "2":
            # Ask for the title
            search_title = input(
                "\nWhat is the title of the book you want to search: "
            ).strip().title()

            # Query to search for the book
            cursor.execute(
                '''
                SELECT book.id AS book_id, book.title, book.authorID,
                book.qty, author.id AS author_id, author.name, author.country 
                FROM book 
                JOIN author
                ON book.authorID = author.id
                WHERE book.title LIKE ?
                ''',
                ('%' + search_title + '%',)
            )

        # Search by AuthorID
        elif search_choice == "3":
            while True:
                try:
                    # Ask for the AuthorID
                    search_authorID = int(
                        input(
                            "\nPlease enter the 4-digit authorID for the book "
                            "you want to search for: "
                        ).strip()
                    )

                    if len(str(search_authorID)) != 4:
                        print(
                            "AuthorID must be 4 digits and cannot start with "
                            "0."
                        )
                        continue  # Reprompts user for authorID

                    # Query to search for the book
                    cursor.execute(
                        '''
                        SELECT book.id AS book_id, book.title, book.authorID,
                        book.qty, author.id AS author_id, author.name, 
                        author.country
                        FROM book 
                        JOIN author
                        ON book.authorID = author.id
                        WHERE book.authorID = ?
                        ''', 
                        (search_authorID,)
                    )
                    break  # Breaks out loop with valid AuthorID

                except ValueError:
                    print("Invalid authorID. Please try again.")

        elif search_choice == "-1":
            print("Exiting search.")
            break  # Returns to main menu

        else:
            print("Invalid choice. Please enter '1', '2', '3' or '-1'.")

        # Fetch query results
        books = cursor.fetchall()

        # Get column names from tables
        details = cursor.description
        detail = [item[0] for item in details]

        # Checks if book being searched exists
        if books:
            for book in books:
                # Create a dictionary by pairing each value with its
                # attribute and print details
                book_info = dict(zip(detail, book))
                print("-" * 30)  # Border
                print(f"ID: {book_info['book_id']}")
                print(f"Title: {book_info['title']}")
                print(
                    f"Author Name(AuthorID): {book_info['name']}"
                    f"({book_info['author_id']})"
                )
                print(f"Author Country: {book_info['country']}")
                print(f"Quantity: {book_info['qty']}")
            print("-" * 30)  # Border
        else:
            print(f'Book you are searching for does not exist')

    # Close database
    db.close()


def view_all():
    '''
    Joins the 'book' table and 'author' table by using the 'id'
    column in the 'author' table as a foreign key linking it to the
    'authorID' column in the 'book' table.

    Print out the title, author name and author country of each book.
    
    It does not save any changes to the database as nothing is being 
    modified, but it closes the database.
    '''
    # Connect to database and get cursor object
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    # Query to join tables and get specific attributes
    cursor.execute(
        '''
        SELECT book.title, author.name, author.country
        FROM book
        JOIN author
        ON book.authorID = author.id
        '''
    )

    # Fetch all the results from the query
    books = cursor.fetchall()

    # Get column names from tables
    attributes = cursor.description
    attribute = [item[0] for item in attributes]
    
    print("Book Details")
    for book in books:
        # Create a dictionary by pairing each value with its attribute
        # and print
        book_info = dict(zip(attribute, book))
        print("-" * 30)  # Border
        print(f"Title: {book_info['title']}")
        print(f"Author's Name: {book_info['name']}")
        print(f"Author's Country: {book_info['country']}")
    print("-" * 30)  # Border after last book

    # Close database
    db.close()


# Call functions to create the databases
create_db1()
create_db2()

while True:
    # Prompt user with user menu
    menu = input(
        "\nWelcome to the bookstore inventory. "
        "Please choose what you would like to do:\n"
        "1. Enter book\n"
        "2. Update book\n"
        "3. Delete book\n"
        "4. Search books\n"
        "5. View details of all books\n"
        "0. Exit\n"
    ).strip().lower()

    # Call corresponding function based on user decision
    if menu == "1":
        enter_book()  # Enter a book
    elif menu == "2":
        update_book()  # Update a book's details
    elif menu == "3":
        delete_book()  # Delete a book
    elif menu == "4":
        search_book()  # Search for a book
    elif menu == "5":
        view_all()  # View all books
    elif menu == "0":
        print("Goodbye.")
        break  # Exit
    else:
        print("Invalid menu choice. Please try again.")