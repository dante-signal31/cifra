import pytest
import cifra.cifra_laucher as cifra_launcher

from typing import Dict


def _assert_dict_key(key: str, value: str, _dict: Dict[str, str]):
    assert key in _dict.keys()
    assert _dict[key] == value


@pytest.mark.quick_test
def test_launcher_create_dictionary():
    provided_args = "dictionary create klingon".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "dictionary")
    _assert("action", "create")
    _assert("dictionary_name", "klingon")


@pytest.mark.quick_test
def test_launcher_create_dictionary_with_initial_file():
    provided_args = "dictionary create klingon --initial_words_file klingon_novel.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "dictionary")
    _assert("action", "create")
    _assert("dictionary_name", "klingon")
    _assert("initial_words_file", "klingon_novel.txt")


@pytest.mark.quick_test
def test_launcher_delete_dictionary():
    provided_args = "dictionary delete klingon".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "dictionary")
    _assert("action", "delete")
    _assert("dictionary_name", "klingon")


@pytest.mark.quick_test
def test_launcher_update_dictionary():
    provided_args = "dictionary update klingon klingon_novel.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "dictionary")
    _assert("action", "update")
    _assert("dictionary_name", "klingon")
    _assert("words_file", "klingon_novel.txt")


@pytest.mark.quick_test
def test_launcher_cipher_caesar():
    provided_args = "cipher caesar 3 message.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "cipher")
    _assert("algorithm", "caesar")
    _assert("key", "3")
    _assert("file_to_cipher", "message.txt")
    assert "ciphered_file" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_cipher_caesar_with_output_file():
    provided_args = "cipher caesar 3 message.txt --ciphered_file ciphered_message.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "cipher")
    _assert("algorithm", "caesar")
    _assert("key", "3")
    _assert("file_to_cipher", "message.txt")
    _assert("ciphered_file", "ciphered_message.txt")


@pytest.mark.quick_test
def test_launcher_incorrect_cipher_algorithm():
    provided_args = "cipher augustus 3 message.txt --ciphered_file ciphered_message.txt".split()
    with pytest.raises(Exception):
        _: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)


@pytest.mark.quick_test
def test_launcher_decipher_caesar():
    provided_args = "decipher caesar 3 ciphered_message.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "decipher")
    _assert("algorithm", "caesar")
    _assert("key", "3")
    _assert("file_to_decipher", "ciphered_message.txt")
    assert "deciphered_file" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_decipher_caesar_with_output_file():
    provided_args = "decipher caesar 3 ciphered_message.txt -deciphered_file deciphered_message.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "cipher")
    _assert("algorithm", "caesar")
    _assert("key", "3")
    _assert("file_to_cipher", "ciphered_message.txt")
    _assert("deciphered_file", "deciphered_message.txt")


@pytest.mark.quick_test
def test_launcher_incorrect_decipher_algorithm():
    provided_args = "decipher augustus 3 ciphered_message.txt --deciphered_file deciphered_message.txt".split()
    with pytest.raises(Exception):
        _: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)


@pytest.mark.quick_test
def test_launcher_attack_caesar():
    provided_args = "attack caesar ciphered_message.txt --deciphered_file recovered_message.txt".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "attack")
    _assert("algorithm", "caesar")
    _assert("file_to_attack", "ciphered_message.txt")
    _assert("deciphered_file", "recovered_message.txt")
    assert "charset" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_attack_caesar_with_charset():
    provided_args = "attack caesar ciphered_message.txt --deciphered_file recovered_message.txt " \
                    "--charset abcdefghijklmnñopqrstuvwxyz".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "attack")
    _assert("algorithm", "caesar")
    _assert("file_to_attack", "ciphered_message.txt")
    _assert("deciphered_file", "recovered_message.txt")
    assert "charset" not in parsed_arguments.keys()

