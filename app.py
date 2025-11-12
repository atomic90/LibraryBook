import streamlit as st

# -------------------
# Datos del catálogo
# -------------------
book_titles = [
    "1984", "To Kill a Mockingbird", "Brave New World", "Animal Farm", "The Great Gatsby",
    "The Land of Sweet Forever", "Fahrenheit 451", "Of Mice and Men", "Moby Dick",
    "The Catcher in the Rye", "The Old Man and the Sea"
]
book_authors = [
    "George Orwell", "Harper Lee", "Aldous Huxley", "George Orwell", "F. Scott Fitzgerald",
    "Harper Lee", "Ray Bradbury", "John Steinbeck", "Herman Melville",
    "J.D. Salinger", "Ernest Hemingway"
]

# -------------------
# Estado inicial
# -------------------
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"
if "output" not in st.session_state:
    st.session_state.output = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "last_author" not in st.session_state:
    st.session_state.last_author = ""
if "show_menu" not in st.session_state:
    st.session_state.show_menu = True

# -------------------
# Funciones
# -------------------
def log(text):
    st.session_state.output += text + "\n"

def show_book_list():
    log("\nLibrary Book List:")
    for i, (title, author) in enumerate(zip(book_titles, book_authors)):
        log(f"{i + 1}) {title} — {author}")
    log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")

def show_borrowed_books():
    log("\nBorrowed Books:")
    for i, idx in enumerate(st.session_state.borrowed_books):
        log(f"{i + 1}) {book_titles[idx - 1]} — {book_authors[idx - 1]}")
    log("\nWhich book would you like to return? (Enter number or 0 to exit):")

def suggest_books_by_author(author):
    log("\nOther books by the same author you might like:")
    for i, auth in enumerate(book_authors):
        if auth == author and (i + 1) not in st.session_state.borrowed_books:
            log(f"{i + 1}) {book_titles[i]}")

# -------------------
# Mostrar salida y entrada
# -------------------
st.title("Library Console App")
st.text_area("Console", value=st.session_state.output, height=500, disabled=True)

with st.form("input_form"):
    user_input = st.text_input("", value="", label_visibility="collapsed")
    submitted = st.form_submit_button("Enter")

# -------------------
# Mostrar menú si es necesario
# -------------------
if st.session_state.show_menu:
    if st.session_state.phase == "borrow":
        show_book_list()
    elif st.session_state.phase == "return":
        if st.session_state.borrowed_books:
            show_borrowed_books()
        else:
            log("\nAll books returned. Thanks for using our service.")
    st.session_state.show_menu = False

# -------------------
# Procesar entrada si se ha enviado
# -------------------
if submitted and user_input.strip() != "":
    try:
        selection = int(user_input.strip())
    except ValueError:
        log("\nInvalid input. Please enter a number.")
        st.session_state.show_menu = True
        st.stop()

    if st.session_state.phase == "borrow":
        if selection == 0:
            log("\nThank you for using the library borrowing system.")
            st.session_state.phase = "return"
            st.session_state.show_menu = True

        elif 1 <= selection <= len(book_titles):
            if selection in st.session_state.borrowed_books:
                log("\nYou have already borrowed this book. Please choose another.")
            else:
                st.session_state.borrowed_books.append(selection)
                st.session_state.last_author = book_authors[selection - 1]
                log(f"\nYou have borrowed: {book_titles[selection - 1]}")
                suggest_books_by_author(st.session_state.last_author)
            st.session_state.show_menu = True
        else:
            log("\nInvalid selection. Please try again.")
            st.session_state.show_menu = True

    elif st.session_state.phase == "return":
        if not st.session_state.borrowed_books:
            log("\nYou have no borrowed books.")
        elif selection == 0:
            log("\nYou still have books to return.")
            log("\nThank you for returning books. Come back soon!")
            st.session_state.borrowed_books.clear()
        elif 1 <= selection <= len(st.session_state.borrowed_books):
            index = st.session_state.borrowed_books.pop(selection - 1)
            log(f"\nYou have returned: {book_titles[index - 1]}")
            if not st.session_state.borrowed_books:
                log("\nAll books returned. Thanks for using our service.")
        else:
            log("\nInvalid selection. Please try again.")
        st.session_state.show_menu = True
