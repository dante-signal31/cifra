"""
Tests for cipher.substitution module.
"""
import pytest
import cipher.substitution as substitution

TEST_CHARSET = "abcdefghijklmnopqrstuvwxyz"
TEST_KEY =     "lfwoayuisvkmnxpbdcrjtqeghz"
ORIGINAL_MESSAGE = "If a man is offered a fact which goes against his " \
                   "instincts, he will scrutinize it closely, and unless " \
                   "the evidence is overwhelming, he will refuse to believe " \
                   "it. If, on the other hand, he is offered something which " \
                   "affords a reason for acting in accordance to his " \
                   "instincts, he will accept it even on the slightest " \
                   "evidence. The origin of myths is explained in this way. " \
                   "-Bertrand Russell"
CIPHERED_MESSAGE = "Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr " \
                   "sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr " \
                   "jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra " \
                   "jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr " \
                   "pyyacao rpnajisxu eiswi lyypcor l calrpx ypc " \
                   "lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm " \
                   "lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx " \
                   "py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm"



@pytest.mark.quick_test
def test_cipher():
    ciphered_text = substitution.cipher(ORIGINAL_MESSAGE, TEST_KEY, charset=TEST_CHARSET)
    assert ciphered_text == CIPHERED_MESSAGE


@pytest.mark.quick_test
def test_decipher():
    deciphered_text = substitution.decipher(CIPHERED_MESSAGE, TEST_KEY, charset=TEST_CHARSET)
    assert deciphered_text == ORIGINAL_MESSAGE


@pytest.mark.quick_test
def test_wrong_length_key_are_detected():
    TEST_CHARSET = "123"
    WRONG_KEY = "1234"
    with pytest.raises(substitution.WrongSubstitutionKey) as e:
        _ = substitution.cipher("", WRONG_KEY, TEST_CHARSET)
    assert e.value.get_cause()[0] == substitution.WrongSubstitutionKeyCauses.wrong_key_length


@pytest.mark.quick_test
def test_repeated_character_keys_are_detected():
    TEST_CHARSET = "123"
    WRONG_KEY = "122"
    with pytest.raises(substitution.WrongSubstitutionKey) as e:
        _ = substitution.cipher("", WRONG_KEY, TEST_CHARSET)
    assert e.value.get_cause()[0] == substitution.WrongSubstitutionKeyCauses.repeated_characters