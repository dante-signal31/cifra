"""
Tests for attack.frequency module.
"""
import math

import pytest

from cifra.attack.frequency import LetterHistogram, normalize_text
from cifra.tests.test_dictionaries import ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS


@pytest.mark.quick_test
def test_normalize_text():
    expected_list = ["this", "ebook", "is", "for", "the", "use", "of", "anyone",
                     "anywhere", "at", "no", "cost", "and", "with", "almost", "no",
                     "restrictions", "whatsoever", "you", "may", "copy", "it",
                     "give", "it", "away", "or", "re", "use", "it", "under", "the",
                     "terms", "of", "the", "project", "gutenberg", "license",
                     "included", "with", "this", "ebook", "or", "online", "at"]
    returned_list = normalize_text(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS)
    assert returned_list == expected_list


@pytest.mark.quick_test
def test_get_letter_frequency():
    text = "Aaaa bb, c, da-a. efg\r\nggg"
    expected_frequencies = {
        "a": float(6)/16,
        "g": float(4)/16,
        "b": float(2)/16,
        "c": float(1)/16,
        "d": float(1)/16,
        "e": float(1)/16,
        "f": float(1)/16
    }
    histogram = LetterHistogram(text)
    # Test calculated histogram are correct.
    for letter in expected_frequencies:
        assert math.isclose(histogram.frequency(letter), expected_frequencies[letter], abs_tol=0.01)
    # Test ordering is correct.
    expected_letters = list(expected_frequencies.keys())
    returned_letters = list(histogram.letters())
    for i in range(3):
        assert returned_letters[i] == expected_letters[i]


@pytest.mark.quick_test
def test_set_matching_width():
    text = "Aaaa bb, c, da-a. efg\r\nggg"
    expected_top = ["a", "g", "b"]
    expected_bottom = ["x", "y", "z"]
    frequencies = LetterHistogram(text)
    frequencies.set_matching_width(3)
    assert frequencies.top_matching == expected_top
    assert frequencies.bottom_matching == expected_bottom


@pytest.mark.quick_test
def test_match_score():
    with open("cifra/tests/resources/english_book.txt") as text_file:
        population_text = text_file.read()
    text = "Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm " \
           "rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia " \
           "esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao " \
           "rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr " \
           "sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia " \
           "pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm"
    expected_match_score = 5
    language_histogram = LetterHistogram(population_text, matching_width=6)
    text_histogram = LetterHistogram(text, matching_width=6)
    match_score = LetterHistogram.match_score(language_histogram, text_histogram)
    assert match_score == expected_match_score
