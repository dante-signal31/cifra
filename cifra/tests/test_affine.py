"""
Tests for cipher.affine module.
"""
import cipher.affine as affine

ORIGINAL_MESSAGE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHERED_MESSAGE_KEY_79 = "BEHKNQTWZCFILORUXADGJMPSVY"
TEST_KEY = 79


def test_cipher():
    ciphered_text = affine.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_79


def test_decipher():
    deciphered_text = affine.decipher(CIPHERED_MESSAGE_KEY_79, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE