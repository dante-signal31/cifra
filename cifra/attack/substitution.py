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
import multiprocessing
from typing import Optional, Dict, Set, List, Tuple
from cifra.attack.dictionaries import get_words_from_text, get_word_pattern, Dictionary, get_candidates_frequency_at_language
from cifra.attack.simple_attacks import _get_usable_cpus
from cifra.cipher.common import DEFAULT_CHARSET
from cifra.cipher.substitution import decipher, WrongSubstitutionKey


def hack_substitution(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                      _database_path: Optional[str] = None) -> (str, float):
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
    keys_found: Dict[str, float] = dict()  # Keys are charset keys and values valid probabilities.
    for language in available_languages:
        possible_mappings, _ = _get_possible_mappings(language, ciphered_words, charset, _database_path)
        language_keys = _assess_candidate_keys(ciphered_text, language, possible_mappings, charset, _database_path)
        # It would be extremely odd, but two languages may generate the same key.
        # So we must keep the one with higher probability.
        for key in keys_found:
            if key in language_keys:
                if language_keys[key] < keys_found[key]:
                    language_keys.pop(key)
        # Now, languages_keys should have keys not yet present at keys_found or
        # with smaller probability.
        keys_found.update(language_keys)
    best_key, best_probability = _get_best_key(keys_found)
    return best_key, best_probability


def hack_substitution_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                         _database_path: Optional[str] = None) -> (str, float):
    """ Get substitution ciphered text key.

    Uses a word pattern matching technique to identify used language.

    **You should use this function instead of *hack_substitution*.**

    Whereas *hack_substitution* uses a sequential approach, this function uses
    multiprocessing to improve performance.

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
    keys_found: Dict[str, float] = dict()  # Keys are charset keys and values valid probabilities.
    with multiprocessing.Pool(_get_usable_cpus()) as pool:
        nargs = ((language, ciphered_words, charset, _database_path) for language in available_languages)
        possible_mappings: List[Tuple[List[Mapping], str]] = pool.starmap(_get_possible_mappings, nargs)
        # I could have passed the entire mappings list to _assess_candidates_keys() but
        # in my tests I've discovered to be more perfomant to extract every element from
        # mappings list and passing them as one element lists.
        nargs = ((ciphered_text, language, [mapping], charset, _database_path)
                 for mappings, language in possible_mappings for mapping in mappings)
        language_keys_list: List[Dict[str, float]] = pool.starmap(_assess_candidate_keys, nargs)
        for language_keys in language_keys_list:
            # It would be extremely odd, but two languages may generate the same key.
            # So we must keep the one with higher probability.
            for key in keys_found:
                if key in language_keys:
                    if language_keys[key] < keys_found[key]:
                        language_keys.pop(key)
            # Now, languages_keys should have keys not yet present at keys_found or
            # with smaller probability.
            keys_found.update(language_keys)
    best_key, best_probability = _get_best_key(keys_found)
    return best_key, best_probability


def _get_possible_mappings(language: str, ciphered_words: Set[str],
                           charset: str = DEFAULT_CHARSET,
                           _database_path: Optional[str] = None) -> Tuple[List[Mapping], str]:
    """ Get every possible mapping for given ciphered words in given language.

    :param language: Language to compare with ciphered words.
    :param ciphered_words: Words whose patterns needs to be compared with those from language dictionary.
    :param charset: Charset used for substitution method. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: Tuple with a list of possible mapping found and a string with language name where those
        mappings where found.
    """
    global_mapping = _generate_language_mapping(language, ciphered_words,
                                                          charset, _database_path)
    global_mapping.clean_redundancies()
    possible_mappings = global_mapping.get_possible_mappings()
    return possible_mappings, language


def _assess_candidate_keys(ciphered_text: str, language: str, possible_mappings: List[Mapping],
                           charset: str = DEFAULT_CHARSET,
                           _database_path: Optional[str] = None) -> Dict[str, float]:
    """ Assess every possible mapping and get how many recovered words are identifiable
    in any language dictionary.

    :param ciphered_text: Text to be deciphered.
    :param language: Language to compare with recovered words.
    :param possible_mappings: Possible cipherletter mappings for given text.
    :param charset: Charset used for substitution method. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: A dict whose keys are tested keys and values are a 0 to 1 float with
        comparison sucess for given language. 1 means every deciphered word using
        tested key can be found in given language dictionary.
    """
    keys_found: Dict[str, float] = dict()
    for possible_mapping in possible_mappings:
        (key, probability) = _assess_possible_mapping(possible_mapping, language, ciphered_text, charset, _database_path)
        keys_found[key] = probability
    return keys_found


def _assess_possible_mapping(possible_mapping: Mapping, language: str, ciphered_text: str, charset: str = DEFAULT_CHARSET,
                             _database_path: Optional[str] = None) -> (str, float):
    """ Convert mapping to a substitution key and check if that key deciphers messages in words
    from any know dictionary.

    :param possible_mapping: Mapping reduced to maximum.
    :param language: Language to compare with recovered words.
    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for substitution method. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: A tuple with key generated from given mapping and a 0 to 1 float with
        comparison success for given language. 1 means every deciphered word using
        tested key can be found in given language dictionary.
    """
    key = possible_mapping.generate_key_string()
    return key, _assess_substitution_key(ciphered_text, key, language,
                                               charset, _database_path=_database_path)


def _generate_language_mapping(language: str, ciphered_words: Set[str],
                               charset: str = DEFAULT_CHARSET,
                               _database_path: Optional[str] = None) -> Mapping:
    """ Generate a mapping with all letter candidates in given language for every
    cipherletter.

    :param language: Language to look letter candidates into.
    :param ciphered_words: Every cipherword in message.
    :param charset: Charset used for substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: Mapping loaded with all candidates in given language.
    """
    language_mapping = Mapping(charset)
    with Dictionary.open(language, False, _database_path=_database_path) as dictionary:
        for ciphered_word in ciphered_words:
            word_mapping = _get_word_mapping(charset, ciphered_word, dictionary)
            language_mapping.reduce_mapping(word_mapping)
    return language_mapping


def _get_best_key(keys_found: Dict[str, float]) -> (str, float):
    """ Get key with maximum probability.

    :param keys_found: Dict with cipher keys as dict keys and their corresponding probabilities as float values.
    :return: Tuple with best key and its corresponding probability.
    """
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


def _assess_substitution_key(ciphered_text: str, key: str, language: str, charset: str,
                             _database_path: Optional[str] = None) -> float:
    """ Decipher text with given key and try to find out if returned text can be identified with given
    language.

    If given key does not comply with coherence rules then it is silently discarded
    returning 0.

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
    try:
        recovered_text = decipher(ciphered_text, key, charset)
        words = get_words_from_text(recovered_text)
        frequency = get_candidates_frequency_at_language(words, language, _database_path=_database_path)
    except WrongSubstitutionKey:
        frequency = 0
    return frequency


