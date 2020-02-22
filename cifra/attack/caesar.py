"""Module to attack Caesar cipher texts.

This module uses a brute force method to guess probable key used to cipher
a text using Caesar algorithm.

You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from typing import Optional

from cifra.attack.dictionaries import identify_language
from cifra.cipher.caesar import DEFAULT_CHARSET, decipher


def brute_force_caesar(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> int:
    """ Get Caesar ciphered text key.

    Uses a brute force technique trying the entire key space until finding a text
    that can be identified with any of our languages.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Caesar key found.
    """
    key_space_length = len(charset)
    current_best_key = 0
    current_best_probability = 0
    for i in range(key_space_length):
        deciphered_text = decipher(ciphered_text, i, charset)
        identified_language = identify_language(deciphered_text, _database_path=_database_path)
        if identified_language.winner is None:
            continue
        elif identified_language.winner_probability > current_best_probability:
            current_best_key = i
            current_best_probability = identified_language.winner_probability
    return current_best_key


