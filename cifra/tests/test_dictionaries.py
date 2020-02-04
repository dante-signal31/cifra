"""
Tests for attack.dictionaries module.
"""
import pytest

from cifra.attack.dictionaries import Dictionary, NotExistingLanguage


def test_open_not_existing_dictionary():
    with pytest.raises(NotExistingLanguage):
        with Dictionary.open("english") as english_dictionary:
            pass


def test_open_existing_dictionary():
    # Create not existing language.
    with Dictionary.open("english", True) as english_dictionary:
        pass
    # Open newly created language
    with Dictionary.open("english") as english_dictionary:
        assert english_dictionary._already_created()


def test_cwd_word():
    """Test if we can check for word existence, write a new word and finally delete it."""
    word = "test"
    with Dictionary.open("english") as english_dictionary:
        assert not english_dictionary.word_exists(word)
        english_dictionary.add_word(word)
        assert english_dictionary.word_exists(word)
        english_dictionary.remove_word(word)
        assert not english_dictionary.word_exists(word)


def test_create_language():
    with Dictionary.open("english") as english_dictionary:
        assert not english_dictionary._already_created()
        english_dictionary._create_dictionary()
        assert english_dictionary._already_created()


