import datetime
import sys

import import_data
from data import session_factory
from data.models.students import Student
from services import crud_services

__student: Student = None


def main():
    setup_db()

    options = 'Enter a command, [r]eserve, [a]vailable_books, all_[b]ooks, [h]istory, re[t]urn, [e]xtend, [c]ancel, s[q]l_statement, e[x]it: '
    option = "NOT SET"

    while option:
        option = input(options).lower().strip()
        if option == 'r':
            reserve_a_book()
        elif option == 'a':
            show_available_books()
        elif option == 'b':
            show_all_books()
        elif option == 'h':
            my_reservations()
        elif option == 't':
            return_reservation()
        elif option == 'e':
            extend_reservation()
        elif option == 'c':
            cancel_reservation()
        elif option == 'q':
            execute_sql_statement()
        elif option == 'x':
            exit_app()


def setup_db():
    global __student

    session_factory.global_init("book_reservations.sqlite")
    session_factory.create_tables()
    import_data.import_if_empty()
    __student = crud_services.get_active_student()
    print("\nActive student - {}\n".format(__student.email))


def reserve_a_book():
    available_books = show_available_books()
    selected = int(input('Enter a book number: ')) - 1

    if not (0 <= selected or selected < len(available_books)):
        print("\nError: Pick another book_number.")
        return

    book = available_books[selected]

    crud_services.reserve_book(__student, book, datetime.datetime.now())


def show_available_books():
    print("********* Show available books *********\n")
    available_books = crud_services.available_books()
    for idx, b in enumerate(available_books, start=1):
        print("#{:02d}. {:45s} {}% @{:35s} - {}".format(idx, b.title, b.ratings, b.library.name, b.library.address))
    print("\n****************************************")
    return available_books


def show_all_books():
    print("********* Show all books *********\n")
    available_books = crud_services.available_books()
    for idx, b in enumerate(available_books, start=1):
        print("AVAILABLE {:45s} {}% @{:35s} - {}".format(b.title, b.ratings, b.library.name, b.library.address))
    reserved_books = crud_services.reserved_books()
    for idx, b in enumerate(reserved_books, start=1):
        print("RESERVED  {:45s} {}% @{:35s} - {}".format(b.title, b.ratings, b.library.name, b.library.address))
    print("\n**********************************")


def my_reservations():
    print("********* My reservations *********\n")
    student = crud_services.get_active_student()
    for r in student.reservations:
        print("{:10s} {:45s} {:45s} {:25s} {:25s}".format(r.status, r.book.title, r.book.library.name,
                                                          r.start_date.date().isoformat(),
                                                          r.end_date.date().isoformat()))
    print("\n***********************************")


def return_reservation():
    update_reservation('RETURNED')


def extend_reservation():
    print("********* My reservations *********\n")
    student = crud_services.get_active_student()
    reservations = crud_services.get_active_reservations(student)
    for idx, r in enumerate(reservations, start=1):
        print("#{:02d}. {:10s} {:45s} {:45s} {:25s} {:25s}".format(idx, r.status, r.book.title, r.book.library.name,
                                                                   r.start_date.date().isoformat(),
                                                                   r.end_date.date().isoformat()))
    print("\n***********************************")
    selected = int(input('Enter a book number: ')) - 1

    if not (0 <= selected or selected < len(reservations)):
        print("\nError: Pick another book_number.")
        return

    reservation = reservations[selected]

    # default to 7 day extension
    crud_services.extend_reservation(student, reservation, 7)
    my_reservations()


def cancel_reservation():
    update_reservation('CANCELLED')


def update_reservation(status):
    print("********* My reservations *********\n")
    student = crud_services.get_active_student()
    reservations = crud_services.get_active_reservations(student)
    for idx, r in enumerate(reservations, start=1):
        print("#{:02d}. {:10s} {:45s} {:45s} {:25s} {:25s}".format(idx, r.status, r.book.title, r.book.library.name,
                                                                   r.start_date.date().isoformat(),
                                                                   r.end_date.date().isoformat()))
    print("\n***********************************")
    selected = int(input('Enter a book number: ')) - 1

    if not (0 <= selected or selected < len(reservations)):
        print("\nError: Pick another book_number.")
        return

    reservation = reservations[selected]

    crud_services.update_reservation(student, reservation, status)
    my_reservations()


def execute_sql_statement():
    sql = input('\nEnter a SQL statement: ')
    results = crud_services.execute_sql_statement(sql)

    print("********* SQL statement results *********\n")
    for r in results:
        print (r)
    print("*****************************************\n")


def exit_app():
    print("")
    print("\nExiting book reservation app...")
    sys.exit(0)


if __name__ == '__main__':
    main()
