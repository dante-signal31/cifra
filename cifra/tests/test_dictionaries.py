"""
Tests for attack.dictionaries module.
"""
import pytest
import tempfile

from cifra.attack.dictionaries import Dictionary, NotExistingLanguage


def test_open_not_existing_dictionary():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(NotExistingLanguage):
            with Dictionary.open("english", database_path=temp_dir) as english_dictionary:
                pass


def test_open_existing_dictionary():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create not existing language.
        with Dictionary.open("english", create=True, database_path=temp_dir) as english_dictionary:
            pass
        # Open newly created language
        with Dictionary.open("english", database_path=temp_dir) as english_dictionary:
            assert english_dictionary._already_created()


def test_cwd_word():
    """Test if we can check for word existence, write a new word and finally delete it."""
    word = "test"
    with tempfile.TemporaryDirectory() as temp_dir:
        with Dictionary.open("english", create=True, database_path=temp_dir) as english_dictionary:
            assert not english_dictionary.word_exists(word)
            english_dictionary.add_word(word)
            assert english_dictionary.word_exists(word)
            english_dictionary.remove_word(word)
            assert not english_dictionary.word_exists(word)


def test_create_language():
    """Test a new language creation at database."""
    with tempfile.TemporaryDirectory() as temp_dir:
        english_dictionary = Dictionary("english", database_path=temp_dir)
        english_dictionary._open()
        assert not english_dictionary._already_created()
        english_dictionary._create_dictionary()
        assert english_dictionary._already_created()
        english_dictionary._close()


# TODO: Add a test to try cascade deleting when an entire language is removed.