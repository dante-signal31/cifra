"""Test for attack.vigenere module."""
import pytest
from typing import Iterator
from cifra.tests.test_dictionaries import loaded_dictionary_temp_dir, MICRO_DICTIONARIES
from cifra.attack.simple_attacks import _dictionary_word_key_generator


def mocked_dictionary_word_key_generator() -> Iterator[str]:
    """ Simulate return a iterator through every word in our dictionaries. """
    word_iterator = (word for language in MICRO_DICTIONARIES for word in MICRO_DICTIONARIES[language])
    return word_iterator


@pytest.mark.quick_test
def test_dictionary_word_key_generator(loaded_dictionary_temp_dir):
    expected_words = set((word for language in MICRO_DICTIONARIES for word in MICRO_DICTIONARIES[language]))
    recovered_words = set(_dictionary_word_key_generator(loaded_dictionary_temp_dir))
    assert recovered_words == expected_words