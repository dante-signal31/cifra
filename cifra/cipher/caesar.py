"""
Library to cipher and decipher texts using Caesar method.
"""

DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyz"


def cipher(text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """
    Cipher given text using Caesar method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    :param text: Text to be ciphered.
    :param key: Secret key. In Caesar method it corresponds with how many position
     advance in the charset. Both ends should know this and use the same one.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :return: Ciphered text.
    """
    ciphered_text = _offset_text(text, key, True, charset)
    return ciphered_text


def decipher(ciphered_text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """
    Decipher given text using Caesar method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. In Caesar method, and for deciphering end, it correspond
     with how many position get bat in the charset. Both ends should know this and
     use the same one.
    :param charset: Charset used for Caesar method substitutions. Both end should
    use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    deciphered_text = _offset_text(ciphered_text, key, False, charset)
    return deciphered_text


def _offset_text(text: str, key: int, advance: bool, charset: str = DEFAULT_CHARSET) -> str:
    """
    Generic function to offset text characters frontwards and backwards.

    :param text: Text to offset.
    :param key: Number of positions to offset characters.
    :param advance: If True offset characters frontwards.
    :param charset: Charset to use for substitution.
    :return: Offset text.
    """
    offset_text = ""
    for char in text:
        new_char = char
        normalized_char = char.lower()
        if normalized_char in charset:
            new_char_position = _get_new_char_position(normalized_char, key, advance, charset)
            new_char = charset[new_char_position] \
                if char.islower() \
                else charset[new_char_position].upper()
        offset_text = "".join([offset_text, new_char])
    return offset_text


def _get_new_char_position(char: str, key: int, advance: bool, charset=DEFAULT_CHARSET) -> int:
    """
    Get position for offset char.

    :param char: Actual character with no offset. It should be normalized to be
     sure it is present at charset.
    :param key: Offset to apply.
    :param advance: If True offset is going to be applied frontwards.
    :param charset: Charset to use for substitution.
    :return: Index in charset for offset char.
    """
    charset_length = len(charset)
    char_position = charset.index(char)
    offset_position = char_position + key if advance else char_position - key
    if advance:
        new_char_position = offset_position % charset_length
    else:
        new_char_position = offset_position \
            if offset_position >= 0 \
            else charset_length - (abs(offset_position) % charset_length)
    return new_char_position
