"""
Cifra database definition.
"""
import contextlib
import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker, Session

if os.getenv("CIFRA_DEBUG", 0) == "1":
    # TODO: Check Travia CI sets it corresponding CIFRA_DEBUG env var to 1.
    DATABASE_PATH = "cifra_database.sqlite"
else:
    DATABASE_PATH = "~/.cifra/cifra_database.sqlite"


Base = declarative_base()


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False, unique=True)
    words = relationship("Word",
                         back_populates="language",
                         cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'Language: {self.language}'


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language",
                            back_populates="words")

    def __repr__(self):
        return f'Word: {self.word} from language {self.language}'


def create_database(database_path: str = DATABASE_PATH) -> sqlalchemy.engine.Engine:
    """ Create and populate database with its default tables.

    :param database_path: Absolute pathname for database file.
    :return: An SQLAlchemy Engine instance for this database.
    """
    connection_string = f"sqlite:///{database_path}"
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine


# @contextlib.contextmanager
# def open_database_session(engine: Engine) -> sqlalchemy.orm.Session:
#     """Context manager to open a session against database.
#
#     This context manager yields created session.
#
#     On scope exit session is closed.
#
#     :param engine: SQLAlchemy Engine instance got from create_database().
#     :return: This context manager returns a SQLAlchemy Session instance to operate with database.
#     """
#     session_factory = sessionmaker(bind=engine)
#     session = session_factory()
#     yield session
#     session.close()


class Database(object):

    def __init__(self, database_path: str = DATABASE_PATH):
        self._engine = create_database(database_path)

    def open_session(self):
        session_factory = sessionmaker(bind=self._engine)
        session = session_factory()
        return session