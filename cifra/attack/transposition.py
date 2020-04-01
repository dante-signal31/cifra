"""Module to attack Transposition cipher texts.

This module uses a brute force method to guess probable key used to cipher
a text using Caesar algorithm.
"""
import multiprocessing
from typing import Optional

from cifra.attack.caesar import _get_usable_cpus
from cifra.attack.dictionaries import identify_language, IdentifiedLanguage, get_best_result
from cifra.cipher.transposition import decipher


def brute_force(ciphered_text: str, _database_path: Optional[str] = None) -> int:
    """ Get Transposition ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_transposition_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Transposition key found.
    """
    key_space_length = len(ciphered_text)
    results = []
    for key in range(1, key_space_length):
        results.append(_assess_transposition_key(ciphered_text, key, _database_path=_database_path))
    best_key = get_best_result(results)
    return best_key


def brute_force_mp(ciphered_text: str, _database_path: Optional[str] = None) -> int:
    """ Get Transposition ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force_transposition*.**

    Whereas *brute_force_caesar* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Trasnposition key found.
    """
    key_space_length = len(ciphered_text)
    results = []
    with multiprocessing.Pool(_get_usable_cpus()) as pool:
        nargs = ((ciphered_text, key, _database_path) for key in range(1, key_space_length))
        results = pool.map(_analize_text, nargs)
    best_key = get_best_result(results)
    return best_key


def _analize_text(nargs):
    ciphered_text, key, _database_path = nargs
    return _assess_transposition_key(ciphered_text, key, _database_path)


def _assess_transposition_key(ciphered_text: str, key: int,
                       _database_path: Optional[str] = None) -> (int, IdentifiedLanguage):
    """Decipher text with given key and try to find out if returned text can be identified with any
    language in our dictionaries.

    :param ciphered_text: Text to be deciphered.
    :param key: Key to decipher *ciphered_text*.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: A tuple with used key ans An *IdentifiedLanguage* object with assessment result.
    """
    deciphered_text = decipher(ciphered_text, key)
    identified_language = identify_language(deciphered_text, _database_path=_database_path)
    return key, identified_language
