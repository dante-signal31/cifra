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


def _init_transposition_matrix(key: int, text: str, ciphering: bool = True) -> List[List[str]]:
    """
    Create matrix used to store characters and perform transposition operations.

    :param key: Secret key used for transposition.
    :param text: Text to cipher.
    :param ciphering: If true then we are populating a transposition matrix
      for ciphering purposes. If false then we are using this function to
      populate a transposition matrix fro deciphering.
    :return: Transposition matrix in its default state.
    """
    matrix = []
    text_length = len(text)
    total_rows = math.ceil(text_length / key) if ciphering else key
    total_columns = key if ciphering else math.ceil(len(text) / key)
    blank_row = [""] * total_columns
    for i in range(total_rows):
        matrix.append(copy.deepcopy(blank_row))
    remainder = (total_columns * total_rows) - text_length
    for i in range(remainder):
        if ciphering:
            matrix[-1][-1*(i+1)] = None
        else:
            matrix[-1*(i+1)][-1] = None
    return matrix


def _populate_transposition_matrix(key: int, text: str,
                                   transposition_matrix: List[List[str]],
                                   ciphering: bool = True) -> List[List[str]]:
    """
    Store text to cipher in transposition matrix.

    :param key: Text to be ciphered.
    :param text: Secret key.
    :param transposition_matrix: Transposition matrix in its default state.
    :param ciphering: If true then we are populating a transposition matrix
      for ciphering purposes. If false then we are using this function to
      populate a transposition matrix fro deciphering.
    :return: transposition_matrix with text to cipher stored inside it.
    """
    total_columns = key if ciphering else math.ceil(len(text) / key)
    offset = 0
    for index, char in enumerate(text):
        row, column = _calculate_position(index + offset, total_columns)
        if transposition_matrix[row][column] is None:
            # Actually we only get here on deciphering cases.
            offset += 1
            row, column = _calculate_position(index + offset, total_columns)
        transposition_matrix[row][column] = char
    # I know transposition_matrix is passed by reference but I find clearer
    # to return it back for a rebinding to another variable.
    return transposition_matrix


def _calculate_position(index: int, total_columns: int) -> (int, int):
    """
    Get matrix coordinates of a given index, based on columns table.

    :param index: Searched index.
    :param total_columns: How many columns per row this matrix has.
    :return: (row, column) for given index.
    """
    row = int(index / total_columns)
    column = index % total_columns
    return row, column


def _get_transposed_text(key: int,
                         populated_transposition_matrix: List[List[str]],
                         ciphering: bool = True) -> str:
    """
    Get transposed characters from populated transposition matrix.

    :param key: Secret key.
    :param populated_transposition_matrix: Transposition matrix with text to cipher stored inside it.
    :param ciphering: If true then we are populating a transposition matrix
      for ciphering purposes. If false then we are using this function to
      populate a transposition matrix fro deciphering.
    :return: Text cohered by transposition method.
    """
    total_columns = len(populated_transposition_matrix[0])
    recovered_text = "".join([row[i]
                             for i in range(total_columns)
                             for row in populated_transposition_matrix
                             if row[i] is not None])
    return recovered_text


def decipher(ciphered_text: str, key: int) -> str:
    """
    Decipher given text using transposition method.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key.
    :return: Deciphered text.
    """
    deciphering_matrix = _init_transposition_matrix(key, ciphered_text, False)
    populated_deciphering_matrix = _populate_transposition_matrix(key,
                                                                  ciphered_text,
                                                                  deciphering_matrix,
                                                                  False)
    deciphered_text = _get_transposed_text(key, populated_deciphering_matrix)
    return deciphered_text
