"""
Tests for cipher.caesar module.
"""
import pytest
import cipher.caesar as caesar

ORIGINAL_MESSAGE = "This is my secret message."
CIPHERED_MESSAGE_KEY_13 = "guv6Jv6Jz!J6rp5r7Jzr66ntrM"
TEST_KEY = 13


@pytest.mark.quick_test
def test_cipher():
    ciphered_text = caesar.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_13


@pytest.mark.quick_test
def test_decipher():
    deciphered_text = caesar.decipher(CIPHERED_MESSAGE_KEY_13, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE


