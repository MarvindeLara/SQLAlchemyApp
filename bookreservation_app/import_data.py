import datetime
import random

from data import session_factory
from data.models.books import Book
from data.models.libraries import Library
from data.models.reservations import Reservation
from data.models.students import Student
from services import crud_services


def import_if_empty():
    __import_students()
    __import_libraries()
    __import_books()
    # __import_reservations() don't need this, just add reservations through main.py


def __import_students():
    session = session_factory.create_session()
    if session.query(Student).count() > 0:
        return

    crud_services.get_active_student()

    student = Student()
    student.student_number = '301091992'
    student.full_name = 'James DeLara'
    student.email = 'james.swdev@gmail.com'
    student.hashed_password = '5678'
    session.add(student)

    session.commit()


def __import_libraries():
    session = session_factory.create_session()
    if session.query(Library).count() > 0:
        return

    library = Library()
    library.name = 'Toronto Public Library - Eglinton'
    library.address = '2380 Eglinton Ave'
    session.add(library)

    library = Library()
    library.name = 'Toronto Public Library - Birchmount'
    library.address = '496 Birchmount Rd'
    session.add(library)

    library = Library()
    library.name = 'Toronto Public Library - Lawrence'
    library.address = '2219 Lawrence Ave E'
    session.add(library)

    session.commit()


def __import_books():
    session = session_factory.create_session()
    if session.query(Book).count() > 0:
        return

    isbn_values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    titles = [
        'Python, C, C++, SQL',
        'HTML5',
        'CSS - Bootstrap 5',
        'SQLAlchemy ORM',
        'SQLAlchemy Core',
        'Pyramid',
        'Flask',
        'Django',
        'Docker',
        'Javascript - Vue.js',
        'Anvil',
        'PyQT5 and Socket Programming',
        'Ignition Perspective, MQTT, Kedro, BIRT',
        'Data Structures and Algorithms',
        'Numpy, Pandas, Data Visualization',
        'Machine Learning',
        'Artificial Intelligence',
    ]
    libraries = list(session.query(Library).all())
    # libraries = libraries.append(None) can't add None in choices since it calls len on each choice

    COUNT = 17
    for _ in range(0, COUNT):
        book = Book()
        book.isbn = ''.join((random.choice(isbn_values) for _ in range(0, 16)))
        selected = random.choice(titles)
        book.title = selected
        titles.remove(selected)
        book.author = "Marvin DeLara"
        book.publisher = "Talk Python"
        book.purchased_price = 89.99
        book.ratings = 99
        # book.available = random.choice([True, False])
        book.available = True
        book.library = random.choice(libraries)

        session.add(book)

    session.commit()
