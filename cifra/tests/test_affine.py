"""
Tests for cipher.affine module.
"""
import string
import cipher.affine as affine
from test_common._random.strings import random_string

ORIGINAL_MESSAGE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHERED_MESSAGE_KEY_79 = "BEHKNQTWZCFILORUXADGJMPSVY"
TEST_KEY = 79


def test_cipher():
    ciphered_text = affine.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_79


def test_decipher():
    deciphered_text = affine.decipher(CIPHERED_MESSAGE_KEY_79, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE


def test_get_random_key():
    charset = ''.join([string.ascii_letters, string.digits])
    test_string = random_string(10)
    key = affine.get_random_key(charset)
    assert affine._validate_key(key, len(charset))
    ciphered_test_string = affine.cipher(test_string, key, charset=charset)
    recovered_string = affine.decipher(ciphered_test_string, key, charset=charset)
    assert recovered_string == test_string