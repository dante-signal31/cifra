"""
Module to deal with words dictionaries.

A dictionary is a repository of distinct words present in an actual language.
"""
# I need to import annotations from future to allow annotate that
# Dictionary.open() returns a Dictionary. That will be the default
# behaviour at python 4.0, but nowadays, you need to import it from
# __future__.
from __future__ import annotations
import contextlib
from typing import Optional

import database


class Dictionary(object):
    """
    Cifra stores word dictionaries in a local database. This class
    is a wrapper to not to deal directly with that database.
    """

    def __init__(self, language: str, database_path: str = None):
        self.language = language
        self._database = database.Database() if database_path is None else database.Database(database_path)
        self._connection = None
        self._language_mapper = None

    def _open(self) -> None:
        """ Do not use this method directly.

        This class is intended to be used as a context manager so you'd better
        use this class open(language: str) method.
        """
        self._connection = self._database.open_session()

    @staticmethod
    @contextlib.contextmanager
    def open(language: str, create: bool = False, database_path: Optional[str] = None) -> Dictionary:
        """
        This class is intended to be used as a context manager so you don't have
        to deal with opening and closing this dictionary. So, call this method
        as a context manager, it will return this instance so you can call
        further methods to manage its words.

        :param language: Language you want to manage its words.
        :param create: Whether this language should be created in database if not present yet.
           It defaults to False. If it is set to False and language is not already present at
           database then a dictionaries.NotExistingLanguage exception is raised, but if it is
           set to True then language is registered in database as a new language.
        :param database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
        :return: An instance of this word dictionary.
        """
        opened_dictionary = Dictionary(language) if database_path is None else Dictionary(language, database_path)
        opened_dictionary._open()
        if opened_dictionary._already_created():
            opened_dictionary._load_language_mapper()
        else:
            if create:
                opened_dictionary._create_dictionary()
            else:
                raise NotExistingLanguage
        yield opened_dictionary
        opened_dictionary._close()

    def _close(self) -> None:
        """ Do not use this method directly.

        This class is intended to be used as a context manager so you'd better
        use this class open(language: str) method.
        """
        self._connection.commit()
        self._connection.close()

    def _load_language_mapper(self) -> None:
        """ Load this language instance to have it for words adding."""
        self._language_mapper = self._connection.query(database.Language) \
            .filter(database.Language.language == self.language)\
            .first()

    def add_word(self, word: str) -> None:
        """
        Add given word to dictionary.

        If word is already present at dictionary, do nothing.

        :param word: word to add to dictionary.
        """
        database_word = database.Word(word=word, language=self._language_mapper,
                                      language_id=self._language_mapper.id)
        self._language_mapper.words.add(database_word)
        self._connection.commit()

    def remove_word(self, word: str) -> None:
        """ Remove given word from dictionary.

        If word is not already present at dictionary, do nothing.

        :param word: word to remove from dictionary.
        """
        word_to_remove = self._connection.query(database.Word)\
            .filter(database.Word.word == word and database.Word.language_id == self._language_mapper.id)\
            .first()
        self._language_mapper.words.remove(word_to_remove)
        self._connection.commit()

    def word_exists(self, word: str) -> bool:
        """
        Check if given word exists at this dictionary.

        :param word: word to check.
        :return: True if word is already present at dictionary, False otherwise.
        """
        language = self._connection.query(database.Language)\
            .filter(database.Language.language == self.language)\
            .first()
        return any(word == word_entry.word for word_entry in language.words)

    def _already_created(self) -> bool:
        """ Check if a table for this instance language already exists at database
        or not.

        :return: True if a table exists for this instance language, otherwise False.
        """
        language = self._connection.query(database.Language) \
            .filter(database.Language.language == self.language)\
            .first()
        return False if language is None else True

    def _create_dictionary(self) -> None:
        """ Create this instance language table in database. """
        language = database.Language(language=self.language)
        self._language_mapper = language
        self._connection.add(language)
        self._connection.commit()


class NotExistingLanguage(Exception):
    """ Exception to alarm when you try to work with a Language that has
    not been created yet.
    """
    pass