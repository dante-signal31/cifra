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
from cifra.cipher.common import DEFAULT_CHARSET


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
    raise NotImplementedError


def brute_force_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                   _database_path: Optional[str] = None) -> int:
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
    raise NotImplementedError