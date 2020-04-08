"""Test for attack.affine module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.affine import brute_force, brute_force_mp
from cifra.cipher.affine import decipher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries

ORIGINAL_MESSAGE = ""
CIPHERED_MESSAGE_79 = ""
TEST_KEY = 79

@pytest.mark.slow_test
def test_brute_force_affine(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


@pytest.mark.slow_test
def test_brute_force_affine_mp(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar_mp: {elapsed_time[0]} seconds.")


def _assert_found_key(found_key):
    assert found_key == TEST_KEY
    deciphered_text = decipher(CIPHERED_MESSAGE_KEY_13, found_key)
    assert deciphered_text == ORIGINAL_MESSAGE