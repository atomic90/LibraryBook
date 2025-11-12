import streamlit as st

# -------------------
# Book Data
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
# Initialize State
# -------------------
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "phase" not in st.session_state:
    st.session_state.phase = "borrow"
if "step" not in st.session_state:
    st.session_state.step = "show_menu"
if "output" not in st.session_state:
    st.session_state.output = ""
if "last_author" not in st.session_state:
    st.session_state.last_author = ""

# -------------------
# Helper Functions
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

def suggest_books_by_author(author):
    log("\nOther books by the same author you might like:")
    for i, auth in enumerate(book_authors):
        if auth == author and (i + 1) not in st.session_state.borrowed_books:
            log(f"{i + 1}) {book_titles[i]}")

# -------------------
# Display Console and Input
# -------------------
st.title("Library Console App")
st.text_area("Console", value=st.session_state.output, height=500, disabled=True)

with st.form("input_form"):
    user_input = st.text_input("", label_visibility="collapsed")
    submitted = st.form_submit_button("Enter")

# -------------------
# Main Logic
# -------------------
if st.session_state.phase == "borrow":
    if st.session_state.step == "show_menu":
        show_book_list()
        log("\nWhich book would you like to borrow? (Enter number or 0 to exit):")
        st.session_state.step = "await_input"

    elif st.session_state.step == "await_input" and submitted:
        try:
            choice = int(user_input.strip())
        except:
            log("\nInvalid input. Please enter a number.")
            st.session_state.step = "show_menu"
            st.stop()

        if choice == 0:
            log("\nThank you for using the library borrowing system.")
            st.session_state.phase = "return"
            st.session_state.step = "show_menu"

        elif 1 <= choice <= len(book_titles):
            if choice in st.session_state.borrowed_books:
                log("\nYou have already borrowed this book. Please choose another.")
            else:
                st.session_state.borrowed_books.append(choice)
                st.session_state.last_author = book_authors[choice - 1]
                log(f"\nYou have borrowed: {book_titles[choice - 1]}")
                suggest_books_by_author(st.session_state.last_author)
            st.session_state.step = "show_menu"
        else:
            log("\nInvalid selection. Please try again.")
            st.session_state.step = "show_menu"

elif st.session_state.phase == "return":
    if st.session_state.step == "show_menu":
        if not st.session_state.borrowed_books:
            log("\nAll books returned. Thanks for using our service.")
        else:
            show_borrowed_books()
            log("\nWhich book would you like to return? (Enter number or 0 to exit):")
            st.session_state.step = "await_input"

    elif st.session_state.step == "await_input" and submitted:
        try:
            choice = int(user_input.strip())
        except:
            log("\nInvalid input. Please enter a number.")
            st.session_state.step = "show_menu"
            st.stop()

        if choice == 0:
            log("\nYou still have books to return.")
            log("\nThank you for returning books. Come back soon!")
            st.session_state.borrowed_books.clear()
        elif 1 <= choice <= len(st.session_state.borrowed_books):
            index = st.session_state.borrowed_books.pop(choice - 1)
            log(f"\nYou have returned: {book_titles[index - 1]}")
        else:
            log("\nInvalid selection. Please try again.")
        st.session_state.step = "show_menu"
