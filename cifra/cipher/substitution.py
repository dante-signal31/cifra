"""
Library to cipher and decipher texts using substitution method.
"""
from enum import Enum, auto
from functools import wraps

DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyz"


class WrongSubstitutionKeyCauses(Enum):
    wrong_key_length = auto()
    repeated_characters = auto()


class WrongSubstitutionKey(Exception):
    """ Exception to warn used key is not valid to be used with this charset and substitution method. """

    def __init__(self, key: str, charset: str, cause: WrongSubstitutionKeyCauses):
        self.key = key
        self.charset = charset
        self._cause = cause

    def get_cause(self) -> (WrongSubstitutionKeyCauses, str):
        """ Get because keys are wrong and a written explanation. """
        if self._cause == WrongSubstitutionKeyCauses.wrong_key_length:
            return self._cause, "Wrong key used: Length is not the same than key one"
        elif self._cause == WrongSubstitutionKeyCauses.repeated_characters:
            return self._cause, "Wrong key used: Key uses repeated characters"


def check_substitution_key(func):
    """ Decorator to check used key is a valid one for substitution method with this charset.

    :raises substitution.WrongSubstitutionKey: If key is not valid. Call get_cause()
        from exception object to get a tuple with a WrongSubstitutionKeyCauses enum, and
        an explanatory message.
    """
    @wraps(func)
    def wrapped(text: str, key: str, charset: str):
        if len(key) != len(charset):
            raise WrongSubstitutionKey(key, charset, WrongSubstitutionKeyCauses.wrong_key_length)
        elif len(key) != len(set(key)):
            raise WrongSubstitutionKey(key, charset, WrongSubstitutionKeyCauses.repeated_characters)
        return func(text, key, charset)
    return wrapped


@check_substitution_key
def cipher(text: str, key: str, charset: str = DEFAULT_CHARSET) -> str:
    """ Cipher given text using substitution method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    This module uses only lowercase charsets. That means that caps will be kept
    but lowercase and uppercase will follow ths same substitutions.

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
    ciphered_chars = []
    for char in text:
        if char.lower() in charset:
            ciphered_char = key[charset.index(char.lower())] if char.islower() \
                else key[charset.index(char.lower())].upper()
        else:
            ciphered_char = char
        ciphered_chars.append(ciphered_char)
    return "".join(ciphered_chars)
    # return "".join(map(lambda char: key[charset.index(char)] if char in charset else char,
    #                    (char for char in text)))


@check_substitution_key
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
    deciphered_chars = []
    for ciphered_char in ciphered_text:
        if ciphered_char.lower() in key:
            char = charset[key.index(ciphered_char.lower())] if ciphered_char.islower() \
                else charset[key.index(ciphered_char.lower())].upper()
        else:
            char = ciphered_char
        deciphered_chars.append(char)
    return "".join(deciphered_chars)
    # return "".join(map(lambda char: charset[key.index(char)] if char in key else char,
    #                    (char for char in ciphered_text)))



