import streamlit as st

# -------------------
# Catálogo
# -------------------
book_titles = [
    "1984", "To Kill a Mockingbird", "Brave New World", "Animal Farm", "The Great Gatsby", "The Land of Sweet Forever",
    "Fahrenheit 451", "Of Mice and Men", "Moby Dick", "The Catcher in the Rye", "The Old Man and the Sea"
]
book_authors = [
    "George Orwell", "Harper Lee", "Aldous Huxley", "George Orwell", "F. Scott Fitzgerald", "Harper Lee",
    "Ray Bradbury", "John Steinbeck", "Herman Melville", "J.D. Salinger", "Ernest Hemingway"
]

# -------------------
# Estado
# -------------------
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "output" not in st.session_state:
    st.session_state.output = ""
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"
if "last_author" not in st.session_state:
    st.session_state.last_author = ""
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# -------------------
# Funciones
# -------------------
def log(text):
    st.session_state.output += text + "\n"

def show_book_list():
    log("\nLibrary Book List:")
    for i, (title, author) in enumerate(zip(book_titles, book_authors)):
        log(f"{i + 1}) {title} — {author}")

def show_borrowed_books():
    log("\nBorrowed Books:")
    for i, idx in enumerate(st.session_state.borrowed_books):
        log(f"{i + 1}) {book_titles[idx - 1]} — {book_authors[idx - 1]}")

def suggest_books_by_author(author_name):
    log("\nOther books by the same author you might like:")
    for i in range(len(book_titles)):
        if book_authors[i] == author_name and (i + 1) not in st.session_state.borrowed_books:
            log(f"{i + 1}) {book_titles[i]}")

# -------------------
# Primera ejecución
# -------------------
if st.session_state.output == "" and st.session_state.phase == "borrow":
    show_book_list()
    log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")

elif st.session_state.output == "" and st.session_state.phase == "return":
    if st.session_state.borrowed_books:
        show_borrowed_books()
        log("\nWhich book would you like to return? (Enter number or 0 to exit):")
    else:
        log("You have no borrowed books.")

# -------------------
# Mostrar consola y entrada
# -------------------
st.title("Library Console App")
st.text_area("Console", value=st.session_state.output, height=500, disabled=True)

input_key = f"input_{st.session_state.input_counter}"
user_input = st.text_input("", key=input_key)

if st.button("Submit") and user_input.strip() != "":
    try:
        choice = int(user_input.strip())
    except ValueError:
        log("\nInvalid input. Please enter a number.")
        st.session_state.input_counter += 1
        st.stop()

    if st.session_state.phase == "borrow":
        if choice == 0:
            log("\nThank you for using the library borrowing system.")
            st.session_state.phase = "return"
            if st.session_state.borrowed_books:
                show_borrowed_books()
                log("\nWhich book would you like to return? (Enter number or 0 to exit):")
            else:
                log("\nYou have no borrowed books.")
        elif 1 <= choice <= len(book_titles) and choice not in st.session_state.borrowed_books:
            st.session_state.borrowed_books.append(choice)
            st.session_state.last_author = book_authors[choice - 1]
            log(f"\nYou have borrowed: {book_titles[choice - 1]}")
            suggest_books_by_author(st.session_state.last_author)
            show_book_list()
            log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")
        elif choice in st.session_state.borrowed_books:
            log("\nYou have already borrowed this book. Please choose another.")
            show_book_list()
            log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")
        else:
            log("\nInvalid selection. Please try again.")
            show_book_list()
            log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")

    elif st.session_state.phase == "return":
        if choice == 0:
            if st.session_state.borrowed_books:
                log("\nYou still have books to return.")
            log("\nThank you for returning books. Come back soon!")
        elif 1 <= choice <= len(st.session_state.borrowed_books):
            index = st.session_state.borrowed_books[choice - 1]
            log(f"\nYou have returned: {book_titles[index - 1]}")
            st.session_state.borrowed_books.pop(choice - 1)
            if st.session_state.borrowed_books:
                show_borrowed_books()
                log("\nWhich book would you like to return? (Enter number or 0 to exit):")
            else:
                log("\nAll books returned. Thanks for using our service.")
        else:
            log("\nInvalid selection. Please try again.")
            show_borrowed_books()
            log("\nWhich book would you like to return? (Enter number or 0 to exit):")

    st.session_state.input_counter += 1