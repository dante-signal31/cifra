"""
Tests for attack.dictionaries module.
"""
import pytest
import tempfile

from cifra.attack.dictionaries import Dictionary, NotExistingLanguage

MICRO_DICTIONARIES = {
    "english": ["yes", "no", "dog", "cat"],
    "spanish": ["si", "no", "perro", "gato"],
    "french": ["qui", "non", "chien", "chat"],
    "german": ["ja", "nein", "hund", "katze"]
}

def test_open_not_existing_dictionary():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(NotExistingLanguage):
            with Dictionary.open("english", _database_path=temp_dir) as english_dictionary:
                pass


def test_open_existing_dictionary():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create not existing language.
        with Dictionary.open("english", create=True, _database_path=temp_dir) as english_dictionary:
            pass
        # Open newly created language
        with Dictionary.open("english", _database_path=temp_dir) as english_dictionary:
            assert english_dictionary._already_created()


def test_cwd_word():
    """Test if we can check for word existence, write a new word and finally delete it."""
    word = "test"
    with tempfile.TemporaryDirectory() as temp_dir:
        with Dictionary.open("english", create=True, _database_path=temp_dir) as english_dictionary:
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


def test_delete_language():
    """Test delete a language also removes its words."""
    language_to_remove = "german"
    with tempfile.TemporaryDirectory() as temp_dir:
        # Load test data.
        for language, words in MICRO_DICTIONARIES.items():
            with Dictionary.open(language, create=True, _database_path=temp_dir) as language_dictionary:
                _ = [language_dictionary.add_word(word) for word in words]
        # Check all words are stored at database:
        for language, words in MICRO_DICTIONARIES.items():
            with Dictionary.open(language, _database_path=temp_dir) as language_dictionary:
                assert all(language_dictionary.word_exists(word) for word in words)
        # Remove a dictionary.
        Dictionary.remove_language(language_to_remove, database_path=temp_dir)
        # Check all words from removed language have been removed too.
        not_existing_dictionary = Dictionary(language, temp_dir)
        not_existing_dictionary._open()
        assert all(not not_existing_dictionary.word_exists(word, _testing=True)
                   for word in MICRO_DICTIONARIES[language_to_remove])
        not_existing_dictionary._close()
