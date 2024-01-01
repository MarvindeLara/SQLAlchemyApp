import datetime
import sqlalchemy
from sqlalchemy import orm
from data.sqlalchemybase import SqlAlchemyBase


class Reservation(SqlAlchemyBase):
    __tablename__ = 'reservations'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    # status: BORROWED, RETURNED, OVERDUE, CANCELLED
    status = sqlalchemy.Column(sqlalchemy.String, index=True)

    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id'), nullable=False)
    # ont-to-one
    student = orm.relationship('Student', back_populates='reservations')

    book_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id'), nullable=False)
    # ont-to-one
    book = orm.relationship('Book', back_populates='reservation')