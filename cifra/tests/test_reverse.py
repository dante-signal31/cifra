"""
Tests for encoding.reverse module.
"""
import cifra.encoding.reverse as reverse

ORIGINAL_MESSAGE = "Three can keep a secret, if two of them are dead."
REVERSED_MESSAGE = ".daed era meht fo owt fi ,terces a peek nac eerhT"


def test_reverse_encode():
    encoded_text = reverse.encode(ORIGINAL_MESSAGE)
    assert encoded_text == REVERSED_MESSAGE


def test_reverse_decode():
    decoded_text = reverse.decode(REVERSED_MESSAGE)
    assert decoded_text == ORIGINAL_MESSAGE
