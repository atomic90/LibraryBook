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
if "step" not in st.session_state:
    st.session_state.step = "show_menu"

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
# Interfaz
# -------------------
st.title("Library Console App")
st.text_area("Console", value=st.session_state.output, height=500, disabled=True)

with st.form("console_form"):
    user_input = st.text_input("", label_visibility="collapsed")
    submitted = st.form_submit_button("Enter")

if submitted:
    try:
        choice = int(user_input.strip())
    except ValueError:
        log("\nInvalid input. Please enter a number.")
        st.stop()

    if st.session_state.phase == "borrow":
        if st.session_state.step == "show_menu":
            if choice == 0:
                log("\nThank you for using the library borrowing system.")
                st.session_state.phase = "return"
                st.session_state.step = "show_menu"
            elif 1 <= choice <= len(book_titles) and choice not in st.session_state.borrowed_books:
                st.session_state.borrowed_books.append(choice)
                st.session_state.last_author = book_authors[choice - 1]
                log(f"\nYou have borrowed: {book_titles[choice - 1]}")
                suggest_books_by_author(st.session_state.last_author)
            elif choice in st.session_state.borrowed_books:
                log("\nYou have already borrowed this book. Please choose another.")
            else:
                log("\nInvalid selection. Please try again.")

            # Show the menu again
            show_book_list()
            log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")

    elif st.session_state.phase == "return":
        if st.session_state.step == "show_menu":
            if len(st.session_state.borrowed_books) == 0:
                log("\nAll books returned. Thanks for using our service.")
                st.stop()
            if choice == 0:
                log("\nYou still have books to return.")
                log("\nThank you for returning books. Come back soon!")
                st.session_state.borrowed_books.clear()
            elif 1 <= choice <= len(st.session_state.borrowed_books):
                idx = st.session_state.borrowed_books.pop(choice - 1)
                log(f"\nYou have returned: {book_titles[idx - 1]}")
                if len(st.session_state.borrowed_books) == 0:
                    log("\nAll books returned. Thanks for using our service.")
            else:
                log("\nInvalid selection. Please try again.")

            # Show the return menu again
            if st.session_state.borrowed_books:
                show_borrowed_books()
                log("\nWhich book would you like to return? (Enter number or 0 to exit):")

# Primera visualización sin input
if not submitted:
    if st.session_state.phase == "borrow" and st.session_state.output == "":
        show_book_list()
        log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")
    elif st.session_state.phase == "return" and st.session_state.output == "":
        if len(st.session_state.borrowed_books) > 0:
            show_borrowed_books()
            log("\nWhich book would you like to return? (Enter number or 0 to exit):")
        else:
            log("\nYou have no borrowed books.")
