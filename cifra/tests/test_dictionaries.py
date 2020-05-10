"""
Tests for attack.dictionaries module.
"""
import os
import dataclasses
import pytest
import tempfile
from typing import List

from test_common.fs.ops import copy_files
from test_common.fs.temp import temp_dir

from cifra.attack.dictionaries import Dictionary, get_words_from_text, \
    NotExistingLanguage, get_words_from_text_file, identify_language, \
    IdentifiedLanguage, get_word_pattern

MICRO_DICTIONARIES = {
    "english": ["yes", "no", "dog", "cat"],
    "spanish": ["si", "no", "perro", "gato"],
    "french": ["qui", "non", "chien", "chat"],
    "german": ["ja", "nein", "hund", "katze"]
}

TEXT_FILE_NAME = "text_to_load.txt"

ENGLISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS = """This eBook is for the use of anyone anywhere at no cost and with
almost no restrictions whatsoever You may copy it give it away or
re use it under the terms of the Project Gutenberg License included
with this eBook or online at"""

ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS = """This eBook is for the use of anyone anywhere at no cost and with
almost no restrictions whatsoever.You may copy it, give it away or
re-use it under the terms of the Project Gutenberg License included
with this eBook or online at 2020"""

SPANISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS = """Todavía lo recuerdo como si aquello hubiera sucedido ayer llegó á las
puertas de la posada estudiando su aspecto afanosa y atentamente
seguido por su maleta que alguien conducía tras él en una carretilla de
mano Era un hombre alto fuerte pesado con un moreno pronunciado
color de avellana Su trenza ó coleta alquitranada le caía sobre los
hombros de su nada limpia blusa marina Sus manos callosas destrozadas
y llenas de cicatrices enseñaban las extremidades de unas uñas rotas y
negruzcas Y su rostro moreno llevaba en una mejilla aquella gran
cicatriz de sable sucia y de un color blanquizco lívido y repugnante
Todavía lo recuerdo paseando su mirada investigadora en torno del
cobertizo silbando mientras examinaba y prorrumpiendo en seguida en
aquella antigua canción marina que tan á menudo le oí cantar después"""

SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS = """Todavía lo recuerdo como si aquello hubiera sucedido ayer: llegó á las
puertas de la posada estudiando su aspecto, afanosa y atentamente,
seguido por su maleta que alguien conducía tras él en una carretilla de
mano. Era un hombre alto, fuerte, pesado, con un moreno pronunciado,
color de avellana. Su trenza ó coleta alquitranada le caía sobre los
hombros de su nada limpia blusa marina. Sus manos callosas, destrozadas
y llenas de cicatrices enseñaban las extremidades de unas uñas rotas y
negruzcas. Y su rostro moreno llevaba en una mejilla aquella gran
cicatriz de sable, sucia y de un color blanquizco, lívido y repugnante.
Todavía lo recuerdo, paseando su mirada investigadora en torno del
cobertizo, silbando mientras examinaba y prorrumpiendo, en seguida, en
aquella antigua canción marina que tan á menudo le oí cantar después:"""

FRENCH_TEXT_WITHOUT_PUNCTUATIONS_MARKS = """Combien le lecteur tandis que commodément assis au coin de son feu
il s amuse à feuilleter les pages d un roman combien il se rend peu
compte des fatigues et des angoisses de l auteur Combien il néglige de
se représenter les longues nuits de luttes contre des phrases rétives
les séances de recherches dans les bibliothèques les correspondances
avec d érudits et illisibles professeurs allemands en un mot tout
l énorme échafaudage que l auteur a édifié et puis démoli simplement
pour lui procurer à lui lecteur quelques instants de distraction au
coin de son feu ou encore pour lui tempérer l ennui d une heure en
wagon"""

FRENCH_TEXT_WITH_PUNCTUATIONS_MARKS = """Combien le lecteur,--tandis que, commodément assis au coin de son feu,
il s'amuse à feuilleter les pages d'un roman,--combien il se rend peu
compte des fatigues et des angoisses de l'auteur! Combien il néglige de
se représenter les longues nuits de luttes contre des phrases rétives,
les séances de recherches dans les bibliothèques, les correspondances
avec d'érudits et illisibles professeurs allemands, en un mot tout
l'énorme échafaudage que l'auteur a édifié et puis démoli, simplement
pour lui procurer, à lui, lecteur, quelques instants de distraction au
coin de son feu, ou encore pour lui tempérer l'ennui d'une heure en
wagon!"""

