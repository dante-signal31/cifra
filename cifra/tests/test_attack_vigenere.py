"""Test for attack.vigenere module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.vigenere import brute_force, brute_force_mp, statistical_brute_force
from cifra.cipher.vigenere import decipher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries

ORIGINAL_MESSAGE = "The real secrets are not the ones I tell."
CIPHERED_MESSAGE = "Vhx tetn sxerxvs tte gqt mje hpel K txnl."
TEST_KEY = "cat"


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
def test_statistical_brute_force_vigenere(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = statistical_brute_force(CIPHERED_MESSAGE, _database_path=loaded_dictionaries.temp_dir,
                                            maximum_key_length=3)
        assert found_key == TEST_KEY
    print(f"\n\nElapsed time with test_brute_force_vigenere_mp: {elapsed_time[0]} seconds.")