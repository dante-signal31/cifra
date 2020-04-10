"""Test for attack.affine module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.affine import brute_force, brute_force_mp
from cifra.cipher.affine import decipher, cipher, get_random_key
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries


ORIGINAL_MESSAGE = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
CIPHERED_MESSAGE_KEY_331 = "eiTven8TXvqH/u.?/CqqlvLi.?JT33DSvD?vESn?xvDYvXTJD?OvE.n3DhcvYDSvE.?xX"
TEST_KEY = 331


@pytest.mark.slow_test
def test_brute_force_affine(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force(CIPHERED_MESSAGE_KEY_331, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_affine: {elapsed_time[0]} seconds.")


@pytest.mark.slow_test
def test_brute_force_affine_mp(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp(CIPHERED_MESSAGE_KEY_331, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_affine_mp: {elapsed_time[0]} seconds.")


def _assert_found_key(found_key) -> None:
    assert found_key == TEST_KEY
    deciphered_text = decipher(CIPHERED_MESSAGE_KEY_331, found_key)
    assert deciphered_text == ORIGINAL_MESSAGE
