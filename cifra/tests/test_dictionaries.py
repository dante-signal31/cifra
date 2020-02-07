"""
Tests for attack.dictionaries module.
"""
import os
import pytest
import tempfile

from cifra.attack.dictionaries import Dictionary, NotExistingLanguage

MICRO_DICTIONARIES = {
    "english": ["yes", "no", "dog", "cat"],
    "spanish": ["si", "no", "perro", "gato"],
    "french": ["qui", "non", "chien", "chat"],
    "german": ["ja", "nein", "hund", "katze"]
}

ENGLISH_TEXT_FILE_NAME = "disclaimer.txt"

ENGLISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS = "This eBook is for the use of anyone anywhere at no cost and with\
almost no restrictions whatsoever You may copy it give it away or\
re-use it under the terms of the Project Gutenberg License included\
with this eBook or online at"

ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS = "This eBook is for the use of anyone anywhere at no cost and with\
almost no restrictions whatsoever.You may copy it, give it away or\
re-use it under the terms of the Project Gutenberg License included\
with this eBook or online at"


@pytest.fixture()
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_folder:
        yield temp_folder


@pytest.fixture()
def loaded_dictionary_temp_dir(temp_dir):
    # Load test data.
    for language, words in MICRO_DICTIONARIES.items():
        with Dictionary.open(language, create=True, _database_path=temp_dir) as language_dictionary:
            _ = [language_dictionary.add_word(word) for word in words]
    # Check all words are stored at database:
    for language, words in MICRO_DICTIONARIES.items():
        with Dictionary.open(language, _database_path=temp_dir) as language_dictionary:
            assert all(language_dictionary.word_exists(word) for word in words)
    yield temp_dir

@pytest.fixture()
def temporary_english_text_file(temp_dir):
    temporary_text_file_pathname = os.path.join(temp_dir, ENGLISH_TEXT_FILE_NAME)
    with open(temporary_text_file_pathname, "w") as text_file:
        text_file.write(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS)
        text_file.flush()
        yield text_file


def test_open_not_existing_dictionary(temp_dir):
    with pytest.raises(NotExistingLanguage):
        with Dictionary.open("english", _database_path=temp_dir) as english_dictionary:
            pass


def test_open_existing_dictionary(temp_dir):
    # Create not existing language.
    with Dictionary.open("english", create=True, _database_path=temp_dir) as english_dictionary:
        pass
    # Open newly created language
    with Dictionary.open("english", _database_path=temp_dir) as english_dictionary:
        assert english_dictionary._already_created()


def test_cwd_word(temp_dir):
    """Test if we can check for word existence, write a new word and finally delete it."""
    word = "test"
    with Dictionary.open("english", create=True, _database_path=temp_dir) as english_dictionary:
        assert not english_dictionary.word_exists(word)
        english_dictionary.add_word(word)
        assert english_dictionary.word_exists(word)
        english_dictionary.remove_word(word)
        assert not english_dictionary.word_exists(word)


def test_create_language(temp_dir):
    """Test a new language creation at database."""
    english_dictionary = Dictionary("english", database_path=temp_dir)
    english_dictionary._open()
    assert not english_dictionary._already_created()
    english_dictionary._create_dictionary()
    assert english_dictionary._already_created()
    english_dictionary._close()


def test_delete_language(loaded_dictionary_temp_dir):
    """Test delete a language also removes its words."""
    language_to_remove = "german"
    Dictionary.remove_language(language_to_remove, _database_path=loaded_dictionary_temp_dir)
    # Check all words from removed language have been removed too.
    not_existing_dictionary = Dictionary(language_to_remove, loaded_dictionary_temp_dir)
    not_existing_dictionary._open()
    assert all(not not_existing_dictionary.word_exists(word, _testing=True)
               for word in MICRO_DICTIONARIES[language_to_remove])
    not_existing_dictionary._close()

#
# # TODO: Write test for populate method.
# def test_populate_language(temporary_english_text_file):
#     for line in temporary_english_text_file.readlines():
#         words =
