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
    ciphered_text = _transpose_text(text, key, ciphering=True)
    return ciphered_text


def decipher(ciphered_text: str, key: int) -> str:
    """
    Decipher given text using transposition method.

    :param ciphered_text: Text to be deciphered.
    :param key: Secret key.
    :return: Deciphered text.
    """
    deciphered_text = _transpose_text(ciphered_text, key, ciphering=False)
    return deciphered_text


def _transpose_text(text: str, key: int, ciphering: bool) -> str:
    """
    Transpose given text.

    :param text: Text to transpose.
    :param key: Key for transposition.
    :param ciphering: True if we are using transposition for ciphering. False if
       we are using it for deciphering.
    :return: Transposed text.
    """
    matrix = _init_transposition_matrix(key, text, ciphering)
    populated_matrix = _populate_transposition_matrix(key,
                                                      text,
                                                      matrix,
                                                      ciphering)
    recovered_text = _get_transposed_text(populated_matrix)
    return recovered_text


def _init_transposition_matrix(key: int, text: str,
                               ciphering: bool = True) -> List[List[str]]:
    """
    Create matrix used to store characters and perform transposition operations.

    :param key: Secret key used for transposition.
    :param text: Text to transpose.
    :param ciphering: If true then we are populating a transposition matrix
      for ciphering purposes. If false then we are using this function to
      populate a transposition matrix from deciphering.
    :return: Transposition matrix in its default state.
    """
    total_rows, total_columns = _get_matrix_dimensions(key, text, ciphering)
    matrix = _create_matrix(total_rows, total_columns)
    matrix = _set_remainder_cells(ciphering, matrix, text)
    return matrix


def _get_matrix_dimensions(key: int, text: str, ciphering: bool) -> (int, int):
    """
    Get transposition matrix dimensions needed for given text and key.

    :param key: Secret key used for transposition.
    :param text: Text to transpose.
    :param ciphering: If true then we are populating a transposition matrix
      for ciphering purposes. If false then we are using this function to
      populate a transposition matrix from deciphering.
    :return: A tuple with matrix dimensions with format (rows, columns)
    """
    text_length = len(text)
    total_rows = math.ceil(text_length / key) if ciphering else key
    total_columns = key if ciphering else math.ceil(len(text) / key)
    return total_rows, total_columns


def _create_matrix(rows: int, columns: int) -> List[List[str]]:
    """
    Create an empty transposition matrix with given dimensions.

    :param rows: Amount of rows created matrix needs to have.
    :param columns: Amount of columns created matrix needs to have.
    :return: An empty transposition matrix.
    """
    matrix = []
    blank_row = [""] * columns
    for i in range(rows):
        matrix.append(copy.deepcopy(blank_row))
    return matrix


def _set_remainder_cells(ciphering: bool, matrix: List[List[str]],
                         text: str) -> List[List[str]]:
    """
    Mark not usable cells in transposition matrix with None.

    Usually, transposition matrix has more cells that those actually needed for
    text characters. Exceeding cells should be marked as None. Be aware that
    transposition algorithm appends exceeding cells in last row tail for
    ciphering matrix whereas uses last column tail for deciphering matrix.

    :param ciphering:
    :param matrix:
    :param text:
    :return:
    """
    text_length = len(text)
    total_rows = len(matrix)
    total_columns = len(matrix[0])
    remainder = (total_columns * total_rows) - text_length
    for i in range(remainder):
        if ciphering:
            matrix[-1][-1 * (i + 1)] = None
        else:
            matrix[-1 * (i + 1)][-1] = None
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
            # Actually we only get here on deciphering cases. When ciphering you
            # exhaust text characters before touching None cells, but when
            # deciphering you get can touch those cells when still distributing
            # chars through matrix. When you come across a cell marked as None
            # You should get over it and use next available cell (not marked
            # as None).
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


def _get_transposed_text(populated_transposition_matrix: List[List[str]]) -> str:
    """
    Get transposed characters from populated transposition matrix.

    :param key: Secret key.
    :param populated_transposition_matrix: Transposition matrix with text to
      cipher stored inside it.
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
