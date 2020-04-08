"""
Tests for cipher.affine module.
"""
import string
import cipher.affine as affine
from test_common._random.strings import random_string

ORIGINAL_MESSAGE = """A computer would deserve to be called intelligent
if it could deceive a human into believing that it was human."
-Alan Turing"""
CIPHERED_MESSAGE_KEY_2894 = "5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!AuaRLLADQALQG93!xQxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1iQX3o1RNNNN5!1RQP36ARu"
TEST_KEY = 2894


def test_cipher():
    ciphered_text = affine.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_2894


def test_decipher():
    deciphered_text = affine.decipher(CIPHERED_MESSAGE_KEY_2894, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE


def test_get_random_key():
    charset = ''.join([string.ascii_letters, string.digits])
    test_string = random_string(10)
    key = affine.get_random_key(charset)
    assert affine._validate_key(key, len(charset))
    ciphered_test_string = affine.cipher(test_string, key, charset=charset)
    recovered_string = affine.decipher(ciphered_test_string, key, charset=charset)
    assert recovered_string == test_string