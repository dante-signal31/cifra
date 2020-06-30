"""
Module to deal with words dictionaries.

A dictionary is a repository of distinct words present in an actual language.
"""
# I need to import annotations from future to allow annotate that
# Dictionary.open() returns a Dictionary. That will be the default
# behaviour at python 4.0, but nowadays, you need to import it from
# __future__.
from __future__ import annotations
import collections
import contextlib
import dataclasses
import re
from typing import Optional, Set, List, Dict, Tuple

import database


class Dictionary(object):
    """
    Cifra stores word dictionaries in a local database. This class
    is a wrapper to not to deal directly with that database.
    """

    @staticmethod
    def remove_dictionary(language: str, _database_path: Optional[str] = None) -> None:
        """Remove given language from database.

        Be aware that all its words will be removed too.

        :param language: Language to remove from database.
        :param _database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
        """
        dictionary_to_remove = Dictionary(language) if _database_path is None else Dictionary(language, _database_path)
        dictionary_to_remove._open()
        dictionary_to_remove._load_language_mapper()
        dictionary_to_remove._connection.delete(dictionary_to_remove._language_mapper)
        dictionary_to_remove._close()

    @staticmethod
    def get_dictionaries_names(_database_path: Optional[str] = None) -> List[str]:
        """Get languages dictionaries present at database.

        :param _database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
        :return: A list with names of dictionaries present at database.
        """
        _database = database.Database() if _database_path is None else database.Database(_database_path)
        connection = _database.open_session()
        languages = connection.query(database.Language.language).all()
        connection.close()
        return [language_entry[0] for language_entry in languages]

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
    def open(language: str, create: bool = False, _database_path: Optional[str] = None) -> Dictionary:
        """ Context manager to create Dictionaries.

        This class is intended to be used as a context manager so you don't have
        to deal with opening and closing this dictionary. So, call this method
        as a context manager, it will return this instance so you can call
        further methods to manage its words.

        :param language: Language you want to manage its words.
        :param create: Whether this language should be created in database if not present yet.
           It defaults to False. If it is set to False and language is not already present at
           database then a dictionaries.NotExistingLanguage exception is raised, but if it is
           set to True then language is registered in database as a new language.
        :param _database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
        :return: An instance of this word dictionary.
        :raises dictionaries.NotExistingLanguage: if create parameter is false and a not existing language is requested
           to be opened.
        """
        opened_dictionary = Dictionary(language) if _database_path is None else Dictionary(language, _database_path)
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
        """ Add given word to dictionary.

        If word is already present at dictionary, do nothing.

        :param word: word to add to dictionary.
        """
        database_word = database.Word(word=word, language=self._language_mapper,
                                      word_pattern=get_word_pattern(word),
                                      language_id=self._language_mapper.id)
        self._language_mapper.words.add(database_word)
        self._connection.commit()

    def add_multiple_words(self, words: Set[str]) -> None:
        """ Add given words to dictionary.

        :param words: List of words to add to dictionary.
        """
        self._language_mapper.words.update((database.Word(word=word,
                                                          language=self._language_mapper,
                                                          word_pattern=get_word_pattern(word),
                                                          language_id=self._language_mapper.id)
                                            for word in words))
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

    def word_exists(self, word: str, _testing: bool = False) -> bool:
        """ Check if given word exists at this dictionary.

        :param word: word to check.
        :param _testing: Don't mess this parameter. You usually won't use it. It is only
           useful for tests.
        :return: True if word is already present at dictionary, False otherwise.
        """
        if not _testing:
            # Normal execution flow will get here.
            # language = self._connection.query(database.Language)\
            #     .filter(database.Language.language == self.language)\
            #     .first()
            # return any(word == word_entry.word for word_entry in language.words)
            return any(word == word_entry.word for word_entry in self._language_mapper.words)
        else:
            # Execution won't get here unless we are running some test.
            # Tests are crafted to not to have same words in multiple languages so I
            # can make a query without taking in count language.
            # TODO: Check if this branch is still needed.
            words = self._connection.query(database.Word)\
                .filter(database.Word.word == word)\
                .first()
            return words is not None

    def get_words_presence(self, words: Set[str]) -> float:
        """ Get how many words of given set are really present in this dictionary.

        :param words: Set of words.
        :return: A float between 0 and 1 being 1 as every word in set is present at dictionary.
        """
        total_words = len(words)
        current_hits = sum(1 if self.word_exists(word) else 0 for word in words)
        presence = current_hits / total_words
        return presence

    def get_words_with_pattern(self, pattern: str) -> List[str]:
        """ Get a list of every word with given pattern.

        :param pattern: Word patter to search for.
        :return: List of words at dictionary with given pattern.
        """
        words = list(
            map(lambda entry: entry.word,
                filter(lambda entry: entry.word_pattern == pattern, self._language_mapper.words)))
        return words

    def populate(self, file_pathname: str) -> None:
        """ Read a file's words and stores them at this language database.

        :param file_pathname: Absolute path to file with text to analyze.
        """
        words = get_words_from_text_file(file_pathname)
        self.add_multiple_words(words)

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


def get_words_from_text_file(file_pathname: str) -> Set[str]:
    """ Extract words from given file.

    :param file_pathname: Absolute filename to file to be read.
    :return: A set of words normalized to lowercase and without any punctuation mark.
    """
    words = set()
    with open(file_pathname) as text_file:
        for line in text_file.readlines():
            words = words | get_words_from_text(line)
    return words


def get_words_from_text(text: str) -> Set[str]:
    """ Extract words from given text.

    Extracted words are normalized to lowercase and any punctuation mark
    adjacent to words are removed.

    :param text: Text to extract words from.
    :return: A set of words normalized to lowercase and without any punctuation mark.
    """
    lowercase_text = text.lower()
    # Line breaks are troublesome for further assessment so we remove it.
    lowercase_text = lowercase_text.replace("\n", " ")
    lowercase_text = lowercase_text.replace("\r", " ")
    words = set(re.findall(re.compile(r'[^\W\d_]+', re.UNICODE), lowercase_text))
    return words


def get_word_pattern(word: str) -> str:
    """ Get word pattern.

    This pattern is useful to break substitution cipher.

    :param word: Word to get pattern for.
    :return: Word pattern.
    """
    char_order = collections.OrderedDict()
    for char in word:
        char_order.setdefault(char, None)
    chars_indexed = list(char_order.keys())
    pattern = list(map(lambda char: chars_indexed.index(char), (char for char in word)))
    return ".".join(map(str, pattern))


@dataclasses.dataclass
class IdentifiedLanguage:
    """ Language selected as more likely to be the one the message is written into.

    * winner: Name of language more likely. If None the no proper language was found.
    * winner_probability: Probability this language is actually the right one. If None the no proper language was found.
    * candidates: Dict with all languages probabilities. Probabilities are floats from 0 to 1.
    """
    winner: Optional[str]
    winner_probability: Optional[float]
    candidates: Dict[str, float]


def identify_language(text: str, _database_path: Optional[str] = None) -> IdentifiedLanguage:
    """ Identify language used to write text.

    It check each word present at text to find out if is present in any language.
    The language that has more words is select as winner.

    :param text: Text to analyze.
    :param _database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
    :return: Language selected as more likely to be the one used to write text.
    """
    words = get_words_from_text(text)
    candidates = _get_candidates_frequency(words,  _database_path)
    winner = _get_winner(candidates)
    return IdentifiedLanguage(winner, candidates[winner], candidates) if winner is not None \
        else IdentifiedLanguage(None, None, candidates)


def _get_candidates_frequency(words: Set[str], _database_path: Optional[str] = None) -> Dict[str, float]:
    """ Get frequency of presence of words in each language.

    :param words: Text words.
    :param _database_path: Absolute pathname to database file. Usually you don't
           set this parameter, but it is useful for tests.
    :return: Dict with all languages probabilities. Probabilities are floats
           from 0 to 1. The higher the frequency of presence of words in language
           the higher of this probability.
    """
    candidates = {}
    for language in Dictionary.get_dictionaries_names(_database_path):
        # with Dictionary.open(language, _database_path=_database_path) as dictionary:
        #     candidates[language] = dictionary.get_words_presence(words)
        candidates[language] = get_candidates_frequency_at_language(words, language, _database_path=_database_path)
    return candidates


def get_candidates_frequency_at_language(words: Set[str], language: str, _database_path: Optional[str] = None) -> float:
    """ Get frequency of presence of words in given language.

    :param words: Text words.
    :param language: Language you want to look into.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: Float from 0 to 1. The higher the frequency of presence of words in language
        the higher of this probability.
    """
    frequency = 0
    with Dictionary.open(language, _database_path=_database_path) as dictionary:
        frecuency = dictionary.get_words_presence(words)
    return frecuency

def _get_winner(candidates: Dict[str, float]) -> str:
    """ Return candidate with highest frequency.

    :param candidates: Dict with all languages probabilities. Probabilities are floats
           from 0 to 1. The higher the frequency of presence of words in language
           the higher of this probability
    :return: The name of language with highest probability.
    """
    current_winner = None
    current_highest_frequency = 0
    for candidate_name, frequency in candidates.items():
        if frequency > current_highest_frequency:
            current_winner = candidate_name
            current_highest_frequency = frequency
    return current_winner


def get_best_result(identified_languages: List[Tuple[int, IdentifiedLanguage]]) -> int:
    """Assess a list of IdentifiedLanguage objects and select the most likely.

    :param identified_languages: A list of tuples with a Caesar key and its corresponding IdentifiedLanguage object.
    :return: Key whose IdentifiedLanguage object got the highest probability.
    """
    current_best_key = 0
    current_best_probability = 0
    for current_key, identified_language in identified_languages:
        if identified_language.winner is None:
            continue
        elif identified_language.winner_probability > current_best_probability:
            current_best_key = current_key
            current_best_probability = identified_language.winner_probability
    return current_best_key


class NotExistingLanguage(Exception):
    """ Exception to alarm when you try to work with a Language that has
    not been created yet.
    """
    pass
