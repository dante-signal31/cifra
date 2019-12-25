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
    # charset_length = len(charset)
    # ciphered_text = ""
    # for char in text:
    #     new_char = char
    #     normalized_char = char.lower()
    #     if normalized_char in charset:
    #         char_position = charset.index(normalized_char)
    #         new_char_position = (char_position + key) % charset_length
    #         new_char = charset[new_char_position] \
    #             if char.islower() \
    #             else charset[new_char_position].upper()
    #     ciphered_text = "".join([ciphered_text, new_char])
    # return ciphered_text
    ciphered_text = _offset_text(text, key, True)
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
    # charset_length = len(charset)
    # deciphered_text = ""
    # for char in ciphered_tex:
    #     new_char = char
    #     normalized_char = char.lower()
    #     if normalized_char in charset:
    #         char_position = charset.index(normalized_char)
    #         offset_position = char_position - key
    #         new_char_position = offset_position \
    #             if offset_position >= 0 \
    #             else charset_length - (abs(offset_position) % charset_length)
    #         new_char = charset[new_char_position] \
    #             if char.islower() \
    #             else charset[new_char_position].upper()
    #     deciphered_text = "".join([deciphered_text, new_char])
    # return deciphered_text
    deciphered_text = _offset_text(ciphered_text, key, False)
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
    charset_length = len(charset)
    offset_text = ""
    for char in text:
        new_char = char
        normalized_char = char.lower()
        if normalized_char in charset:
            char_position = charset.index(normalized_char)
            if advance:
                new_char_position = (char_position + key) % charset_length
            else:
                offset_position = char_position - key
                new_char_position = offset_position \
                    if offset_position >= 0 \
                    else charset_length - (abs(offset_position) % charset_length)
            new_char = charset[new_char_position] \
                if char.islower() \
                else charset[new_char_position].upper()
        offset_text = "".join([offset_text, new_char])
    return offset_text
