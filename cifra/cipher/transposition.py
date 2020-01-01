"""
Library to cipher and decipher texts using transposition method.
"""
import math
import copy
from typing import List


def cipher(text: str, key: int) -> str:
    """
    Cipher given text using transposition method.

    :param text: Text to be ciphered.
    :param key: Secret key.
    :return: Ciphered text.
    """
    transposition_matrix = _init_transposition_matrix(key, text)
    populated_transposition_matrix = _populate_transposition_matrix(key,
                                                                    text,
                                                                    transposition_matrix)
    ciphered_text = _get_transposed_text(key, populated_transposition_matrix)
    return ciphered_text


def _init_transposition_matrix(key: int, text: str) -> List[List[str]]:
    """
    Create matrix used to store characters and perform transposition operations.

    Created matrix is going to have as many columns as set by *key*, and as many
    row as needed  to store every char in *text* in its cell.

    :param key: Secret key used for transposition.
    :param text: Text to cipher.
    :return: Transposition matrix in its default state.
    """
    matrix = []
    total_rows = math.ceil(len(text) / key)
    blank_row = [None] * key
    for i in range(total_rows):
        matrix.append(copy.deepcopy(blank_row))
    return matrix


def _populate_transposition_matrix(key: int, text: str,
                                   transposition_matrix: List[List[str]]) -> List[List[str]]:
    """
    Store text to cipher in transposition matrix.

    :param key: Text to be ciphered.
    :param text: Secret key.
    :param transposition_matrix: Transposition matrix in its default state.
    :return: transposition_matrix with text to cipher stored inside it.
    """
    for index, char in enumerate(text):
        row = int(index / key)
        column = index % key
        transposition_matrix[row][column] = char
    # I know transposition_matrix is passed by reference but I find clearer
    # to return it back for a rebinding to another variable.
    return transposition_matrix


def _get_transposed_text(key: int,
                         populated_transposition_matrix: List[List[str]]) -> str:
    """
    Get transposed characters from populated transposition matrix.

    :param key: Secret key.
    :param populated_transposition_matrix: Transposition matrix with text to cipher stored inside it.
    :return: Text cohered by transposition method.
    """
    ciphered_text = "".join([row[i]
                             for i in range(key)
                             for row in populated_transposition_matrix
                             if row[i] is not None])
    return ciphered_text


def decipher(ciphered_text: str, key: int) -> str:
    """
    Decipher given text using transposition method.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key.
    :return: Deciphered text.
    """
    raise NotImplementedError
