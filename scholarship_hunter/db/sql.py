from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect(connection_str):
    return create_engine(connection_str)  # works


def create_tables(engine):
    Base.metadata.create_all(engine)
