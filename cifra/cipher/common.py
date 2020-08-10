""" Common functions to be used across cipher modules. """
from enum import Enum, auto

from cifra.cipher.cryptomath import find_mod_inverse

DEFAULT_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


class Ciphers(Enum):
    CAESAR = auto()
    TRANSPOSITION = auto()
    AFFINE = auto()
    VIGENERE = auto()


def _offset_text(text: str, key: int, advance: bool, cipher_used: Ciphers, charset: str = DEFAULT_CHARSET) -> str:
    """ Generic function to offset text characters frontwards and backwards.

    :param text: Text to offset.
    :param key: Number of positions to offset characters.
    :param advance: If True offset characters frontwards.
    :param cipher_used: Kind of cipher we are using for this message.
    :param charset: Charset to use for substitution.
    :return: Offset text.
    """
    offset_text = ""
    for char in text:
        new_char = char
        if char in charset:
            new_char_position = _get_new_char_position(char, key, advance, cipher_used, charset)
            new_char = charset[new_char_position]
        offset_text = "".join([offset_text, new_char])
    return offset_text


def _get_new_char_position(char: str, key: int, advance: bool, cipher_used: Ciphers, charset=DEFAULT_CHARSET) -> int:
    """ Get position for offset char.

    :param char: Actual character with no offset. It should be normalized to be
     sure it is present at charset.
    :param key: Offset to apply.
    :param advance: If True offset is going to be applied frontwards.
    :param cipher_used: Kind of cipher we are using for this message.
    :param charset: Charset to use for substitution.
    :return: Index in charset for offset char.
    """
    charset_length = len(charset)
    char_position = charset.index(char)
    offset_position = _get_offset_position(char_position, key, advance, cipher_used, charset_length)
    new_char_position = offset_position % charset_length
    return new_char_position


def _get_offset_position(current_position: int, key: int, advance: bool, cipher_used: Ciphers, charset_length: int) -> int:
    """ Get new offset depending on ciphering being used.

    :param current_position: Charset index of current char we are calculating offset to.
    :param key: Key value used for this message.
    :param advance: If True offset is going to be applied frontwards, that is when you cipher.
    :param cipher_used: Kind of cipher we are using for this message.
    :param charset_length: Length of charset to use for substitution.
    :return: New offset position for this char.
    """
    if cipher_used is Ciphers.CAESAR or cipher_used is Ciphers.VIGENERE:
        return current_position + key if advance else current_position - key
    if cipher_used is Ciphers.AFFINE:
        multiplying_key, adding_key = get_affine_key_parts(key, charset_length)
        if advance:
            return (current_position * multiplying_key) + adding_key
        else:
            return (current_position - adding_key) * find_mod_inverse(multiplying_key, charset_length)


def get_affine_key_parts(key: int, charset_length: int) -> (int, int):
    """ Split given key in two parts to be used by Affine cipher.

    :param key: Key used for ciphering and deciphering.
    :param charset_length: Length of charset used for Affine method substitutions. Both end should
      use the same charset or original text won't be properly recovered.
    :return: A tuple whose first component is key used for multiplying while ciphering and second component is used for
      adding.
    """
    multiplying_key = key // charset_length
    adding_key = key % charset_length
    return multiplying_key, adding_key