class Mapping(object):
    """ Class to manage possible candidates to substitute every cipherletter in charset.

    You can use it as a dict whose keys are letters and values are sets with substitution
    letters candidates.
    """

    def __init__(self, charset: str = DEFAULT_CHARSET):
        """ Create empty mapping for cipher letters.

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
        key_list = []
        for clear_char in self._charset:
            char_found = False
            for key, value_set in self._mapping.items():
                if value_set == set():
                    continue
                # Use this method with already reduced mappings because only
                # first element of every set will be taken.
                value = [v for v in value_set][0]
                if value == clear_char:
                    char_found = True
                    key_list.append(key)
                    break
            if not char_found:
                key_list.append(clear_char)
        return "".join(key_list)

    def popitem(self) -> (str, Set[str]):
        """ Remove and return a cipherletter and its candidates from current mapping.

        :return: A tuple with selected cipherletter and its candidates.
        """
        return self._mapping.popitem()

    def get_possible_mappings(self, mapping: Mapping = None) -> List[Mapping]:
        """ Return every possible mapping from an unresolved mapping.

        An unresolved mapping is one that has more than one possibility in any of
        its chars.

        :param mapping: A character mapping.
        :return: A list of mapping candidates.
        """
        if mapping is None:
            mapping = Mapping.new_mapping(self._mapping, self._charset)
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

    def clean_redundancies(self) -> None:
        """ Remove redundancies from mapping.

        If any cipherletter has been reduced to just one candidate, then that
        candidate should not be in any other cipherletter. Leaving it would produce
        an inconsistent deciphering key with repeated characters.
        """
        candidates_to_remove = [[candidate for candidate in candidate_set][0]
                                for candidate_set in self._mapping.values() if len(candidate_set) == 1]
        sets_to_check = [candidate_set for candidate_set in self._mapping.values() if len(candidate_set) > 1]
        for candidate_to_remove in candidates_to_remove:
            for set_to_check in sets_to_check:
                if candidate_to_remove in set_to_check:
                    set_to_check.remove(candidate_to_remove)


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