GERMAN_TEXT_WITHOUT_PUNCTUATIONS_MARKS = """Da unser Gutsherr Mr Trelawney Dr Livesay und die übrigen Herren
mich baten alle Einzelheiten über die Schatzinsel von Anfang bis zu
Ende aufzuschreiben und nichts auszulassen als die Lage der Insel und
auch die nur weil noch ungehobene Schätze dort liegen nehme ich im
Jahre die Feder zur Hand und beginne bei der Zeit als mein Vater
noch den Gasthof Zum Admiral Benbow hielt und jener dunkle alte
Seemann mit dem Säbelhieb über der Wange unter unserem Dache Wohnung
nahm"""

GERMAN_TEXT_WITH_PUNCTUATIONS_MARKS = """Da unser Gutsherr, Mr. Trelawney, Dr. Livesay und die übrigen Herren
mich baten, alle Einzelheiten über die Schatzinsel von Anfang bis zu
Ende aufzuschreiben und nichts auszulassen als die Lage der Insel, und
auch die nur, weil noch ungehobene Schätze dort liegen, nehme ich im
Jahre 17.. die Feder zur Hand und beginne bei der Zeit, als mein Vater
noch den Gasthof „Zum Admiral Benbow“ hielt und jener dunkle, alte
Seemann mit dem Säbelhieb über der Wange unter unserem Dache Wohnung
nahm."""

LANGUAGES = ["english", "spanish", "french", "german"]


@dataclasses.dataclass
class LoadedDictionaries:
    """Class with info to use a temporary dictionaries database."""
    temp_dir: str
    languages: List[str]


