# -------------------
# Book Catalog and Authors
# -------------------
book_titles = [
    "1984", "To Kill a Mockingbird", "Brave New World", "Animal Farm", "The Great Gatsby", "The Land of Sweet Forever",
    "Fahrenheit 451", "Of Mice and Men", "Moby Dick", "The Catcher in the Rye", "The Old Man and the Sea"
]

book_authors = [
    "George Orwell", "Harper Lee", "Aldous Huxley", "George Orwell", "F. Scott Fitzgerald", "Harper Lee",
    "Ray Bradbury", "John Steinbeck", "Herman Melville", "J.D. Salinger", "Ernest Hemingway"
]

borrowed_books = []

# -------------------
# ----- FUNCTIONS -----
# -------------------
# Basic functions, without calling each other

def show_book_list():
    print("\nLibrary Book List:")
    for i in range(len(book_titles)):
        print(str(i + 1) + ") " + book_titles[i] + " — " + book_authors[i])

# show_book_list()

def show_borrowed_books():
    print("\nBorrowed Books:")
    for i in range(len(borrowed_books)):
        index = borrowed_books[i] - 1
        print(str(i + 1) + ") " + book_titles[index] + " — " + book_authors[index])

# show_borrowed_books()

def suggest_books_by_author(author_name):
    print("\nOther books by the same author you might like:")
    for i in range(len(book_titles)):
        if book_authors[i] == author_name and (i + 1) not in borrowed_books:
            print(str(i + 1) + ") " + book_titles[i])

# suggest_books_by_author("George Orwell")


# -----------------------------
# ----- MAIN PROGRAM FLOW -----
# -----------------------------

# Part 1: Borrowing books
finished = False
last_borrowed_author = ""

while not finished:
    show_book_list()
    selection = int(input("\nWhich book would you like to borrow? (Enter the number or 0 to exit): "))

    if selection == 0:
        finished = True
        print("\nThank you for using the library borrowing system.")
    elif selection >= 1 and selection <= len(book_titles) and selection not in borrowed_books:
        borrowed_books.append(selection)
        last_borrowed_author = book_authors[selection - 1]
        print("\nYou have borrowed: " + book_titles[selection - 1])
        suggest_books_by_author(last_borrowed_author)
    elif selection in borrowed_books:
        print("\nYou have already borrowed this book. Please choose another.")
    else:
        print("\nInvalid selection. Please try again.")

# Part 2: Returning books
finished = False
total_returned = False
while not finished:
    if len(borrowed_books) == 0 and total_returned == False:
      print("You have no borrowed books.")
      finished = True
    elif len(borrowed_books) == 0 and total_returned == True:
       print("All books returned, Thanks for using our service.")
       finished = True
    else:
        show_borrowed_books()
        selection = int(input("\nWhich book would you like to return? (Enter the number or 0 to exit): "))

        if selection == 0:
            if len(borrowed_books) > 0:
                print("\nYou still have books to return.")
            finished = True
            print("\nThank you for returning books. Come back soon!")
        elif selection >= 1 and selection <= len(borrowed_books):
            index_to_return = borrowed_books[selection - 1]
            print("\nYou have returned: " + book_titles[index_to_return - 1])
            borrowed_books.pop(selection - 1)
            if len(borrowed_books) == 0:
              total_returned = True
        else:
            print("\nInvalid selection. Please try again.")