""" Common functions to be used across cipher modules. """
from enum import Enum, auto

DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyz"


class Ciphers(Enum):
    CAESAR = auto()
    TRANSPOSITION = auto()
    MULTIPLICATIVE = auto()


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
        normalized_char = char.lower()
        if normalized_char in charset:
            new_char_position = _get_new_char_position(normalized_char, key, advance, cipher_used, charset)
            new_char = charset[new_char_position] \
                if char.islower() \
                else charset[new_char_position].upper()
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
    # offset_position = char_position + key if advance else char_position - key
    offset_position = _get_offset_position(char_position, key, advance, cipher_used)
    if advance:
        new_char_position = offset_position % charset_length
    else:
        new_char_position = offset_position \
            if offset_position >= 0 \
            else charset_length - (abs(offset_position) % charset_length)
    return new_char_position


def _get_offset_position(current_position: int, key: int, advance: bool, cipher_used: Ciphers) -> int:
    """ Get new offset depending on ciphering being used.

    :param current_position: Charset index of current char we are calculating offset to.
    :param key: Key value used for this message.
    :param advance: If True offset is going to be applied frontwards.
    :param cipher_used: Kind of cipher we are using for this message.
    :return: New offset position for this char.
    """
    if cipher_used is Ciphers.CAESAR:
        return current_position + key if advance else current_position - key
    if cipher_used is Ciphers.MULTIPLICATIVE:
        return current_position * key if advance else current_position / key