import streamlit as st

# -----------------------------
# Initialization
# -----------------------------
def init_state():
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True

    st.session_state.catalog_books = [
        "1984", "Animal Farm",
        "To Kill a Mockingbird", "Go Set a Watchman",
        "The Great Gatsby", "Tender Is the Night",
        "Pride and Prejudice", "Sense and Sensibility",
        "Moby-Dick", "Billy Budd"
    ]
    st.session_state.authors = [
        "George Orwell", "George Orwell",
        "Harper Lee", "Harper Lee",
        "F. Scott Fitzgerald", "F. Scott Fitzgerald",
        "Jane Austen", "Jane Austen",
        "Herman Melville", "Herman Melville"
    ]

    st.session_state.borrowed_books = []
    st.session_state.last_borrowed_author = ""
    st.session_state.phase = "borrow"
    st.session_state.log = []
    st.session_state.prompt_mode = None

def print_line(s=""):
    st.session_state.log.append(s)

def print_newline_then(s):
    st.session_state.log.append("")
    st.session_state.log.append(s)

def render_console(placeholder):
    placeholder.code("\n".join(st.session_state.log), language=None)

# -----------------------------
# Printing helpers
# -----------------------------
def print_catalog_and_prompt():
    print_newline_then("Book Catalog:")
    for i, title in enumerate(st.session_state.catalog_books):
        a = st.session_state.authors[i]
        print_line(f"{i + 1}) {title} by {a}")
    print_newline_then("Which book would you like to borrow (enter the number or '0' to exit)?")
    st.session_state.prompt_mode = "borrow"

def print_borrowed_list_and_prompt():
    borrowed = st.session_state.borrowed_books
    catalog = st.session_state.catalog_books
    authors = st.session_state.authors

    print_newline_then("Borrowed Books:")
    for i in range(len(borrowed)):
        book = catalog[borrowed[i] - 1]
        author = authors[borrowed[i] - 1]
        print_line(f"{i + 1}) {book} by {author}")
    print_newline_then("Which book would you like to return (enter the number or '0' to exit)?")
    st.session_state.prompt_mode = "return"

# -----------------------------
# Borrow Phase
# -----------------------------
def process_borrow_input(user_text):
    try:
        selection = int(user_text.strip())
    except Exception:
        print_newline_then("Invalid book number. Please try again.")
        print_catalog_and_prompt()
        return

    catalog = st.session_state.catalog_books
    authors = st.session_state.authors
    borrowed = st.session_state.borrowed_books

    if selection == 0:
        print_newline_then("Thank you for using our library service. See you soon!")
        st.session_state.phase = "return"
        if len(borrowed) == 0:
            print_line("You have not borrowed books.")
            st.session_state.phase = "done"
            st.session_state.prompt_mode = None
            st.rerun()
        else:
            print_borrowed_list_and_prompt()
            st.rerun()
        return

    if 1 <= selection <= len(catalog) and selection not in borrowed:
        borrowed.append(selection)
        st.session_state.last_borrowed_author = authors[selection - 1]
        print_newline_then("You have borrowed " + catalog[selection - 1])

        print_newline_then("Other books by the same author:")
        for i in range(len(catalog)):
            current = i + 1
            if authors[i] == st.session_state.last_borrowed_author and current not in borrowed:
                print_line(f"{current}) {catalog[i]}")

        print_catalog_and_prompt()
        return

    elif selection in borrowed:
        print_newline_then("You have already borrowed this book. Please try again.")
        print_catalog_and_prompt()
        return

    else:
        print_newline_then("Invalid book number. Please try again.")
        print_catalog_and_prompt()
        return

def borrow_phase():
    console_placeholder = st.empty()

    if st.session_state.prompt_mode != "borrow":
        print_catalog_and_prompt()

    render_console(console_placeholder)

    with st.form("borrow_form", clear_on_submit=True):
        user_text = st.text_input("", key="borrow_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_borrow_input(user_text)
        render_console(console_placeholder)

# -----------------------------
# Return Phase
# -----------------------------
def process_return_input(user_text):
    try:
        selection = int(user_text.strip())
    except Exception:
        print_newline_then("Invalid book number. Please try again.")
        print_borrowed_list_and_prompt()
        return

    borrowed = st.session_state.borrowed_books
    catalog = st.session_state.catalog_books

    if selection == 0:
        st.session_state.phase = "done"
        print_newline_then("Thank you for using our returning service. See you soon!")
        st.session_state.prompt_mode = None
        st.rerun()
        return

    if 1 <= selection <= len(borrowed):
        title = catalog[borrowed[selection - 1] - 1]
        print_newline_then("You have returned " + title)
        borrowed.pop(selection - 1)

        if len(borrowed) == 0:
            print_line("You have not borrowed books.")
            st.session_state.phase = "done"
            st.session_state.prompt_mode = None
            st.rerun()
            return
        else:
            print_borrowed_list_and_prompt()
            return
    else:
        print_newline_then("Invalid book number. Please try again.")
        print_borrowed_list_and_prompt()
        return

def return_phase():
    console_placeholder = st.empty()

    if len(st.session_state.borrowed_books) == 0:
        print_line("You have not borrowed books.")
        st.session_state.phase = "done"
        st.session_state.prompt_mode = None
        render_console(console_placeholder)
        return

    if st.session_state.prompt_mode != "return":
        print_borrowed_list_and_prompt()

    render_console(console_placeholder)

    with st.form("return_form", clear_on_submit=True):
        user_text = st.text_input("", key="return_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_return_input(user_text)
        render_console(console_placeholder)

# -----------------------------
# App Entry
# -----------------------------
st.set_page_config(page_title="Library Borrowing System", layout="centered")
st.title("Library Borrowing")

init_state()

if st.session_state.phase == "borrow":
    borrow_phase()
elif st.session_state.phase == "return":
    return_phase()
else:
    st.code("\n".join(st.session_state.log), language=None)