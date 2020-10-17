"""
Module for frequency attacks.
"""
from __future__ import annotations

from itertools import chain
from collections import Counter
from typing import Dict, List, Set

from cifra.attack.dictionaries import normalize_text
import cifra.cipher.common as common


class LetterHistogram(object):

    def __init__(self, text: str, matching_width: int = 6, charset: str = common.DEFAULT_CHARSET):
        """ Create a LetterHistogram instance reading a text.

        :param text: Text to read.
        :param matching_width: Desired length for top and bottom matching list.
        :param charset: Minimum charset expected in given text.
        :return: A dict whose keys are detected letters and values are float ranging
            from 0 to 1, being 1 as this letter is the only one in text and 0 as this
            letter does not happen in this text (actually that value is
            impossible because it would not exist that key). Keys are ordered from higher
            value to lesser.
        """
        self._charset = charset
        normalized_words = normalize_text(text)
        letter_sequence = "".join(normalized_words)
        letter_counter = Counter(letter_sequence)
        self._total_letters: int = sum(letter_counter.values())
        self._ordered_dict = self._create_ordered_list(letter_counter)
        self._top_matching_letters: List[str] = []
        self._bottom_matching_letters: List[str] = []
        self.set_matching_width(matching_width)

    def _create_ordered_list(self, letter_counter: Counter) -> Dict[str, int]:
        """ Create an ordered dict ordering by values.

        Equal values are sorted by keys alphabetically.

        :return: Ordered dict.
        """
        ordered_dict_by_values = {key: value
                                  for (key, value) in letter_counter.most_common()}
        charset_letters_not_in_text = (letter.lower() for letter in self._charset
                                       if letter.lower() not in ordered_dict_by_values and letter.isalpha())
        for letter in charset_letters_not_in_text:
            ordered_dict_by_values.update({letter: 0})
        values_set = sorted(set(ordered_dict_by_values.values()), reverse=True)
        key_bins = [[key for (key, _value) in ordered_dict_by_values.items() if _value == value]
                    for value in values_set]
        key_bins_ordered = [sorted(bin) for bin in key_bins]
        ordered_dict_by_values_and_keys = {key: ordered_dict_by_values[key]
                                           for key in chain(*key_bins_ordered)}
        return ordered_dict_by_values_and_keys

    def __getitem__(self, item):
        return self._ordered_dict[item]

    def frequency(self, key: str) -> float:
        """ Return frequency for given letter.

        Frequency is the possibility of occurrence of given letter inside a normal text.
        Its value goes from 0 to 1.

        :return: Probability of occurrence of given letter.
        """
        return float(self._ordered_dict[key])/self._total_letters

    @property
    def top_matching(self) -> List[str]:
        """ Return a list with most probable letters in given text.

        You can change length of this list calling set_matching_width().
        """
        return self._top_matching_letters

    @property
    def bottom_matching(self):
        """ Return a list with least probable letters in given text.

        You can change length of this list calling set_matching_width().
        """
        return self._bottom_matching_letters

    def letters(self):
        """ Return letters whose frequency we have. """
        return self._ordered_dict.keys()

    def set_matching_width(self, width: int):
        """ Set top and bottom matching to have desired length.

        By default top and bottom matching lists have 6 letters length, but
        with this method you can change that.
        """
        self._top_matching_letters = list(self._ordered_dict.keys())[:width]
        self._bottom_matching_letters = list(self._ordered_dict.keys())[-width:]

    @staticmethod
    def match_score(one: LetterHistogram, other: LetterHistogram) -> int:
        """ Compare two LetterHistogram instances.

        Score is calculated counting how many letters are in matching extremes of
        both instances. A coincidence is counted only if is present in top matching
        in both instances or in bottom matching in both instances.

        If matching extremes are of X length, then maximum score is of 2 * X.

        :param one: First instance to compare.
        :param other: Second instance to compare.
        :return: Integer score. The higher the more coincidence between two instances.
        """
        top_match = sum(1 for letter in one.top_matching if letter in other.top_matching)
        bottom_match = sum(1 for letter in one.bottom_matching if letter in other.bottom_matching)
        return top_match + bottom_match


def find_repeated_sequences(text: str, length: int = 3) -> Dict[str, List[int]]:
    """ Take a text a return repeated patterns with its separations.

    :param text: Text to analyze.
    :param length: Length of patterns to search for.
    :return: A dict whose keys are found patterns and its values are a list of
        integers with separations between found patters.
    """
    normalized_words = normalize_text(text)
    char_string = "".join(normalized_words)
    char_string_length = len(text)
    sequences: Dict[str, List[int]] = dict()
    for i, char in enumerate(char_string):
        sequence_to_find = char_string[i:i+length]
        if sequence_to_find in sequences:
            continue
        index = i
        previous_index = 0
        # First pass: adjacent spaces.
        while index < char_string_length:
            index = char_string.find(sequence_to_find, index)
            if index == -1:
                break
            elif not previous_index == 0:
                separation = index - previous_index
                if sequence_to_find not in sequences:
                    sequences[sequence_to_find] = [separation]
                else:
                    try:
                        sequences[sequence_to_find].index(sequence_to_find)
                    except ValueError:
                        sequences[sequence_to_find].append(separation)
            previous_index = index
            index += length
    # Second pass: spaces not adjacent
    for sequence in sequences:
        not_adjacent_spaces = []
        sequence_length = len(sequences[sequence])
        if sequence_length > 1:
            for i, space in enumerate(sequences[sequence]):
                for n in range(sequence_length, i+1, -1):
                    spaces_to_add = sequences[sequence][i+1:n]
                    not_adjacent_spaces.append(space + sum(spaces_to_add))
            sequences[sequence].extend(not_adjacent_spaces)
    return sequences
