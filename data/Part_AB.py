import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class PartAB(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'part_ab'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test = relationship("Test", backref="test")

    question = sqlalchemy.Column(sqlalchemy.String)

    part = sqlalchemy.Column(sqlalchemy.CHAR)

    right_answer = sqlalchemy.Column(sqlalchemy.String)
    first = sqlalchemy.Column(sqlalchemy.String)
    second = sqlalchemy.Column(sqlalchemy.String)
    third = sqlalchemy.Column(sqlalchemy.String)
    fourth = sqlalchemy.Column(sqlalchemy.String)
    fifth = sqlalchemy.Column(sqlalchemy.String)