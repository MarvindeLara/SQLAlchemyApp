import datetime
import sqlalchemy
from sqlalchemy import orm

from data.models.reservations import Reservation
from data.sqlalchemybase import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    student_number = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    full_name = sqlalchemy.Column(sqlalchemy.String, index=True)
    # for demo, email and password are set to nullable (allows nulls)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    last_login = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    # many-to-one
    reservations = orm.relationship('Reservation', order_by=[Reservation.start_date.desc()], back_populates='student')
