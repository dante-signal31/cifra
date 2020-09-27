"""Module to attack Transposition cipher texts.

This module uses a brute force method to guess probable key used to cipher
a text using Transposition algorithm.
"""
from typing import Optional

from cifra.attack.dictionaries import IdentifiedLanguage
from cifra.attack.simple_attacks import _assess_key, _integer_key_generator
from cifra.attack.simple_attacks import _brute_force as simple_brute_force
from cifra.attack.simple_attacks import _brute_force_mp as simple_brute_force_mp
from cifra.cipher.transposition import decipher


def brute_force(ciphered_text: str, _database_path: Optional[str] = None) -> int:
    """ Get Transposition ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Transposition key found.
    """
    key_space_length = len(ciphered_text)
    return simple_brute_force(key_generator=_integer_key_generator(key_space_length),
                              assess_function=_assess_transposition_key,
                              # key_space_length=key_space_length,
                              ciphered_text=ciphered_text,
                              _database_path=_database_path)


def brute_force_mp(ciphered_text: str, _database_path: Optional[str] = None) -> int:
    """ Get Transposition ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Transposition key found.
    """
    key_space_length = len(ciphered_text)
    return simple_brute_force_mp(key_generator=_integer_key_generator(key_space_length),
                                 assess_function=_analize_text,
                                 key_space_length=key_space_length,
                                 ciphered_text=ciphered_text,
                                 _database_path=_database_path)


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
    return _assess_key(decipher, ciphered_text=ciphered_text, key=key, _database_path=_database_path)
