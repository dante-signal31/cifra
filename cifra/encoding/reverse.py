"""
Reverse encoding functions.

Reverse encoding is the simplest of encoding methods. It just reverses order of
text characters.
"""


def encode(text: str) -> str:
    """
    Reverse order of given text characters.

    :param text: Text to reverse.
    :return: Reversed text.
    """
    reversed_text = "".join(char for char in text[-1::-1])
    return reversed_text


def decode(text: str) -> str:
    """
    Obtain original text from a reversed text.

    :param text: Reversed text.
    :return: Original text.
    """
    # Reverse of reverse is original text.
    return encode(text)

