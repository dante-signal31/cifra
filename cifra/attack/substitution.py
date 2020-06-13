"""Module to attack substitution cipher texts.

This module uses a word patter matching method to guess probable key used to cipher
a text using substitution algorithm.

You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from __future__ import annotations
import copy
import functools
from typing import Optional, Dict, Set, List
from cifra.attack.dictionaries import get_words_from_text, get_word_pattern, Dictionary, IdentifiedLanguage, identify_language, get_candidates_frequency_at_language
from cifra.cipher.common import DEFAULT_CHARSET
from cifra.cipher.substitution import decipher


def hack_substitution(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> (str, float):
    """ Get substitution ciphered text key.

    Uses a word pattern matching technique to identify used language.

    **You should not use this function. Use *hack_substitution_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for substitution method. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: A tuple with substitution key found and success probability.
    """
    ciphered_words = get_words_from_text(ciphered_text)
    available_languages = Dictionary.get_dictionaries_names(_database_path=_database_path)
    keys_found = dict() # Keys are charset keys and values valid probabilities.
    global_mapping = dict()
    for language in available_languages:
        with Dictionary.open(language, False, _database_path=_database_path) as dictionary:
            global_mapping[language] = Mapping(charset)
            for ciphered_word in ciphered_words:
                word_mapping = _get_word_mapping(charset, ciphered_word, dictionary)
                global_mapping[language].reduce_mapping(word_mapping)
            possible_mappings = global_mapping[language].get_possible_mappings()
            for possible_mapping in possible_mappings:
                key = possible_mapping.generate_key_string()
                keys_found[key] = _assess_substitution_key(ciphered_text, key, language, charset)
    best_probability = 0
    best_key = ""
    for key, value in keys_found.items():
        if value > best_probability:
            best_probability = value
            best_key = key
    return best_key, best_probability

def _get_used_charset(text: str) -> Set[str]:
    """ Get a set with single chars used in text.

    :param text: Text to extract chars from.
    :return: Set with texts chars.
    """
    used_charset = set()
    words = get_words_from_text(text)
    for word in words:
        new_set = set(word)
        used_charset |= new_set
    return used_charset

# def _reduce_global_mapping(global_mapping: Dict[str, Dict[str, Set[str]]], language: str, word_mapping: Dict[str, Set[str]]) -> None:
#     """ Apply given word mapping to reduce global mapping.
#
#     :param global_mapping: Current global mapping for analyzed cipher words so far.
#     :param language: Current language assesed.
#     :param word_mapping: Partial mapping for an individual word.
#     """
#     for key in global_mapping[language].keys():
#         if len(global_mapping[language][key]) > 1 and word_mapping[key]:  # Both set are not empty.
#             global_mapping[language][key] &= word_mapping[key]
#         elif not global_mapping[language][key] and word_mapping[key]:
#             global_mapping[language][key] = word_mapping[key].copy()

# def _init_mapping(charset: str = DEFAULT_CHARSET) -> Dict[str, Set[str]]:
#     """ Create empty mapping for cipher letters
#
#     :param text: Ciphered text to extract letters from.
#     :return: A dict whose keys are letters and values are sets with subtitution
#         letter candidates.
#     """
#     returned_dict = dict()
#     for char in charset:
#         returned_dict[char] = set()
#     return returned_dict


# def _get_possible_mappings(mapping: Dict[str, Set[str]]) -> List[Dict[str, Set[str]]]:
#     """ Return every possible mapping from an unresolved mapping.
#
#     An unresolved mapping is one that has more than one possibility in any of
#     its chars.
#
#     :param mapping: A character mapping.
#     :return: A list of mapping candidates.
#     """
#     try:
#         char, candidates = mapping.popitem()
#     except KeyError:
#         return [dict(), ]
#     else:
#         mapping_to_return = []
#         partial_mappings = _get_possible_mappings(mapping)
#         for candidate in candidates:
#             for partial_mapping in partial_mappings:
#                 current_mapping = {char: {candidate}}
#                 current_mapping.update(partial_mapping)
#                 mapping_to_return.append(current_mapping)
#         return mapping_to_return


def _assess_substitution_key(ciphered_text: str, key: str, language: str, charset: str,
                       _database_path: Optional[str] = None) -> float:
    """ Decipher text with given key and try to find out if returned text can be identified with given
    language.

    :param ciphered_text: Text to be deciphered.
    :param key: Key to decipher *ciphered_text*.
    :param language: Language to compare got text.
    :param charset: Charset used for substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: Float from 0 to 1. The higher the frequency of presence of words in language
        the higher of this probability.
    """
    recovered_text = decipher(ciphered_text, key, charset)
    words = get_words_from_text(recovered_text)
    frequency = get_candidates_frequency_at_language(words, language, _database_path=_database_path)
    return frequency


