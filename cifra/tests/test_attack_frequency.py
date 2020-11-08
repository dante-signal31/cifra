"""
Tests for attack.frequency module.
"""
import math

import pytest

# TODO: Change import for normalize_text() to point to cipher.common module.
from cifra.attack.frequency import LetterHistogram, normalize_text, \
    find_repeated_sequences, get_substrings, match_substring, find_most_likely_subkeys
from cifra.tests.test_dictionaries import ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS


@pytest.fixture(scope="session")
def language_histogram() -> LetterHistogram:
    """Create a letter histogram for english language.

    :return: Yields a LetterHistogram for english language.
    """
    with open("cifra/tests/resources/english_book.txt") as text_file:
        population_text = text_file.read()
    language_histogram = LetterHistogram(text=population_text, matching_width=6)
    yield language_histogram


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
    histogram = LetterHistogram(text=text)
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
    frequencies = LetterHistogram(text=text)
    frequencies.set_matching_width(3)
    assert frequencies.top_matching == expected_top
    assert frequencies.bottom_matching == expected_bottom


@pytest.mark.quick_test
def test_match_score(language_histogram):
    text = "Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm " \
           "rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia " \
           "esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao " \
           "rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr " \
           "sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia " \
           "pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm"
    expected_match_score = 5
    text_histogram = LetterHistogram(text=text, matching_width=6)
    match_score = LetterHistogram.match_score(language_histogram, text_histogram)
    assert match_score == expected_match_score


@pytest.mark.quick_test
def test_find_repeated_sequences():
    ciphered_text = "PPQCA XQVEKG YBNKMAZU YBNGBAL JON I TSZM JYIM. VRAG VOHT VRAU C TKSG. DDWUO XITLAZU VAVV RAZ C VKB QP IWPOU"
    expected_patterns = {
        "ybn": [8],
        "azu": [48],
        "vra": [8, 24, 32]
    }
    found_patterns = find_repeated_sequences(ciphered_text, length=3)
    assert set(found_patterns) == set(expected_patterns)


@pytest.mark.quick_test
def test_find_repeated_sequences_many_repetitions():
    ciphered_text = "PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIM. VRA GVOHT VRA UCTKSG.DDWUOXITLAZUVAV VRA ZCVKBQPIWPOUX VRA WZ VRA"
    expected_patterns = {
        "ybn": [8],
        "azu": [48],
        "vra": [8, 24, 16, 5, 32, 48, 53, 40, 45, 21]
    }
    found_patterns = find_repeated_sequences(ciphered_text, length=3)
    assert set(found_patterns) == set(expected_patterns)


@pytest.mark.quick_test
def test_get_substrings():
    ciphertext = "abc dabc dabcd abcd"
    substrings = get_substrings(ciphertext, 4)
    assert substrings[0] == "aaaa"
    assert substrings[1] == "bbbb"
    assert substrings[2] == "cccc"
    assert substrings[3] == "dddd"


@pytest.mark.quick_test
def test_match_substring(language_histogram):
    substring = "PAEBABANZIAHAKDXAAAKIU"
    expected_result = 4
    match_result = match_substring(substring, language_histogram)
    assert match_result == expected_result


@pytest.mark.quick_test
def test_most_likely_subkey(language_histogram):
    ciphered_substring = "PAEBABANZIAHAKDXAAAKIU"
    expected_result = ["p", "t", "w", "x"]
    result = find_most_likely_subkeys(ciphered_substring, language_histogram)
    assert result == expected_result

