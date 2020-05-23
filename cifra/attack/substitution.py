"""Module to attack substitution cipher texts.

This module uses a word patter matching method to guess probable key used to cipher
a text using substitution algorithm.

You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from typing import Optional, Dict, Set, List
from cifra.attack.dictionaries import get_words_from_text, get_word_pattern, Dictionary
from cifra.cipher.common import DEFAULT_CHARSET


def hack_substitution(ciphered_text: str, charset: str = DEFAULT_CHARSET, _database_path: Optional[str] = None) -> str:
    """ Get substitution ciphered text key.

    Uses a word pattern matching technique to identify used language.

    **You should not use this function. Use *hack_substitution_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for substitution method. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: Substitution key found.
    """
    ciphered_words = get_words_from_text(ciphered_text)
    available_languages = Dictionary.get_dictionaries_names(_database_path=_database_path)
    cipherletter_mappings = dict()
    for language in available_languages:
        with Dictionary.open(language, False, _database_path=_database_path) as dictionary:
            cipherletter_mappings[language] = _init_mapping(charset)
            for ciphered_word in ciphered_words:
                word_mapping = _init_mapping(charset)
                ciphered_word_pattern = get_word_pattern(ciphered_word)
                word_candidates = dictionary.get_words_with_pattern(ciphered_word_pattern)
                for index, char in enumerate(ciphered_word):
                    for word_candidate in word_candidates:
                        word_mapping[char].add(word_candidate[index])
                for key in cipherletter_mappings[language].keys():
                    cipherletter_mappings[language][key] &= word_mapping[key]


def _init_mapping(charset: str = DEFAULT_CHARSET) -> Dict[str, Set[str]]:
    """ Create mapping for cipher letters

    :param text: Ciphered text to extract letters from.
    :return: A dict whose keys are letters and values are sets with subtitution
        letter candidates.
    """
    returned_dict = dict()
    for char in charset:
        returned_dict[char] = set()
    return returned_dict


def _get_possible_mappings(mapping: Dict[str, Set[str]]) -> List[Dict[str, Set[str]]]:
    """ Return every possible mapping from an unresolved mapping.

    An unresolved mapping is one that has more than one possibility in any of
    its chars.

    :param mapping: A character mapping.
    :return: A list of mapping candidates.
    """
    try:
        char, candidates = mapping.popitem()
    except KeyError:
        return [dict(), ]
    else:
        mapping_to_return = []
        partial_mappings = _get_possible_mappings(mapping)
        for candidate in candidates:
            for partial_mapping in partial_mappings:
                current_mapping = {char: {candidate}}
                current_mapping.update(partial_mapping)
                mapping_to_return.append(current_mapping)
        return mapping_to_return

