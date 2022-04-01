import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'


    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favourite_recipes = sqlalchemy.Column(sqlalchemy.String, nullable=True)