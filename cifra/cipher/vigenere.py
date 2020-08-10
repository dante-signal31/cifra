"""
Library to cipher and decipher texts using Vigenere method.
"""
from common import _offset_text, Ciphers

# To keep along with book examples I'm going to work with an only lowercase
# charset.
DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyz"


def cipher(text: str, key: str, charset: str = DEFAULT_CHARSET) -> str:
    """ Cipher given text using Vigenere method.

    Be aware that different languages use different charsets. Default charset
    is for english language, if you are using any other you should use a proper
    dataset. For instance, if you are ciphering an spanish text, you should use
    a charset with "ñ" character.

    This module uses only lowercase charsets. That means that caps will be kept
    but lowercase and uppercase will follow ths same substitutions.

    :param text: Text to be ciphered.
    :param key: Secret key. Both ends should know this and
     use the same one. The longer key you use the harder to break ciphered text.
    :param charset: Charset used for Vigenere method. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :return: Ciphered text.
    """
    key_length = len(key)
    offset_chars = []
    skip_accumulator = 0
    for index, char in enumerate(text):
        if char.lower() not in charset:
            offset_chars.append(char)
            skip_accumulator += 1
            continue
        subkey_char = key[(index - skip_accumulator) % key_length]
        subkey_offset = charset.find(subkey_char)
        if char.islower():
            offset_char = _offset_text(char, subkey_offset, True, Ciphers.VIGENERE, charset)
        else:
            offset_char = _offset_text(char.lower(), subkey_offset, True, Ciphers.VIGENERE, charset)
            offset_char = offset_char.upper()
        offset_chars.append(offset_char)
    ciphered_text = "".join(offset_chars)
    return ciphered_text


def decipher(ciphered_text: str, key: str, charset: str = DEFAULT_CHARSET) -> str:
    """ Decipher given text using vigenere method.

    Note you should use the same charset that ciphering end did.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key. Both ends should know this and
     use the same one. The longer key you use the harder to break ciphered text.
    :param charset: Charset used for Vigenere method. Both end should
    use the same charset or original text won't be properly recovered.
    :return: Deciphered text.
    """
    raise NotImplementedError
