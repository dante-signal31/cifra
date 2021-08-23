import os
import tempfile

import pytest
import cifra.cifra_launcher as cifra_launcher

from typing import Dict


def _assert_dict_key(key: str, value: str, _dict: Dict[str, str]):
    assert key in _dict
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
    with tempfile.NamedTemporaryFile() as output_file:
        provided_args = f"dictionary create klingon --initial_words_file {output_file.name}".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "dictionary")
        _assert("action", "create")
        _assert("dictionary_name", "klingon")
        _assert("initial_words_file", f"{output_file.name}")


@pytest.mark.quick_test
def test_launcher_create_dictionary_with_not_existing_initial_file():
    with pytest.raises(BaseException):
        provided_args = "dictionary create klingon --initial_words_file klingon_novel.txt".split()
        _: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)


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
    with tempfile.NamedTemporaryFile() as words_file:
        provided_args = f"dictionary update klingon {words_file.name}".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "dictionary")
        _assert("action", "update")
        _assert("dictionary_name", "klingon")
        _assert("words_file", f"{words_file.name}")


@pytest.mark.quick_test
def test_launcher_cipher_caesar():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"cipher caesar 3 {message_file.name}".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "cipher")
        _assert("algorithm", "caesar")
        _assert("key", "3")
        _assert("file_to_cipher", f"{message_file.name}")
        assert "ciphered_file" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_cipher_caesar_with_output_file():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"cipher caesar 3 {message_file.name} --ciphered_file ciphered_message.txt".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "cipher")
        _assert("algorithm", "caesar")
        _assert("key", "3")
        _assert("file_to_cipher", f"{message_file.name}")
        _assert("ciphered_file", "ciphered_message.txt")


@pytest.mark.quick_test
def test_launcher_incorrect_cipher_algorithm():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"cipher augustus 3 {message_file.name} --ciphered_file ciphered_message.txt".split()
        with pytest.raises(BaseException):
            _: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)


@pytest.mark.quick_test
def test_launcher_decipher_caesar():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"decipher caesar 3 {message_file.name}".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "decipher")
        _assert("algorithm", "caesar")
        _assert("key", "3")
        _assert("file_to_decipher", f"{message_file.name}")
        assert "deciphered_file" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_decipher_caesar_with_output_file():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"decipher caesar 3 {message_file.name} --deciphered_file deciphered_message.txt".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "decipher")
        _assert("algorithm", "caesar")
        _assert("key", "3")
        _assert("file_to_decipher", f"{message_file.name}")
        _assert("deciphered_file", "deciphered_message.txt")


@pytest.mark.quick_test
def test_launcher_incorrect_decipher_algorithm():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"decipher augustus 3 {message_file.name} --deciphered_file deciphered_message.txt".split()
        with pytest.raises(BaseException):
            _: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)


@pytest.mark.quick_test
def test_launcher_attack_caesar():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"attack caesar {message_file.name} --deciphered_file recovered_message.txt".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "attack")
        _assert("algorithm", "caesar")
        _assert("file_to_attack", f"{message_file.name}")
        _assert("deciphered_file", "recovered_message.txt")
        assert "charset" not in parsed_arguments.keys()


@pytest.mark.quick_test
def test_launcher_attack_caesar_with_charset():
    with tempfile.NamedTemporaryFile() as message_file:
        provided_args = f"attack caesar {message_file.name} --deciphered_file recovered_message.txt " \
                        "--charset abcdefghijklmnñopqrstuvwxyz".split()
        parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
        def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
        _assert("mode", "attack")
        _assert("algorithm", "caesar")
        _assert("file_to_attack", f"{message_file.name}")
        _assert("deciphered_file", "recovered_message.txt")
        _assert("charset", "abcdefghijklmnñopqrstuvwxyz")


@pytest.mark.quick_test
def test_launcher_list_dictionaries():
    provided_args = "dictionary list".split()
    parsed_arguments: Dict[str, str] = cifra_launcher.parse_arguments(provided_args)
    def _assert(key, value): return _assert_dict_key(key, value, parsed_arguments)
    _assert("mode", "dictionary")
    _assert("action", "list")
