import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class PartC(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'part_c'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test = relationship("Test", backref="test")

    question = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)