"""
Tests for cipher.vigenere module.
"""
import pytest
import cipher.vigenere as vigenere

ORIGINAL_MESSAGE = "Common sense is not so common."
CIPHERED_MESSAGE = "Rwlloc admst qr moi an bobunm."
TEST_KEY = "pizza"


@pytest.mark.quick_test
def test_cipher():
    ciphered_text = vigenere.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE


@pytest.mark.quick_test
def test_decipher():
    deciphered_text = vigenere.decipher(CIPHERED_MESSAGE, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE