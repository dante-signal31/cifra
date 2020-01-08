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


class Dictionary(object):
    """
    Cifra stores word dictionaries as SQL tables in a local database. This class
    is a wrapper to not to deal directly with that database.
    """

    def __init__(self, language: str):
        raise NotImplementedError

    def _open(self) -> None:
        """
        Do not use this method directly. This class is intended to be used as a
        context manager so you'd better use this class open(language: str)
        method.
        """
        raise NotImplementedError

    @staticmethod
    @contextlib.contextmanager
    def open(language: str) -> Dictionary:
        """
        This class is intended to be used as a context manager so you don't have
        to deal with opening and closing this dictionary. So, call this method
        as a context manager, it will return this instance so you can call
        further methods to manage its words.

        :param language: language you want to manage its words.
        :return: An instance of this word dictionary.
        """
        opened_dictionary = Dictionary(language)
        opened_dictionary._open()
        yield opened_dictionary
        opened_dictionary._close()

    def _close(self) -> None:
        """
        Do not use this method directly. This class is intended to be used as a
        context manager so you'd better use this class open(language: str)
        method.
        """
        raise NotImplementedError

    def add_word(self, word: str) -> None:
        """
        Add given word to dictionary.

        If word is already present at dictionary, do nothing.

        :param word: word to add to dictionary.
        """
        raise NotImplementedError

    def remove_word(self, word: str) -> None:
        """
        Remove given word from dictionary.

        If word is not already present at dictionary, do nothing.

        :param word: word to remove from dictionary.
        """
        raise NotImplementedError

    def word_exists(self, word: str) -> bool:
        """
        Check if given word exists at this dictionary.

        :param word: word to check.
        :return: True if word is already present at dictionary, False otherwise.
        """
        raise NotImplementedError

    def _already_created(self) -> bool:
        """
        Check if a table for this instance language already exists at database
        or not.

        :return: True if a table exists for this instance language, otherwise False.
        """
        raise NotImplementedError

    def _create_dictionary(self) -> None:
        """
        Create this instance language table in database.
        """
        raise NotImplementedError
