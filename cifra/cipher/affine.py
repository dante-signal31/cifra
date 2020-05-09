"""
Library to cipher and decipher texts using Affine method.
"""
import random
# import sys
from enum import Enum, auto
from cifra.cipher.common import DEFAULT_CHARSET, Ciphers, _offset_text
from cifra.cipher.cryptomath import gcd


class WrongAffineKeyCauses(Enum):
    multiplying_key_below_zero = auto()
    multiplying_key_zero = auto()
    adding_key_below_zero = auto ()
    adding_key_too_long = auto()
    keys_not_relatively_prime = auto()


class WrongAffineKey(Exception):

    def __init__(self, key: int, multiplying_key: int, adding_key: int, cause: WrongAffineKeyCauses):
        self.key = key
        self.multiplying_key = multiplying_key
        self.adding_key = adding_key
        self._cause = cause

    def get_cause(self)-> (WrongAffineKeyCauses, str):
        """Get because keys are wrong and a written explanation"""
        if self._cause == WrongAffineKeyCauses.multiplying_key_below_zero:
            return self._cause, "Wrong key used: Multiplying key must be greater than 0."
        if self._cause == WrongAffineKeyCauses.multiplying_key_zero:
            return self._cause, "Wrong key used: Multiplying key must not be 0."
        elif self._cause == WrongAffineKeyCauses.adding_key_below_zero:
            return self._cause, "Wrong key used: Adding key must be greater than 0."
        elif self._cause == WrongAffineKeyCauses.adding_key_too_long:
            return self._cause, "Wrong key used: Adding key must be smaller than charset length."
        elif self._cause == WrongAffineKeyCauses.keys_not_relatively_prime:
            return self._cause, "Wrong key used: Keys are not relatively prime."


def cipher(text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """ Cipher given text using Affine method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    Not every key is good to cipher using Affine with a given charset. It must
    meet a set of rules. So we must check given key meets them.

    If given key does not meet any of the rules them a WrongKey exception is raised.

    :param text: Text to be ciphered.
    :param key: Secret key. Both ends should know this and use the same one.
    :param charset: Charset used for Affine method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :return: Ciphered text.
    """
    validate_key(key, len(charset))
    ciphered_text = _offset_text(text, key, True, Ciphers.AFFINE, charset)
    return ciphered_text


def decipher(ciphered_text: str, key: int, charset: str = DEFAULT_CHARSET) -> str:
    """ Decipher given text using Affine method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. Both ends should know this and use the same one.
    :param charset: Charset used for Affine method substitutions. Both end should
      use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    validate_key(key, len(charset))
    deciphered_text = _offset_text(ciphered_text, key, False, Ciphers.AFFINE, charset)
    return deciphered_text


def get_random_key(charset: str = DEFAULT_CHARSET) -> int:
    """Get a valid random Affine key for given charset.

    Get manually a valid Affine key can be hardsome because all rules it must meet.
    This function automates that task, so you can use it and run.

    :param charset: Charset you are going to use to cipher.
    :returns: An random Affine key valid for given charset.
    """
    charset_length = len(charset)
    while True:
        key_a = random.randint(2, charset_length)
        key_b = random.randint(2, charset_length)
        if gcd(key_a, charset_length) == 1:
            return key_a * charset_length + key_b


def get_key_parts(key: int, charset_length: int) -> (int, int):
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


def validate_key(key: int, charset_length: int) -> bool:
    """ Check if given key is good for Affine cipher using this charset.

    Not every key is good to cipher using Affine with a given charset. It must
    meet a set of rules. So we must check given key meets them.

    If given key does not meet any of the rules them a WrongKey exception is raised.

    :param key: Secret key. Both ends should know this and use the same one.
    :param charset_length: Charset used for Affine method substitutions. Both end should
      use the same charset or original text won't be properly recovered.
    :return: True if validation was right. You won't receive a False, an exception will be raised before.
    """
    multiplying_key = key // charset_length
    adding_key = key % charset_length
    if multiplying_key < 0:
        raise WrongAffineKey(key, multiplying_key, adding_key, WrongAffineKeyCauses.multiplying_key_below_zero)
    elif multiplying_key == 0:
        raise WrongAffineKey(key, multiplying_key, adding_key, WrongAffineKeyCauses.multiplying_key_zero)
    elif adding_key < 0:
        raise WrongAffineKey(key, multiplying_key, adding_key, WrongAffineKeyCauses.adding_key_below_zero)
    elif adding_key > charset_length - 1:
        raise WrongAffineKey(key, multiplying_key, adding_key, WrongAffineKeyCauses.adding_key_too_long)
    elif gcd(multiplying_key, charset_length) != 1:
        raise WrongAffineKey(key, multiplying_key, adding_key, WrongAffineKeyCauses.keys_not_relatively_prime)
    return True

