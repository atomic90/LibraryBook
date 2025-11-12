import streamlit as st

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

# -------------------
# Estado de la aplicación
# -------------------
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "output" not in st.session_state:
    st.session_state.output = ""
if "last_borrowed_author" not in st.session_state:
    st.session_state.last_borrowed_author = ""
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"
if "total_returned" not in st.session_state:
    st.session_state.total_returned = False
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# -------------------
# Funciones de lógica
# -------------------
def log(text):
    st.session_state.output += text + "\n"

def show_book_list():
    log("\nLibrary Book List:")
    for i in range(len(book_titles)):
        log(f"{i + 1}) {book_titles[i]} — {book_authors[i]}")
    log("\nWhich book would you like to borrow? (Enter the number or 0 to exit):")

def show_borrowed_books():
    log("\nBorrowed Books:")
    for i in range(len(st.session_state.borrowed_books)):
        index = st.session_state.borrowed_books[i] - 1
        log(f"{i + 1}) {book_titles[index]} — {book_authors[index]}")
    log("\nWhich book would you like to return? (Enter the number or 0 to exit):")

def suggest_books_by_author(author_name):
    log("\nOther books by the same author you might like:")
    for i in range(len(book_titles)):
        if book_authors[i] == author_name and (i + 1) not in st.session_state.borrowed_books:
            log(f"{i + 1}) {book_titles[i]}")

# -------------------
# Interfaz Streamlit (modo consola)
# -------------------
st.title("Library Console Simulation")

# Mostrar lista inicial una vez
if not st.session_state.initialized:
    show_book_list()
    st.session_state.initialized = True

st.text_area("Console", value=st.session_state.output, height=500, key="console_output", disabled=True)
user_input = st.text_input("Input:", key="input")

if st.button("Enter") and user_input.strip() != "":
    try:
        selection = int(user_input.strip())
    except ValueError:
        log("\nInvalid input. Please enter a number.")
        st.experimental_rerun()

    if st.session_state.phase == "borrow":
        if selection == 0:
            log("\nThank you for using the library borrowing system.")
            st.session_state.phase = "return"
            if st.session_state.borrowed_books:
                show_borrowed_books()
            else:
                log("You have no borrowed books.")
            st.experimental_rerun()

        elif 1 <= selection <= len(book_titles) and selection not in st.session_state.borrowed_books:
            st.session_state.borrowed_books.append(selection)
            st.session_state.last_borrowed_author = book_authors[selection - 1]
            log(f"\nYou have borrowed: {book_titles[selection - 1]}")
            suggest_books_by_author(st.session_state.last_borrowed_author)
            show_book_list()
            st.experimental_rerun()

        elif selection in st.session_state.borrowed_books:
            log("\nYou have already borrowed this book. Please choose another.")
            show_book_list()
            st.experimental_rerun()

        else:
            log("\nInvalid selection. Please try again.")
            show_book_list()
            st.experimental_rerun()

    elif st.session_state.phase == "return":
        if len(st.session_state.borrowed_books) == 0 and not st.session_state.total_returned:
            log("You have no borrowed books.")
            st.session_state.total_returned = True
            st.experimental_rerun()

        elif len(st.session_state.borrowed_books) == 0 and st.session_state.total_returned:
            log("All books returned, Thanks for using our service.")

        else:
            if selection == 0:
                log("\nYou still have books to return.")
                log("\nThank you for returning books. Come back soon!")
                st.session_state.borrowed_books.clear()
                st.session_state.total_returned = True
                st.experimental_rerun()

            elif 1 <= selection <= len(st.session_state.borrowed_books):
                index_to_return = st.session_state.borrowed_books[selection - 1]
                log(f"\nYou have returned: {book_titles[index_to_return - 1]}")
                st.session_state.borrowed_books.pop(selection - 1)
                if len(st.session_state.borrowed_books) == 0:
                    st.session_state.total_returned = True
                    log("\nAll books returned, Thanks for using our service.")
                else:
                    show_borrowed_books()
                st.experimental_rerun()

            else:
                log("\nInvalid selection. Please try again.")
                show_borrowed_books()
                st.experimental_rerun()