class Mapping(object):
    """ Class to manage possible candidates to substitute every cipherletter in charset.

    You can use it as a dict whose keys are letters and values are sets with substitution
    letters candidates.
    """

    def __init__(self, charset: str = DEFAULT_CHARSET):
        """ Create empty mapping for cipher letters

        :param charset: Charset used for substitution method. Both ends, ciphering
            and deciphering, should use the same charset or original text won't be properly
            recovered.
        :return: A Mapping class instance.
        """
        self._mapping = dict()
        self._charset = charset
        for char in charset:
            self._mapping[char] = set()

    @classmethod
    def new_mapping(cls, mapping_dict: Dict[str, Set[str]], charset: str = DEFAULT_CHARSET) -> Mapping:
        """ Create a mapping loaded with given mapping dict.

        :param mapping_dict: Content to load.
        :param charset: Charset used for substitution method. Both ends, ciphering
            and deciphering, should use the same charset or original text won't be properly
            recovered.
        :return: A Mapping class instance.
        """
        mapping = cls(charset)
        mapping.load_content(mapping_dict)
        return mapping

    def __delitem__(self, key):
        self._mapping.__delattr__(key)

    def __getitem__(self, key):
        return self._mapping[key]

    def __setitem__(self, key, value):
        self._mapping[key] = value

    def __eq__(self, other):
        return self.get_current_content() == other.get_current_content()

    def load_content(self, mapping_dict: Dict[str, Set[str]]) -> None:
        """ Populates this mapping using a dict.

        Dict's keys are cipherletters and values are sets of mapping char candidates.

        Given mapping should use the same charset as this one. Differing cipherletters
        will be discarded.

        :param mapping_dict: Content to load.
        """
        for key, value_set in mapping_dict.items():
            if key in self._mapping and not value_set == set():
                self._mapping[key] = copy.deepcopy(value_set)

    def get_current_content(self) -> Dict[str, Set[str]]:
        """ Get current mapping content.

        :return: Dict's keys are cipherletters and values are sets of mapping char candidates.
        """
        return self._mapping

    def cipherletters(self):
        """ Get this mapping cipherletters.

        :return: A set-like view object with cipherletters registered in this mapping.
        """
        return self._mapping.keys()

    def generate_key_string(self) -> str:
        """ Generate an string to be used as a substitution key.

        If any cipherletter has no substitutions alternative then the same cipherletter
        is used for substitution. Also, be aware that first candidate for every
        cipherletter will be chosen so use this method when mapping is completely
        reduced.

        :return: Generated key string.
        """
        return "".join(value_set.pop() if value_set != set() else key for key, value_set in self._mapping.items())

    def popitem(self) -> (str, Set[str]):
        return self._mapping.popitem()

    def get_possible_mappings(self, mapping: Mapping = None) -> List[Mapping]:
        """ Return every possible mapping from an unresolved mapping.

        An unresolved mapping is one that has more than one possibility in any of
        its chars.

        :param mapping: A character mapping.
        :return: A list of mapping candidates.
        """
        if mapping is None:
            mapping = Mapping.new_mapping(self._mapping)
        try:
            char, candidates = mapping.popitem()
        except KeyError:
            return [Mapping(charset=self._charset), ]
        else:
            mapping_list = []
            partial_mappings = self.get_possible_mappings(mapping)
            if not candidates == set():
                for candidate in candidates:
                    for partial_mapping in partial_mappings:
                        current_mapping = Mapping.new_mapping({char: {candidate}}, charset=self._charset)
                        current_mapping.load_content(partial_mapping.get_current_content())
                        mapping_list.append(current_mapping)
            else:
                for partial_mapping in partial_mappings:
                    current_mapping = Mapping.new_mapping({char: set()}, charset=self._charset)
                    current_mapping.load_content(partial_mapping.get_current_content())
                    mapping_list.append(current_mapping)
            return mapping_list

    def reduce_mapping(self, word_mapping: Mapping) -> None:
        """ Apply given word mapping to reduce this mapping.

        :param word_mapping: Partial mapping for an individual word.
        """
        for cipherletter in self.cipherletters():
            if len(self[cipherletter]) > 1 and word_mapping[cipherletter]:  # Both set are not empty.
                self[cipherletter] &= word_mapping[cipherletter]
            elif not self[cipherletter] and word_mapping[cipherletter]:
                self[cipherletter] = word_mapping[cipherletter].copy()


def _get_word_mapping(charset: str, ciphered_word: str, dictionary: Dictionary) -> Mapping:
    """ Create a mapping with characters candidates for given ciphered word.

    :param charset: Charset used for substitution method. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param ciphered_word: Ciphered word used to find words with similar patterns.
    :param dictionary: Dictionary to extract from words with the same pattern than ciphered word.
    :return: A Mapping class instance.
    """
    word_mapping = Mapping(charset)
    ciphered_word_pattern = get_word_pattern(ciphered_word)
    word_candidates = dictionary.get_words_with_pattern(ciphered_word_pattern)
    for index, char in enumerate(ciphered_word):
        for word_candidate in word_candidates:
            word_mapping[char].add(word_candidate[index])
    return word_mapping
