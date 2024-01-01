import datetime
import sqlalchemy
from sqlalchemy import orm
from data.sqlalchemybase import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    isbn = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True)
    author = sqlalchemy.Column(sqlalchemy.String, index=True)
    publisher = sqlalchemy.Column(sqlalchemy.String, index=True)
    purchased_price = sqlalchemy.Column(sqlalchemy.Float, index=True)
    ratings = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    available = sqlalchemy.Column(sqlalchemy.Boolean, index=True)

    library_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('libraries.id'), nullable=False)
    # ont-to-one
    library = orm.relationship('Library', back_populates='books')
    # one-to-one
    reservation = orm.relationship('Reservation', back_populates='book')
