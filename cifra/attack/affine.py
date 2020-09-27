"""Module to attack Affine cipher texts.

This module uses a brute force method to guess probable key used to cipher
a text using Affine algorithm.

You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from typing import Optional
from cifra.cipher.affine import decipher, validate_key, WrongAffineKey
from cifra.cipher.common import DEFAULT_CHARSET
from cifra.attack.dictionaries import IdentifiedLanguage
from cifra.attack.simple_attacks import _assess_key, _integer_key_generator
from cifra.attack.simple_attacks import _brute_force as simple_brute_force
from cifra.attack.simple_attacks import _brute_force_mp as simple_brute_force_mp


def brute_force(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> int:
    """ Get Affine ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Affine method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Affine key found.
    """
    key_space_length = len(charset) ** 2
    return simple_brute_force(key_generator=_integer_key_generator(key_space_length),
                              assess_function=_assess_affine_key,
                              # key_space_length=key_space_length,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def brute_force_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                   _database_path: Optional[str] = None) -> int:
    """ Get Affine ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Affine method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Affine key found.
    """
    key_space_length = len(charset) ** 2
    return simple_brute_force_mp(key_generator=_integer_key_generator(key_space_length),
                                 assess_function=_analize_text,
                                 key_space_length=key_space_length,
                                 ciphered_text=ciphered_text,
                                 charset=charset,
                                 _database_path=_database_path)


def _analize_text(nargs):
    ciphered_text, key, charset, _database_path = nargs
    return _assess_affine_key(ciphered_text, key, charset, _database_path)


def _assess_affine_key(ciphered_text: str, key: int, charset: str,
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
    try:
        validate_key(key, len(charset))
    except WrongAffineKey:
        return key, IdentifiedLanguage(None, None, dict())
    else:
        return _assess_key(decipher, ciphered_text=ciphered_text, key=key, charset=charset, _database_path=_database_path)