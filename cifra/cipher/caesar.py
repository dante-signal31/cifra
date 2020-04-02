"""
Library to cipher and decipher texts using Caesar method.
"""
from common import _offset_text, Ciphers, DEFAULT_CHARSET


def cipher(text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """ Cipher given text using Caesar method.

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
    ciphered_text = _offset_text(text, key, True, Ciphers.CAESAR, charset)
    return ciphered_text


def decipher(ciphered_text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """ Decipher given text using Caesar method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. In Caesar method, and for deciphering end, it correspond
     with how many position get bat in the charset. Both ends should know this and
     use the same one.
    :param charset: Charset used for Caesar method substitutions. Both end should
    use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    deciphered_text = _offset_text(ciphered_text, key, False, Ciphers.CAESAR, charset)
    return deciphered_text
