"""Test for attack.caesar module."""
import pytest
from test_common.benchmark.timing import timeit

from cifra.attack.caesar import brute_force, brute_force_mp, \
    brute_force_in_memory, brute_force_in_pool, brute_force_in_pool_in_memory, \
    brute_force_mp_in_memory, brute_force_mp_in_pool, brute_force_mp_in_pool_in_memory
from cifra.cipher.caesar import decipher
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries

from cifra.tests.test_caesar import ORIGINAL_MESSAGE, CIPHERED_MESSAGE_KEY_13, \
    TEST_KEY


@pytest.mark.slow_test
def test_brute_force_caesar(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


@pytest.mark.slow_test
def test_brute_force_caesar_in_memory(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_in_memory(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


def test_brute_force_caesar_in_pool(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_in_pool(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


def test_brute_force_caesar_in_memory_pool(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_in_pool_in_memory(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")

@pytest.mark.slow_test
def test_brute_force_caesar_mp(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar_mp: {elapsed_time[0]} seconds.")

@pytest.mark.slow_test
def test_brute_force_caesar_mp_in_memory(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp_in_memory(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


def test_brute_force_caesar_mp_in_pool(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp_in_pool(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")


def test_brute_force_caesar_mp_in_memory_pool(loaded_dictionaries: LoadedDictionaries):
    elapsed_time = []
    with timeit(elapsed_time):
        found_key = brute_force_mp_in_pool_in_memory(CIPHERED_MESSAGE_KEY_13, _database_path=loaded_dictionaries.temp_dir)
        _assert_found_key(found_key)
    print(f"\n\nElapsed time with test_brute_force_caesar: {elapsed_time[0]} seconds.")

def _assert_found_key(found_key):
    assert found_key == TEST_KEY
    deciphered_text = decipher(CIPHERED_MESSAGE_KEY_13, found_key)
    assert deciphered_text == ORIGINAL_MESSAGE



