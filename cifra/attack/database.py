"""
Cifra database definition.
"""
from __future__ import annotations
import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

if os.getenv("CIFRA_DEBUG", 0) == "1":
    # TODO: Check Travia CI sets it corresponding CIFRA_DEBUG env var to 1.
    DATABASE_FILENAME = "cifra_database.sqlite"
else:
    DATABASE_FILENAME = "~/.cifra/cifra_database.sqlite"


Base = declarative_base()


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False, unique=True)
    words = relationship("Word",
                         back_populates="language",
                         cascade="all, delete, delete-orphan",
                         collection_class=set)

    def __repr__(self):
        return f'Language: {self.language}'


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    word_pattern = Column(String, nullable=False)
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language",
                            back_populates="words")

    def __repr__(self):
        return f'Word: {self.word} from {self.language}'

    # How to implement hash?:
    # https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
    def __key(self):
        return self.word, self.language_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: Word):
        if isinstance(other, Word):
            return self.__key() == other.__key()
        return NotImplemented

def create_database(database_path: str = DATABASE_FILENAME) -> sqlalchemy.engine.Engine:
    """ Create and populate database with its default tables.

    :param database_path: Absolute path for database file.
    :return: An SQLAlchemy Engine instance for this database.
    """
    database_pathname = os.path.join(database_path, DATABASE_FILENAME)
    connection_string = f"sqlite:///{database_pathname}"
    engine = create_engine(connection_string, echo=False)
    Base.metadata.create_all(engine)
    return engine


class Database(object):

    def __init__(self, database_path: str = DATABASE_FILENAME):
        self._engine = create_database(database_path)

    def open_session(self):
        session_factory = sessionmaker(bind=self._engine)
        session = session_factory()
        return session
