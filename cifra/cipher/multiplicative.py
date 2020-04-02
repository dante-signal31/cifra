"""
Library to cipher and decipher texts using Multiplicative method.
"""
from cifra.cipher.common import DEFAULT_CHARSET, Ciphers, _offset_text


def cipher(text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """
    Cipher given text using Multiplicative method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    :param text: Text to be ciphered.
    :param key: Secret key. In Multiplicative method it corresponds with how many position
     advance in the charset, taking in count you multiply char index by key. Both ends
     should know this and use the same one.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :return: Ciphered text.
    """
    ciphered_text = _offset_text(text, key, True, Ciphers.MULTIPLICATIVE, charset)
    return ciphered_text


def decipher(ciphered_text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """
    Decipher given text using Multiplicative method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. In Multiplicative method it corresponds with how many position
     advance in the charset, taking in count you multiply char index by key. Both ends
     should know this and use the same one.
    :param charset: Charset used for Caesar method substitutions. Both end should
    use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    deciphered_text = _offset_text(ciphered_text, key, False, Ciphers.MULTIPLICATIVE, charset)
    return deciphered_text

