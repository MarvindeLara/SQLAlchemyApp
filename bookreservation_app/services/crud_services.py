import datetime

from data import session_factory
from data.models.books import Book
from data.models.reservations import Reservation
from data.models.students import Student
from typing import List, Any
from sqlalchemy import text


def get_active_student():
    session = session_factory.create_session()

    student = session.query(Student).filter(Student.email == 'marvin.swdev@gmail.com').first()
    if student:
        return student

    # C in CRUD
    student = Student()
    student.student_number = '301091991'
    student.full_name = 'Marvin DeLara'
    student.email = 'marvin.swdev@gmail.com'
    student.hashed_password = '1234'
    session.add(student)

    session.commit()

    return student


def get_active_reservations(student: Student):
    session = session_factory.create_session()

    reservations = session.query(Reservation).filter(Reservation.student_id == student.id,
                                                     Reservation.status == 'BORROWED').all()

    return list(reservations)


# TODO: use case for deleting a row (although not advisable)
# reservation = session.query(Reservation).filter(Reservation.id == reservation.id).one()
# session.delete(reservation)
# TODO: bulk update to set status to OVERDUE
def update_reservations(student: Student):
    session = session_factory.create_session()

    reservations = session.query(Reservation).filter(Reservation.student.id == student.id).all()
    session.commit()

    return reservations


def available_books() -> List[Book]:
    session = session_factory.create_session()

    # R in CRUD
    books = session.query(Book).filter(Book.available == True).all()

    # noinspection PyComparisonWithNone
    # books = session.query(Book).filter(Book.library_id != None).all()

    return list(books)


def reserved_books() -> List[Book]:
    session = session_factory.create_session()

    books = session.query(Book).filter(Book.available == False).all()

    return list(books)


def reserve_book(student: Student, book: Book, start_date: datetime.datetime) -> Reservation:
    session = session_factory.create_session()

    book = session.query(Book).filter(Book.id == book.id).one()
    book.available = False

    session.commit()

    session = session_factory.create_session()

    reservation = Reservation()
    reservation.start_date = start_date
    reservation.end_date = reservation.start_date + datetime.timedelta(days=7)
    reservation.status = 'BORROWED'
    reservation.student = student
    book = session.query(Book).filter(Book.id == book.id).one()
    reservation.book = book

    session.add(reservation)

    session.commit()

    return reservation


def update_reservation(student: Student, reservation: Reservation, status: str) -> Reservation:
    session = session_factory.create_session()

    # U in CRUD
    reservation = session.query(Reservation).filter(Reservation.id == reservation.id).one()
    reservation.status = status
    reservation.book.available = True

    session.commit()

    return reservation


def extend_reservation(student: Student, reservation: Reservation, extension: int) -> Reservation:
    session = session_factory.create_session()

    # U in CRUD
    reservation = session.query(Reservation).filter(Reservation.id == reservation.id).one()
    reservation.end_date = reservation.end_date + datetime.timedelta(days=7)

    session.commit()

    return reservation


def execute_sql_statement(sql: str) -> List[Any]:
    session = session_factory.create_session()

    statement = text(sql)
    results = session.execute(statement)

    # statement = text("""
    # SELECT students.student_number, students.full_name, students.email,
    # books.isbn, books.title, libraries.name
    # FROM students
    # JOIN reservations
    # ON students.id = reservations.student_id AND reservations.status = 'BORROWED'
    # JOIN books
    # ON reservations.book_id = books.id
    # JOIN libraries
    # ON books.library_id = libraries.id
    # WHERE students.id = :id;
    # """)
    # results = session.execute(statement, {'id': 1})

    # statement = text("""
    #     SELECT books.id, reservations.status, reservations.start_date, reservations.end_date,
    #     books.isbn, books.title, libraries.name,
    #     students.student_number, students.full_name, students.email
    #     FROM reservations
    #     JOIN books
    #     ON reservations.book_id = books.id
    #     JOIN libraries
    #     ON books.library_id = libraries.id
    #     JOIN students
    #     ON students.id = reservations.student_id
    #     WHERE books.id IN (:id1, :id2, :id3, :id4, :id5);
    #     """)
    # results = session.execute(statement, {'id1': 8, 'id2': 9, 'id3': 17, 'id4': None, 'id5': None})

    session.commit()

    return list(results)
