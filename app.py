import streamlit as st

# Datos
book_titles = [
    "1984", "To Kill a Mockingbird", "Brave New World", "Animal Farm", "The Great Gatsby", "The Land of Sweet Forever",
    "Fahrenheit 451", "Of Mice and Men", "Moby Dick", "The Catcher in the Rye", "The Old Man and the Sea"
]

book_authors = [
    "George Orwell", "Harper Lee", "Aldous Huxley", "George Orwell", "F. Scott Fitzgerald", "Harper Lee",
    "Ray Bradbury", "John Steinbeck", "Herman Melville", "J.D. Salinger", "Ernest Hemingway"
]

# Estado de la app
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "output" not in st.session_state:
    st.session_state.output = ""
if "last_borrowed_author" not in st.session_state:
    st.session_state.last_borrowed_author = ""
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"

# Funciones
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

# UI
st.title("Library Borrowing System")
st.text_area("Console Output", value=st.session_state.output, height=400, key="console", disabled=True)

if st.session_state.phase == "borrow":
    show_book_list()
    options = ["0 - Exit"] + [f"{i+1} - {book_titles[i]}" for i in range(len(book_titles))]
    selection = st.selectbox("Which book would you like to borrow?", options, key="borrow_select")
    if st.button("Submit Borrow Selection"):
        sel = int(selection.split(" ")[0])
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

elif st.session_state.phase == "return":
    if not st.session_state.borrowed_books:
        log("All books returned. Thanks for using our service.")
    else:
        show_borrowed_books()
        options = ["0 - Exit"] + [f"{i+1} - {book_titles[st.session_state.borrowed_books[i] - 1]}" for i in range(len(st.session_state.borrowed_books))]
        selection = st.selectbox("Which book would you like to return?", options, key="return_select")
        if st.button("Submit Return Selection"):
            sel = int(selection.split(" ")[0])
            if sel == 0:
                if st.session_state.borrowed_books:
                    log("\nYou still have books to return.")
                log("\nThank you for returning books. Come back soon!")
                st.session_state.borrowed_books.clear()
            elif 1 <= sel <= len(st.session_state.borrowed_books):
                index_to_return = st.session_state.borrowed_books[sel - 1]
                log(f"\nYou have returned: {book_titles[index_to_return - 1]}")
                st.session_state.borrowed_books.pop(sel - 1)
                if not st.session_state.borrowed_books:
                    log("All books returned. Thanks for using our service.")
            else:
                log("\nInvalid selection. Please try again.")