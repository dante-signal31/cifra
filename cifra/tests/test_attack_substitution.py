"""
Tests for cipher.substitution module.
"""
import os
import pytest

import cifra.attack.substitution as attack_substitution
import cifra.cipher.substitution as substitution
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries
from cifra.tests.test_substitution import ORIGINAL_MESSAGE, CIPHERED_MESSAGE, \
    TEST_KEY, TEST_CHARSET


TEST_CHARSET_SPANISH = "abcdefghijklmnopqrstuvwxyzáéíóúñ"
TEST_KEY_SPANISH =     "lfwoayuisvkmnxpbdcrjtqeghzñúóíéá"

ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS = "resources/english_book_c1.txt"
SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS = "resources/spanish_book_c1.txt"


@pytest.mark.slow_test
@pytest.mark.parametrize("text_file,language, key, charset",
                         [(ENGLISH_TEXT_WITH_PUNCTUATIONS_MARKS, "english", TEST_KEY, TEST_CHARSET),
                          (SPANISH_TEXT_WITH_PUNCTUATIONS_MARKS, "spanish", TEST_KEY_SPANISH, TEST_CHARSET_SPANISH)],
                         ids=["english", "spanish"])
def test_hack_substitution(loaded_dictionaries: LoadedDictionaries, text_file: str, language: str, key: str, charset: str):
    text_file_pathname = os.path.join(os.getcwd(), "cifra", "tests", text_file)
    with open(text_file_pathname) as text_file:
        clear_text = text_file.read()
        ciphered_text = substitution.cipher(clear_text, key, charset)
    found_key = attack_substitution.hack_substitution(ciphered_text,
                                                      charset,
                                                      _database_path=loaded_dictionaries.temp_dir)
    assert key == found_key[0]


@pytest.mark.quick_test
def test_init_mapping():
    expected_mapping = {'a': set(), 'b': set(), 'c': set(), 'd': set(), 'e': set(), 'f': set(), 'g': set(),
                        'h': set(), 'i': set(), 'j': set(), 'k': set(), 'l': set(), 'm': set(),
                        'n': set(), 'o': set(), 'p': set(), 'q': set(), 'r': set(), 's': set(), 't': set(),
                        'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': set(), 'z': set(),
                        }
    recovered_mapping = attack_substitution.Mapping(TEST_CHARSET)
    assert recovered_mapping.get_current_content() == expected_mapping


@pytest.mark.quick_test
def test_mapping_equality():
    mapping_content = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f"},
                       "5": {"g", "h"}}
    mapping1 = attack_substitution.Mapping.new_mapping(mapping_content)
    mapping2 = attack_substitution.Mapping.new_mapping(mapping_content)
    assert mapping1 == mapping2


@pytest.mark.quick_test
def test_mapping_inequality():
    mapping_content = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f"},
                       "5": {"g", "h"}}
    mapping_content2 = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f"}}
    mapping1 = attack_substitution.Mapping.new_mapping(mapping_content)
    mapping2 = attack_substitution.Mapping.new_mapping(mapping_content2)
    assert mapping1 != mapping2


@pytest.mark.quick_test
def test_get_possible_mappings():
    mapping_content = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f"},
                       "5": {"g", "h"}}
    mapping = attack_substitution.Mapping()
    mapping.load_content(mapping_content)
    expected_list_content = [{"1": {"a"},
                              "2": {"c"},
                              "3": {"d"},
                              "4": {"e"},
                              "5": {"g"}}, {"1": {"a"},
                                            "2": {"c"},
                                            "3": {"d"},
                                            "4": {"f"},
                                            "5": {"g"}}, {"1": {"b"},
                                                          "2": {"c"},
                                                          "3": {"d"},
                                                          "4": {"e"},
                                                          "5": {"g"}}, {"1": {"b"},
                                                                        "2": {"c"},
                                                                        "3": {"d"},
                                                                        "4": {"f"},
                                                                        "5": {"g"}},
                             {"1": {"a"},
                              "2": {"c"},
                              "3": {"d"},
                              "4": {"e"},
                              "5": {"h"}}, {"1": {"a"},
                                            "2": {"c"},
                                            "3": {"d"},
                                            "4": {"f"},
                                            "5": {"h"}}, {"1": {"b"},
                                                          "2": {"c"},
                                                          "3": {"d"},
                                                          "4": {"e"},
                                                          "5": {"h"}}, {"1": {"b"},
                                                                        "2": {"c"},
                                                                        "3": {"d"},
                                                                        "4": {"f"},
                                                                        "5": {"h"}}]
    expected_list = [attack_substitution.Mapping() for _ in range(len(expected_list_content))]
    for index, _mapping in enumerate(expected_list):
        _mapping.load_content(expected_list_content[index])
    recovered_mappings = mapping.get_possible_mappings()
    assert len(expected_list) == len(recovered_mappings)
    assert all(_mapping in recovered_mappings for _mapping in expected_list)


