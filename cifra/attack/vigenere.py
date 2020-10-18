"""Module to attack Vigenere cipher texts.
This module uses two approaches: a dictionary brute force method to guess probable word key used to cipher
a text using Vigenere algorithm and a frequency analysis attack.
You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from itertools import chain, permutations
from typing import Optional, Iterator
from cifra.attack.simple_attacks import _assess_key
from cifra.attack.simple_attacks import _brute_force as simple_brute_force
from cifra.attack.simple_attacks import _brute_force_mp as simple_brute_force_mp
from cifra.attack.simple_attacks import _dictionary_word_key_generator as dictionary_word_key_generator
from cifra.attack.dictionaries import IdentifiedLanguage, Dictionary
from cifra.cipher.vigenere import DEFAULT_CHARSET, decipher
from cifra.attack.frequency import get_substrings, find_most_likely_subkeys
from cifra.tests.test_simple_attacks import mocked_dictionary_word_key_generator


def brute_force(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                _database_path: Optional[str] = None,
                _testing=False) -> str:
    """ Get Vigenere ciphered text key.
    Uses a brute force technique trying the entire dictionary space until finding a text
    that can be identified with any of our languages.
    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.
    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = dictionary_word_key_generator(_database_path) if not _testing else mocked_dictionary_word_key_generator()
    return simple_brute_force(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              # key_space_length=key_space_length,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def brute_force_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                   _database_path: Optional[str] = None,
                   _testing=False) -> str:
    """ Get Vigenere ciphered text key.

    Uses a brute force technique trying the entire dictionary space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = dictionary_word_key_generator(_database_path) if not _testing else mocked_dictionary_word_key_generator()
    return simple_brute_force_mp(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def _analize_text(nargs):
    ciphered_text, key, charset, _database_path = nargs
    return _assess_vigenere_key(ciphered_text, key, charset, _database_path)


def _assess_vigenere_key(ciphered_text: str, key: int, charset: str,
                       _database_path: Optional[str] = None) -> (int, IdentifiedLanguage):
    """Decipher text with given key and try to find out if returned text can be identified with any
    language in our dictionaries.

    :param ciphered_text: Text to be deciphered.
    :param key: Key to decipher *ciphered_text*.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: A tuple with used key and an *IdentifiedLanguage* object with assessment result.
    """
    return _assess_key(decipher, ciphered_text=ciphered_text, key=key, charset=charset, _database_path=_database_path)


def statistical_brute_force(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                maximum_key_length: int = 5,
                _database_path: Optional[str] = None,
                # _testing=False
                            ) -> str:
    """ Get Vigenere ciphered text key.

    Uses a statistical brute force technique (Kasiski analysis) trying the most
    likely keys until finding a text that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This

    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = frequency_key_generator(ciphered_text,
                                                     maximum_key_length,
                                                     _database_path)
    return simple_brute_force(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              # key_space_length=key_space_length,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def frequency_key_generator(ciphered_text: str,
                            maximum_key_length: int = 5,
                            _database_path: Optional[str] = None) -> Iterator[str]:
    """ Assess statistically given ciphertext to return most likely keys.

    :param ciphered_text: Text to be deciphered.
    :param maximum_key_length: Give keys up to given maximum key length.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: An iterator through most likely keys below given length.
    """
    # TODO: Pending unit test for this function.
    for language in Dictionary.get_available_languages(_database_path):
        with Dictionary.open(language, False, _database_path) as language_dictionary:
            for key_length in range(1, maximum_key_length):
                substrings = get_substrings(ciphered_text, key_length)
                # TODO: Remove list()s and leave generators.
                likely_keys = list(chain(*(find_most_likely_subkeys(substring,
                                                                    language_dictionary.letter_histogram,
                                                                    amount=4)
                                    for substring in substrings)))
                passwords_to_try = list(permutations(likely_keys, key_length))
                for password_chars in passwords_to_try:
                    password = "".join(password_chars)
                    yield password
    # raise NotImplementedError