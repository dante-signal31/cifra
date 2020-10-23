"""Module to attack Vigenere cipher texts.
This module uses two approaches: a dictionary brute force method to guess probable word key used to cipher
a text using Vigenere algorithm and a frequency analysis attack.
You should be aware that to be successful charset used for attack should be the
same used to cipher. Besides, this module tries to guess if deciphered text is
the good one comparing it with words from a language dictionary. If original
message was in a language you don't have a dictionary for, then correct key
won't be detected.
"""
from itertools import chain, permutations
from typing import Optional, Iterator, List, Set, Union, Generator
from cifra.attack.simple_attacks import _assess_key
from cifra.attack.simple_attacks import _brute_force as simple_brute_force
from cifra.attack.simple_attacks import _brute_force_mp as simple_brute_force_mp
from cifra.attack.simple_attacks import _dictionary_word_key_generator as dictionary_word_key_generator
from cifra.attack.dictionaries import IdentifiedLanguage, Dictionary
from cifra.attack.frequency import get_substrings, find_most_likely_subkeys, find_repeated_sequences
from cifra.attack.substitution import Mapping
from cifra.cipher.cryptomath import find_factors, count_factors
from cifra.cipher.vigenere import DEFAULT_CHARSET, decipher
from cifra.tests.test_simple_attacks import mocked_dictionary_word_key_generator


