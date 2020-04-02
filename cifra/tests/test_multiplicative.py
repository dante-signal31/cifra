"""
Tests for cipher.multiplicative module.
"""
import cipher.multiplicative as multiplicative

ORIGINAL_MESSAGE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'"
CIPHERED_MESSAGE_KEY_17= "ARizCTk2EVm4GXo6IZq8Kbs0Mdu!Ofw.QhyBSj1DUl3FWn5HYp7Jar9Lct Nev?Pgx"
TEST_KEY = 17
TEST_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'"


def test_cipher():
    ciphered_text = multiplicative.cipher(ORIGINAL_MESSAGE, TEST_KEY)
    assert ciphered_text == CIPHERED_MESSAGE_KEY_17


def test_decipher():
    deciphered_text = multiplicative.decipher(CIPHERED_MESSAGE_KEY_17, TEST_KEY)
    assert deciphered_text == ORIGINAL_MESSAGE