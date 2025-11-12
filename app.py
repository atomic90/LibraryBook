import streamlit as st

# ----------------------
# Datos iniciales
# ----------------------
book_titles = [
    "1984", "To Kill a Mockingbird", "Brave New World", "Animal Farm", "The Great Gatsby", "The Land of Sweet Forever",
    "Fahrenheit 451", "Of Mice and Men", "Moby Dick", "The Catcher in the Rye", "The Old Man and the Sea"
]

book_authors = [
    "George Orwell", "Harper Lee", "Aldous Huxley", "George Orwell", "F. Scott Fitzgerald", "Harper Lee",
    "Ray Bradbury", "John Steinbeck", "Herman Melville", "J.D. Salinger", "Ernest Hemingway"
]

# ----------------------
# Estado de la aplicación
# ----------------------
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "output" not in st.session_state:
    st.session_state.output = ""
if "last_borrowed_author" not in st.session_state:
    st.session_state.last_borrowed_author = ""
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"
if "awaiting_input" not in st.session_state:
    st.session_state.awaiting_input = True

# ----------------------
# Funciones
# ----------------------
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

# ----------------------
# UI Simulación de consola
# ----------------------
st.title("Library System - Console Mode")
st.text_area("Console", value=st.session_state.output, height=500, key="console_output", disabled=True)

user_input = st.text_input("Input:", key="input")

if st.button("Enter") and user_input.strip() != "":
    try:
        sel = int(user_input.strip())
    except ValueError:
        log("\nInvalid input. Please enter a number.")
        st.stop()

    # ----------------------
    # Fase de préstamo
    # ----------------------
    if st.session_state.phase == "borrow":
        if sel == 0:
            log("\nThank you for using the library borrowing system.")
            st.session_state.phase = "return"
        elif 1 <= sel <= len(book_titles) and sel not in st.session_state.borrowed_books:
            st.session_state.borrowed_books.append(sel)
            st.session_state.last_borrowed_author = book_authors[sel - 1]
            log(f"\nYou have borrowed: {book_titles[sel - 1]}")
            suggest_books_by_author(st.session_state.last_borrowed_author)
        elif sel in st.session_state.borrowed_books:
            log("\nYou have already borrowed this book. Please choose another.")
        else:
            log("\nInvalid selection. Please try again.")
        show_book_list()

    # ----------------------
    # Fase de devolución
    # ----------------------
    elif st.session_state.phase == "return":
        if not st.session_state.borrowed_books:
            log("\nAll books returned. Thanks for using our service.")
        elif sel == 0:
            if st.session_state.borrowed_books:
                log("\nYou still have books to return.")
            log("\nThank you for returning books. Come back soon!")
            st.session_state.borrowed_books.clear()
        elif 1 <= sel <= len(st.session_state.borrowed_books):
            index_to_return = st.session_state.borrowed_books[sel - 1]
            log(f"\nYou have returned: {book_titles[index_to_return - 1]}")
            st.session_state.borrowed_books.pop(sel - 1)
            if not st.session_state.borrowed_books:
                log("\nAll books returned. Thanks for using our service.")
        else:
            log("\nInvalid selection. Please try again.")
        if st.session_state.borrowed_books:
            show_borrowed_books()

    st.experimental_rerun()

# Primera ejecución
if st.session_state.output == "":
    show_book_list()