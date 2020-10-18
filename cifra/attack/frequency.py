"""
Module for frequency attacks.
"""
from __future__ import annotations

from itertools import chain
from collections import Counter
from typing import Dict, List, Set

from cifra.attack.dictionaries import normalize_text
import cifra.cipher.common as common
from cifra.cipher.vigenere import decipher, DEFAULT_CHARSET


class LetterHistogram(object):

    def __init__(self, letters: Dict[str, int], matching_width: int = 6, charset: str = DEFAULT_CHARSET):
        """ Create a LetterHistogram instance from a dict with letters as keys and occurrences for values.

        :param letters: A dict with letters as keys and occurrences for values.
        :param matching_width: Desired length for top and bottom matching list.
        :param charset: Minimum charset expected in given text.
        """
        self._charset = charset
        self._total_letters = sum(letters.values())
        letter_counter = Counter(letters)
        self._ordered_dict = self._create_ordered_dict(letter_counter)
        self._top_matching_letters: List[str] = []
        self._bottom_matching_letters: List[str] = []
        self.set_matching_width(matching_width)


    def __init__(self, text: str, matching_width: int = 6, charset: str = DEFAULT_CHARSET):
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
        self._ordered_dict = self._create_ordered_dict(letter_counter)
        self._top_matching_letters: List[str] = []
        self._bottom_matching_letters: List[str] = []
        self.set_matching_width(matching_width)

    def _create_ordered_dict(self, letter_counter: Counter) -> Dict[str, int]:
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

    @property
    def charset(self):
        """ Return charset used in this histogram. """
        return self._charset

    def letters(self):
        """ Return letters whose frequency we have. """
        return self._ordered_dict.keys()

    def items(self):
        """ Return letters-counters pairs. """
        return self._ordered_dict.items()

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
        integers with separations between found patterns.
    """
    sequences = _find_adjacent_separations(text, length)
    _find_not_adjacent_separations(sequences)
    return sequences


def _find_adjacent_separations(text: str, length: int) -> Dict[str, List[int]]:
    """ Find repeated sequences of given length and separations between adjacent
    repeated sequences.

    :param text: Text to analyze.
    :param length: Length of patterns to search for.
    :return: A dict whose keys are found patterns and its values are a list of
        integers with separations between adjacent found patters.
    """
    normalized_words = normalize_text(text)
    char_string = "".join(normalized_words)
    char_string_length = len(text)
    sequences = dict()
    for i, char in enumerate(char_string):
        sequence_to_find = char_string[i:i + length]
        if sequence_to_find not in sequences:
            index = i + length
            previous_index = i
            while index < char_string_length:
                if (index := char_string.find(sequence_to_find, index)) == -1:
                    break
                else:
                    separation = index - previous_index
                    if sequence_to_find not in sequences:
                        sequences[sequence_to_find] = [separation]
                    else:
                        sequences[sequence_to_find].append(separation)
                previous_index = index
                index += length
    return sequences


def _find_not_adjacent_separations(sequences: Dict[str, List[int]]) -> None:
    """ Complete a dict of repeated sequences calculating separation between
    not adjacent repetitions.

    :param sequences: A dict whose keys are found patterns and its values are a list of
        integers with separations between adjacent found patters. This dict will be
        updated in place with calculated sequences.
    """
    for sequence in sequences:
        not_adjacent_spaces = []
        sequence_length = len(sequences[sequence])
        if sequence_length > 1:
            for i, space in enumerate(sequences[sequence]):
                for n in range(sequence_length, i + 1, -1):
                    spaces_to_add = sequences[sequence][i + 1:n]
                    not_adjacent_spaces.append(space + sum(spaces_to_add))
            sequences[sequence].extend(not_adjacent_spaces)


def get_substrings(ciphertext: str, step: int) -> List[str]:
    """ Get substrings for a given step.

    .. code-block:: python
        ciphertext = "abcdabcdabcdabcd"
        substrings = get_substrings(ciphertext, 4)
        assert substrings[0] == "aaaa"
        assert substrings[1] == "bbbb"
        assert substrings[2] == "cccc"
        assert substrings[3] == "dddd"

    :param ciphertext: Text to extract substrings from.
    :param step: How many letters lap before extracting next substring letter.
    :return: A list with substrings. This lists will have the same length as step parameter.
    """
    substrings = []
    for i in range(step):
        substring = ciphertext[i::step]
        substrings.append(substring)
    return substrings


def match_substring(substring: str, reference_histogram: LetterHistogram) -> int:
    """ Compare a substring against a known letter histogram.

    The higher the returned value the more likely this substring is from the same
    language as reference histogram.

    :param substring: String to compare.
    :param reference_histogram: Histogram to compare against.
    :return: Score value.
    """
    substring_histogram = LetterHistogram(substring)
    match_result = LetterHistogram.match_score(substring_histogram, reference_histogram)
    return match_result


def find_most_likely_subkeys(substring: str, reference_histogram: LetterHistogram, amount: int) -> List[str]:
    """ Get the most likely letters used to get given ciphered substring in the context of
    given language histogram.

    :param substring: Ciphered substring.
    :param reference_histogram: Histogram to compare against.
    :param amount: How many likely subkeys to estimate.
    :return: A list of letters as most likely candidates to be the key for given ciphered substring.
    """
    scores: Dict[str, int] = dict()
    for letter in reference_histogram.charset:
        deciphered_text = decipher(substring, letter, reference_histogram.charset)
        deciphered_histogram = LetterHistogram(deciphered_text, charset=reference_histogram.charset)
        score = LetterHistogram.match_score(deciphered_histogram, reference_histogram)
        scores[letter] = score
    scores_counter = Counter(scores)
    most_likely_subkeys = sorted([key for key, value in scores_counter.most_common(amount)])
    return most_likely_subkeys
