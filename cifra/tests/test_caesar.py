"""
Tests for cipher.caesar module.
"""
import cipher.caesar as caesar

ORIGINAL_MESSAGE = "This is my secret message."
CIPHERED_MESSAGE_KEY_13 = "Guvf vf zl frperg zrffntr."
TEST_KEY = 13


def test_cipher():
    ciphered_text = caesar.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_13


def test_decipher():
    deciphered_text = caesar.decipher(CIPHERED_MESSAGE_KEY_13, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE


