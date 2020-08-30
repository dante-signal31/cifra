"""
Tests for cipher.transposition module.
"""
import pytest

import cifra.cipher.transposition as transposition

ORIGINAL_MESSAGE = "Common sense is not so common."
CIPHERED_MESSAGE_KEY_8 = "Cenoonommstmme oo snnio. s s c"
TEST_KEY = 8


@pytest.mark.quick_test
def test_cipher():
    ciphered_text = transposition.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_8


@pytest.mark.quick_test
def test_decipher():
    deciphered_text = transposition.decipher(CIPHERED_MESSAGE_KEY_8, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE