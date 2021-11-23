import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Test(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    results = orm.relation("Result", back_populates='test')

    results_table = sqlalchemy.Table(
        'result_association',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('results', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('results.id')),
        sqlalchemy.Column('tests', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('tests.id')))