@pytest.fixture(scope="session")
def loaded_dictionaries() -> LoadedDictionaries:
    """Create a dictionaries database at a temp dir filled with four languages.

    Languages in database are: english, spanish, french and german.

    :return: Yields a LoadedDictionary fill info of temporal dictionaries database.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        resources_path = os.path.join(temp_dir, "resources")
        os.mkdir(resources_path)
        copy_files([f"cifra/tests/resources/{language}_book.txt" for language in LANGUAGES], resources_path)
        for language in LANGUAGES:
            with Dictionary.open(language=language, create=True, _database_path=temp_dir) as dictionary:
                language_book = os.path.join(temp_dir, f"resources/{language}_book.txt")
                dictionary.populate(language_book)
        yield LoadedDictionaries(temp_dir=temp_dir, languages=LANGUAGES)


@pytest.fixture()
def loaded_dictionary_temp_dir(temp_dir):
    """Create a dictionary at a temp dir filled with only a handful of words.

    :return: Yields created temp_dir to host temporal dictionary database.
    """
    # Load test data.
    for language, words in MICRO_DICTIONARIES.items():
        with Dictionary.open(language, create=True, _database_path=temp_dir) as language_dictionary:
            _ = [language_dictionary.add_word(word) for word in words]
    # Check all words are stored at database:
    for language, words in MICRO_DICTIONARIES.items():
        with Dictionary.open(language, _database_path=temp_dir) as language_dictionary:
            assert all(language_dictionary.word_exists(word) for word in words)
    yield temp_dir


@pytest.fixture(params=[(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS, ENGLISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS, "english"),
                        (SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS, SPANISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS, "spanish"),
                        (FRENCH_TEXT_WITH_PUNCTUATIONS_MARKS, FRENCH_TEXT_WITHOUT_PUNCTUATIONS_MARKS, "french"),
                        (GERMAN_TEXT_WITH_PUNCTUATIONS_MARKS, GERMAN_TEXT_WITHOUT_PUNCTUATIONS_MARKS, "german")],
                ids=["english", "spanish", "french", "german"])
def temporary_text_file(temp_dir, request):
    temporary_text_file_pathname = os.path.join(temp_dir, TEXT_FILE_NAME)
    with open(temporary_text_file_pathname, "w") as text_file:
        text_file.write(request.param[0])
        text_file.flush()
        yield text_file, request.param[1], request.param[2], temp_dir


@pytest.mark.quick_test
def test_open_not_existing_dictionary(temp_dir):
    with pytest.raises(NotExistingLanguage):
        with Dictionary.open("english", _database_path=temp_dir) as _:
            pass


@pytest.mark.quick_test
def test_open_existing_dictionary(temp_dir):
    # Create not existing language.
    with Dictionary.open("english", create=True, _database_path=temp_dir) as _:
        pass
    # Open newly created language
    with Dictionary.open("english", _database_path=temp_dir) as english_dictionary:
        assert english_dictionary._already_created()


@pytest.mark.quick_test
def test_cwd_word(temp_dir):
    """Test if we can check for word existence, write a new word and finally delete it."""
    word = "test"
    with Dictionary.open("english", create=True, _database_path=temp_dir) as english_dictionary:
        assert not english_dictionary.word_exists(word)
        english_dictionary.add_word(word)
        assert english_dictionary.word_exists(word)
        english_dictionary.remove_word(word)
        assert not english_dictionary.word_exists(word)


@pytest.mark.quick_test
def test_store_word_pattern(temp_dir):
    """Test word pattern is properly stored at database."""
    word = "classification"
    with Dictionary.open("test", create=True, _database_path=temp_dir) as test_dictionary:
        assert not test_dictionary.word_exists(word)
        test_dictionary.add_word(word)
        assert test_dictionary.word_exists(word)
        words = test_dictionary.get_words_with_pattern("0.1.2.3.3.4.5.4.0.2.6.4.7.8")
        assert word in words



@pytest.mark.quick_test
def test_create_language(temp_dir):
    """Test a new language creation at database."""
    english_dictionary = Dictionary("english", database_path=temp_dir)
    english_dictionary._open()
    assert not english_dictionary._already_created()
    english_dictionary._create_dictionary()
    assert english_dictionary._already_created()
    english_dictionary._close()


@pytest.mark.quick_test
def test_delete_language(loaded_dictionary_temp_dir):
    """Test delete a language also removes its words."""
    language_to_remove = "german"
    Dictionary.remove_dictionary(language_to_remove, _database_path=loaded_dictionary_temp_dir)
    # Check all words from removed language have been removed too.
    not_existing_dictionary = Dictionary(language_to_remove, loaded_dictionary_temp_dir)
    not_existing_dictionary._open()
    assert all(not not_existing_dictionary.word_exists(word, _testing=True)
               for word in MICRO_DICTIONARIES[language_to_remove])
    not_existing_dictionary._close()


@pytest.mark.quick_test
def test_get_words_from_text_file(temporary_text_file):
    text_file = temporary_text_file[0].name
    text_without_punctuation_marks = temporary_text_file[1]
    expected_set = set(text_without_punctuation_marks.lower().split())
    returned_set = get_words_from_text_file(text_file)
    assert expected_set == returned_set


@pytest.mark.quick_test
def test_populate_words_from_text_files(temporary_text_file):
    text_file = temporary_text_file[0].name
    text_without_punctuation_marks = temporary_text_file[1]
    current_language = temporary_text_file[2]
    temp_dir = temporary_text_file[3]
    expected_set = set(text_without_punctuation_marks.lower().split())
    with Dictionary.open(current_language, create=True, _database_path=temp_dir) as current_dictionary:
        current_dictionary.populate(text_file)
    with Dictionary.open(current_language, _database_path=temp_dir) as current_dictionary:
        for word in expected_set:
            assert current_dictionary.word_exists(word)


@pytest.mark.quick_test
@pytest.mark.parametrize("text_with_punctuation_marks,text_without_punctuation_marks",
                         [(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS, ENGLISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS),
                          (SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS, SPANISH_TEXT_WITHOUT_PUNCTUATIONS_MARKS),
                          (FRENCH_TEXT_WITH_PUNCTUATIONS_MARKS, FRENCH_TEXT_WITHOUT_PUNCTUATIONS_MARKS),
                          (GERMAN_TEXT_WITH_PUNCTUATIONS_MARKS, GERMAN_TEXT_WITHOUT_PUNCTUATIONS_MARKS)],
                         ids=["english", "spanish", "french", "german"])
def test_get_words_from_text(text_with_punctuation_marks: str, text_without_punctuation_marks: str):
    expected_set = set(text_without_punctuation_marks.lower().split())
    returned_set = get_words_from_text(text_with_punctuation_marks)
    assert expected_set == returned_set


@pytest.mark.slow_test
def test_get_dictionaries_names(loaded_dictionaries: LoadedDictionaries):
    dictionaries_names = Dictionary.get_dictionaries_names(_database_path=loaded_dictionaries.temp_dir)
    assert dictionaries_names == loaded_dictionaries.languages


@pytest.mark.quick_test
def test_get_word_pattern():
    word = "HGHHU"
    expected_word_pattern = "0.1.0.0.2"
    word_pattern = get_word_pattern(word)
    assert expected_word_pattern == word_pattern


@pytest.mark.quick_test
def test_add_multiple_words(temp_dir):
    language = "english"
    with Dictionary.open(language, create=True, _database_path=temp_dir) as dictionary:
        assert all(not dictionary.word_exists(word) for word in MICRO_DICTIONARIES[language])
        dictionary.add_multiple_words(MICRO_DICTIONARIES[language])
        assert all(dictionary.word_exists(word) for word in MICRO_DICTIONARIES[language])


@pytest.mark.slow_test
@pytest.mark.parametrize("text,language",
                         [(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS, "english"),
                          (SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS, "spanish")],
                         ids=["english", "spanish"])
def test_identify_language(loaded_dictionaries: LoadedDictionaries, text: str, language: str):
    identified_language = identify_language(text, loaded_dictionaries.temp_dir)
    assert identified_language.winner == language
    assert identified_language.winner_probability == 1.0
