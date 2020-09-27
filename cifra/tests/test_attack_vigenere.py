"""Test for attack.vigenere module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.vigenere import brute_force, brute_force_mp
from cifra.cipher.vigenere import decipher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries, loaded_dictionary_temp_dir

ORIGINAL_MESSAGE = "The real secrets are not the ones I tell."
CIPHERED_MESSAGE = "Lue bisy sogjrtc ejr nyx lue yrwf I didy."
TEST_KEY = "snake"


@pytest.mark.slow_test
def test_brute_force_vigenere(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force(CIPHERED_MESSAGE, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


@pytest.mark.slow_test
def test_brute_force_vigenere_mp(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp(CIPHERED_MESSAGE, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar_mp: {elapsed_time[0]} seconds.")


def _assert_found_key(found_key):
    assert found_key == TEST_KEY
    deciphered_text = decipher(CIPHERED_MESSAGE, found_key)
    assert deciphered_text == ORIGINAL_MESSAGE