"""
Tests for cipher.substitution module.
"""
import pytest

import cifra.attack.substitution as attack_substitution
import cifra.cipher.substitution as substitution
from cifra.tests.test_dictionaries import loaded_dictionaries, LoadedDictionaries
from cifra.tests.test_substitution import ORIGINAL_MESSAGE, CIPHERED_MESSAGE, \
    TEST_KEY, TEST_CHARSET

# TEST_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# ORIGINAL_MESSAGE = "If a man is offered a fact which goes against his " \
#                    "instincts, he will scrutinize it closely, and unless " \
#                    "the evidence is overwhelming, he will refuse to believe " \
#                    "it. If, on the other hand, he is offered something which " \
#                    "affords a reason for acting in accordance to his " \
#                    "instincts, he will accept it even on the slightest " \
#                    "evidence. The origin of myths is explained in this way. " \
#                    "-Bertrand Russell"
# CIPHERED_MESSAGE = "Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr " \
#                    "sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr " \
#                    "jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra " \
#                    "jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr " \
#                    "pyyacao rpnajisxu eiswi lyypcor l calrpx ypc " \
#                    "lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm " \
#                    "lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx " \
#                    "py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm"
# TEST_KEY = "LFWOAYUISVKMNXPBDCRJTQEGHZlfwoayuisvkmnxpbdcrjtqeghz"


@pytest.mark.slow_test
def test_hack_substitution(loaded_dictionaries: LoadedDictionaries):
    found_key = attack_substitution.hack_substitution(CIPHERED_MESSAGE,
                                                      TEST_CHARSET,
                                                      _database_path=loaded_dictionaries.temp_dir)
    assert TEST_KEY == found_key


@pytest.mark.quick_test
def test_init_mapping():
    expected_mapping = {'A': set(), 'B': set(), 'C': set(), 'D': set(), 'E': set(), 'F': set(), 'G': set(),
                        'H': set(), 'I': set(), 'J': set(), 'K': set(), 'L': set(), 'M': set(),
                        'N': set(), 'O': set(), 'P': set(), 'Q': set(), 'R': set(), 'S': set(), 'T': set(),
                        'U': set(), 'V': set(), 'W': set(), 'X': set(), 'Y': set(), 'Z': set(),
                        'a': set(), 'b': set(), 'c': set(), 'd': set(), 'e': set(), 'f': set(), 'g': set(),
                        'h': set(), 'i': set(), 'j': set(), 'k': set(), 'l': set(), 'm': set(),
                        'n': set(), 'o': set(), 'p': set(), 'q': set(), 'r': set(), 's': set(), 't': set(),
                        'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': set(), 'z': set(),
                        }
    recovered_mapping = attack_substitution._init_mapping(TEST_CHARSET)
    assert expected_mapping == recovered_mapping

@pytest.mark.quick_test
def test_get_possible_mappings():
    mapping = {"1": ["a", "b"],
               "2": ["c"],
               "3": ["d"],
               "4": ["e", "f"]}
    expected_list = [{"1": ["a"],
                      "2": ["c"],
                      "3": ["d"],
                      "4": ["e"]}, {"1": ["a"],
                                    "2": ["c"],
                                    "3": ["d"],
                                    "4": ["f"]}, {"1": ["b"],
                                                  "2": ["c"],
                                                  "3": ["d"],
                                                  "4": ["e"]}, {"1": ["b"],
                                                                "2": ["c"],
                                                                "3": ["d"],
                                                                "4": ["f"]}]
    recovered_mappings = attack_substitution._get_possible_mappings(mapping)
    assert all(_mapping in recovered_mappings for _mapping in expected_list) \
           and len(expected_list) == len(recovered_mappings)