def brute_force(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                _database_path: Optional[str] = None,
                _testing=False) -> str:
    """ Get Vigenere ciphered text key.
    Uses a brute force technique trying the entire dictionary space until finding a text
    that can be identified with any of our languages.
    **You should not use this function. Use *brute_force_mp* instead.** This
    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.
    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = dictionary_word_key_generator(_database_path) if not _testing else mocked_dictionary_word_key_generator()
    return simple_brute_force(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              # key_space_length=key_space_length,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def brute_force_mp(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                   _database_path: Optional[str] = None,
                   _testing=False) -> str:
    """ Get Vigenere ciphered text key.

    Uses a brute force technique trying the entire dictionary space until finding a text
    that can be identified with any of our languages.

    **You should use this function instead of *brute_force*.**

    Whereas *brute_force* uses a sequential approach, this function uses
    multiprocessing to improve performance.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = dictionary_word_key_generator(_database_path) if not _testing else mocked_dictionary_word_key_generator()
    return simple_brute_force_mp(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def _analize_text(nargs):
    ciphered_text, key, charset, _database_path = nargs
    return _assess_vigenere_key(ciphered_text, key, charset, _database_path)


def _assess_vigenere_key(ciphered_text: str, key: int, charset: str,
                       _database_path: Optional[str] = None) -> (int, IdentifiedLanguage):
    """Decipher text with given key and try to find out if returned text can be identified with any
    language in our dictionaries.

    :param ciphered_text: Text to be deciphered.
    :param key: Key to decipher *ciphered_text*.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
     and deciphering, should use the same charset or original text won't be properly
     recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
     set this parameter, but it is useful for tests.
    :return: A tuple with used key and an *IdentifiedLanguage* object with assessment result.
    """
    return _assess_key(decipher, ciphered_text=ciphered_text, key=key, charset=charset, _database_path=_database_path)


def statistical_brute_force(ciphered_text: str, charset: str = DEFAULT_CHARSET,
                maximum_key_length: int = 5,
                _database_path: Optional[str] = None,
                # _testing=False
                            ) -> str:
    """ Get Vigenere ciphered text key.

    Uses a statistical brute force technique (Kasiski analysis) trying the most
    likely keys until finding a text that can be identified with any of our languages.

    **You should not use this function. Use *brute_force_mp* instead.** This

    function is slower than *mp* one because is sequential while the other uses a
    multiprocessing approach. This function only stay here to allow comparisons
    between sequential and multiprocessing approaches.

    :param ciphered_text: Text to be deciphered.
    :param charset: Charset used for Caesar method substitution. Both ends, ciphering
        and deciphering, should use the same charset or original text won't be properly
        recovered.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :param _testing: Vigenere takes to long time to be tested against real dictionaries. So,
        to keep tests short if _testing is set to True a mocked key generator is used so only
        a controlled handful of words are tested to find a valid key. In simple terms: don't
        mess with this parameter and keep it to False, it is only used for testing.
    :return: Most probable Vigenere key found.
    """
    key_generator_function = frequency_key_generator(ciphered_text,
                                                     maximum_key_length,
                                                     _database_path)
    return simple_brute_force(key_generator=key_generator_function,
                              assess_function=_assess_vigenere_key,
                              ciphered_text=ciphered_text,
                              charset=charset,
                              _database_path=_database_path)


def frequency_key_generator(ciphered_text: str,
                            maximum_key_length: int = 5,
                            _database_path: Optional[str] = None) -> Iterator[str]:
    """ Assess statistically given ciphertext to return most likely keys.

    :param ciphered_text: Text to be deciphered.
    :param maximum_key_length: Give keys up to given maximum key length.
    :param _database_path: Absolute pathname to database file. Usually you don't
        set this parameter, but it is useful for tests.
    :return: An iterator through most likely keys below given length.
    """
    likely_key_lengths = _get_likely_key_lengths(ciphered_text, maximum_key_length)
    keys_to_try: List[str] = []
    for language in Dictionary.get_available_languages(_database_path):
        with Dictionary.open(language, False, _database_path) as language_dictionary:
            for key_length in likely_key_lengths:
                substrings = get_substrings(ciphered_text, key_length)
                likely_keys = _get_likely_keys(substrings, language_dictionary)
                keys_to_try.extend(likely_keys)
    for key in keys_to_try:
        yield key


def _get_likely_key_lengths(ciphered_text: str, maximum_key_length: int) -> List[int]:
    """ Get most likely key lengths using Kasiski examination.

    :param ciphered_text: Text to be decrypted.
    :param maximum_key_length: We are not interested in keys longer than this limit.
    :return: A list with most likely lengths shorter than maximum_key_length.
    """
    sequences = find_repeated_sequences(ciphered_text)
    factors = (find_factors(separation) for separation_list in sequences.values() for separation in separation_list)
    factors_count = count_factors(*factors)
    likely_key_lengths = [key_length for key_length, _ in factors_count.most_common() if
                          key_length <= maximum_key_length]
    return likely_key_lengths


def _get_likely_keys(substrings: List[str], language_dictionary: Dictionary) -> List[str]:
    """ Get likely subkeys for given substrings.

    :param substrings: List of substrings extracted from current ciphered text.
    :param language_dictionary: Language to compare its histogram with.
    :return: List of likely keys to try.
    """
    likely_key_letters_bins = (find_most_likely_subkeys(substring,
                                                        language_dictionary.letter_histogram)
                               for substring in substrings)
    likely_keys = _get_key_letters_combinations(likely_key_letters_bins)
    return likely_keys


def _get_key_letters_combinations(likely_key_letters_bins: Union[List[List[str]], Iterator[List[str]]]) -> List[str]:
    """ Get every possible key from combinations of letter from every given bin.

    :param likely_key_letters_bins: Indexed list with likely list for every position in key (i.e. likely_key_letter_bins[0]
         is a list of likely letters to be at first position of key whereas likely_key_letter_bins[1] is a list with likely
         letters for second position of key).
    :return: A list with every possible key from combining letters from bins.
    """
    likely_keys = []
    # I'm going to use a Mapping just to get every possible combination
    # of characters.
    # We don't expect keys longer than DEFAULT_CHARSET length.
    likely_key_letters_mapping = Mapping(charset=DEFAULT_CHARSET)
    bins_dict = {f"{DEFAULT_CHARSET[i]}": set(letter_bin) for i, letter_bin in enumerate(likely_key_letters_bins)}
    likely_key_letters_mapping.load_content(bins_dict)
    likely_key_letters_combinations = likely_key_letters_mapping.get_possible_mappings()
    for combination in likely_key_letters_combinations:
        key_letters = [value.pop() for _, value in combination.items() if len(value) > 0]
        likely_keys.append("".join(key_letters))
    return likely_keys

