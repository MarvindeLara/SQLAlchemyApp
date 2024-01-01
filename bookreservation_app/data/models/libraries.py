import datetime
import sqlalchemy
from sqlalchemy import orm
from data.sqlalchemybase import SqlAlchemyBase


class Library(SqlAlchemyBase):
    __tablename__ = 'libraries'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    address = sqlalchemy.Column(sqlalchemy.String, index=True)

    # many-to-one
    books = orm.relationship('Book', back_populates='library')