@pytest.mark.quick_test
def test_get_possible_mappings_with_empties():
    mapping_content = {"1": {"a", "b"},
                       "1.5": set(),
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f"},
                       "5": {"g", "h"}}
    mapping = attack_substitution.Mapping()
    mapping.load_content(mapping_content)
    expected_list_content = [{"1": {"a"},
                              "1.5": set(),
                              "2": {"c"},
                              "3": {"d"},
                              "4": {"e"},
                              "5": {"g"}}, {"1": {"a"},
                                            "1.5": set(),
                                            "2": {"c"},
                                            "3": {"d"},
                                            "4": {"f"},
                                            "5": {"g"}}, {"1": {"b"},
                                                          "1.5": set(),
                                                          "2": {"c"},
                                                          "3": {"d"},
                                                          "4": {"e"},
                                                          "5": {"g"}}, {"1": {"b"},
                                                                        "1.5": set(),
                                                                        "2": {"c"},
                                                                        "3": {"d"},
                                                                        "4": {"f"},
                                                                        "5": {"g"}},
                             {"1": {"a"},
                              "1.5": set(),
                              "2": {"c"},
                              "3": {"d"},
                              "4": {"e"},
                              "5": {"h"}}, {"1": {"a"},
                                            "1.5": set(),
                                            "2": {"c"},
                                            "3": {"d"},
                                            "4": {"f"},
                                            "5": {"h"}}, {"1": {"b"},
                                                          "1.5": set(),
                                                          "2": {"c"},
                                                          "3": {"d"},
                                                          "4": {"e"},
                                                          "5": {"h"}}, {"1": {"b"},
                                                                        "1.5": set(),
                                                                        "2": {"c"},
                                                                        "3": {"d"},
                                                                        "4": {"f"},
                                                                        "5": {"h"}}]
    expected_list = [attack_substitution.Mapping() for _ in range(len(expected_list_content))]
    for index, _mapping in enumerate(expected_list):
        _mapping.load_content(expected_list_content[index])
    recovered_mappings = mapping.get_possible_mappings()
    assert len(expected_list) == len(recovered_mappings)
    assert all(_mapping in recovered_mappings for _mapping in expected_list)


@pytest.mark.quick_test
def test_reduce_mapping():
    mapping_content = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"e", "f", "g"},
                       "5": {"h"}}
    mapping_content_2 = {"1": {"a"},
                         "2": {"c"},
                         "4": {"e", "g"},
                         "5": {"h"}}
    expected_reduced_mapping = {"1": {"a"},
                                "2": {"c"},
                                "3": {"d"},
                                "4": {"e", "g"},
                                "5": {"h"}}
    mapping = attack_substitution.Mapping.new_mapping(mapping_content)
    mapping2 = attack_substitution.Mapping.new_mapping(mapping_content_2)
    expected_mapping = attack_substitution.Mapping.new_mapping(expected_reduced_mapping)
    mapping.reduce_mapping(mapping2)
    assert mapping.get_current_content() == expected_mapping.get_current_content()


@pytest.mark.quick_test
def test_generate_key_string():
    mapping_content = {"f": {"a"},
                       "g": {"b"},
                       "h": {"c"},
                       "i": {"d"},
                       "j": {"e"}}
    expected_keystring = "ABCDEFGHIJKLMNOPQRSTUVWXYZfghijfghijklmnopqrstuvwxyz"
    TEST_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    mapping = attack_substitution.Mapping.new_mapping(mapping_content, charset=TEST_CHARSET)
    returned_keystring = mapping.generate_key_string()
    assert returned_keystring == expected_keystring


@pytest.mark.quick_test
def test_get_used_charset():
    text = "aaabb cd eef g"
    expected_charset = set("abcdefg")
    returned_charset = attack_substitution._get_used_charset(text)
    assert returned_charset == expected_charset


@pytest.mark.quick_test
def test_clean_redundancies():
    mapping_content = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"d", "f"},
                       "5": {"c", "h"}}
    mapping_cleaned = {"1": {"a", "b"},
                       "2": {"c"},
                       "3": {"d"},
                       "4": {"f"},
                       "5": {"h"}}
    mapping = attack_substitution.Mapping.new_mapping(mapping_content, charset=TEST_CHARSET)
    expected_mapping = attack_substitution.Mapping.new_mapping(mapping_cleaned, charset=TEST_CHARSET)
    mapping.clean_redundancies()
    assert mapping.get_current_content() == expected_mapping.get_current_content()

