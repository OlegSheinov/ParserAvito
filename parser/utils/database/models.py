from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

metadata = MetaData()

main_categories = Table(
    "main_categories", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('category_id', Integer, unique=True),
    Column('category_absolute_id', Integer),
    Column('name', String(128)),
    Column('param_201', Integer, nullable=True),
    Column('parent_id', Integer)
)


parameters = Table(
    "params", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('param_id', String(64)),
    Column('param_title', String(128)),
)

values = Table(
    'values', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('value_id', Integer, unique=True),
    Column('value_title', String(128)),
    Column('value_parent', ForeignKey('params.id'))
)

values_params = relationship('params', backref='values')

