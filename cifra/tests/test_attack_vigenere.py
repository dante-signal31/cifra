"""Test for attack.vigenere module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.vigenere import brute_force, brute_force_mp, statistical_brute_force, _get_likely_key_lengths
from cifra.cipher.vigenere import decipher, cipher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries

ORIGINAL_MESSAGE = "The real secrets are not the ones I tell."
CIPHERED_MESSAGE = "Vhx tetn sxerxvs tte gqt mje hpel K txnl."
TEST_KEY = "cat"


@pytest.fixture(scope="session")
def vigenere_ciphered_english_book():
    """ Get example english text ciphered with key 'cat' using Vigenere cipher. """
    text_file_pathname = "cifra/tests/resources/english_book.txt"
    ciphered_book_text = ""
    with open(text_file_pathname) as book:
        book_text = book.read()
        ciphered_book_text = cipher(book_text, TEST_KEY)
    yield ciphered_book_text

@pytest.mark.slow_test
def test_brute_force_vigenere(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force(CIPHERED_MESSAGE, _database_path=loaded_dictionaries.temp_dir, _testing=True)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_vigenere: {elapsed_time[0]} seconds.")


@pytest.mark.slow_test
def test_brute_force_vigenere_mp(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp(CIPHERED_MESSAGE, _database_path=loaded_dictionaries.temp_dir, _testing=True)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_vigenere_mp: {elapsed_time[0]} seconds.")


def _assert_found_key(found_key):
    assert found_key == TEST_KEY
    deciphered_text = decipher(CIPHERED_MESSAGE, found_key)
    assert deciphered_text == ORIGINAL_MESSAGE


@pytest.mark.slow_test
def test_statistical_brute_force_vigenere(loaded_dictionaries: LoadedDictionaries,
                                          vigenere_ciphered_english_book: str):
    ciphered_text = "PPQCA XQVEKG YBNKMAZU YBNGBAL JON I TSZM JYIM. VRAG VOHT VRAU C TKSG. DDWUO XITLAZU VAVV RAZ C VKB QP IWPOU"
    test_key = "wick"
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = statistical_brute_force(ciphered_text, _database_path=loaded_dictionaries.temp_dir,
                                            maximum_key_length=4)
        assert found_key == test_key
    print(f"\n\nElapsed time with test_brute_force_vigenere_mp: {elapsed_time[0]} seconds.")

@pytest.mark.quick_test
def test_get_likely_key_lengths():
    ciphered_text = "PPQCA XQVEKG YBNKMAZU YBNGBAL JON I TSZM JYIM. VRAG VOHT VRAU C TKSG. DDWUO XITLAZU VAVV RAZ C VKB QP IWPOU"
    likely_key_lengths = _get_likely_key_lengths(ciphered_text, 8)
    assert likely_key_lengths[0] == 2
    assert likely_key_lengths[1] == 4
    assert likely_key_lengths[2] == 8