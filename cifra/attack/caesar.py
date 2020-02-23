"""Module to attack Caesar cipher texts.

This module uses a brute force method to guess probable key used to cipher
a text using Caesar algorithm.

You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
import multiprocessing
import os
from typing import Optional, List, Tuple

from cifra.attack.dictionaries import identify_language, IdentifiedLanguage
from cifra.cipher.caesar import DEFAULT_CHARSET, decipher


def brute_force_caesar(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> int:
    """ Get Caesar ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_caesar_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Caesar key found.
    """
    key_space_length = len(charset)
    results = []
    for key in range(key_space_length):
        results.append(_assess_caesar_key(ciphered_text, key, charset, _database_path=_database_path))
    best_key = _get_best_result(results)
    return best_key


def brute_force_caesar_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> int:
    """ Get Caesar ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force_caesar*.**

    Whereas *brute_force_caesar* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Caesar key found.
    """
    key_space_length = len(charset)
    results = []
    with multiprocessing.Pool(_get_usable_cpus()) as pool:
        nargs = ((ciphered_text, key, charset, _database_path) for key in range(key_space_length))
        results = pool.map(_analize_text, nargs)
    best_key = _get_best_result(results)
    return best_key


def _analize_text(nargs):
    ciphered_text, key, charset, _database_path = nargs
    return _assess_caesar_key(ciphered_text, key, charset, _database_path)


def _get_usable_cpus() -> int:
    """Get the number of CPUs the current process can use.

    :return: Number of CPUs the current process can use.
    """
    return len(os.sched_getaffinity(0))


def _assess_caesar_key(ciphered_text: str, key: int, charset: str,
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
    :return: A tuple with used key ans An *IdentifiedLanguage* object with assessment result.
    """
    deciphered_text = decipher(ciphered_text, key, charset)
    identified_language = identify_language(deciphered_text, _database_path=_database_path)
    return key, identified_language


def _get_best_result(identified_languages: List[Tuple[str, IdentifiedLanguage]]) -> int:
    """Assess a list of IdentifiedLanguage objects and select the most likely.

    :param identified_languages: A list of tuples with a Caesar key and its corresponding IdentifiedLanguage object.
    :return: Caesar key whose IdentifiedLanguage object got the highest probability.
    """
    current_best_key = 0
    current_best_probability = 0
    for caesar_key, identified_language in identified_languages:
        if identified_language.winner is None:
            continue
        elif identified_language.winner_probability > current_best_probability:
            current_best_key = caesar_key
            current_best_probability = identified_language.winner_probability
    return current_best_key
