"""
Library to cipher and decipher texts using substitution method.
"""
from common import DEFAULT_CHARSET


def cipher(text: str, key: str, charset: str = DEFAULT_CHARSET) -> str:
    """ Cipher given text using substitution method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    :param text: Text to be ciphered.
    :param key: Secret key. In substitution method it corresponds with how to
     substitute each character in the charset. Both ends should know this and
     use the same one. Besides key should have the same length than charset and
     no repeated characters.
    :param charset: Charset used for substitution method. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :return: Ciphered text.
    """
    raise NotImplementedError


def decipher(ciphered_text: str, key: str, charset: str = DEFAULT_CHARSET) -> str:
    """ Decipher given text using substitution method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. In substitution method it corresponds with how to
     substitute each character in the charset. Both ends should know this and
     use the same one. Besides key should have the same length than charset and
     no repeated characters.
    :param charset: Charset used for substitution method. Both end should
    use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    raise NotImplementedError
