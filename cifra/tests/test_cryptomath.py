import pytest

from cifra.cipher.cryptomath import gcd, find_mod_inverse


@pytest.mark.quick_test
def test_gcd():
    recovered_gcd = gcd(24, 32)
    assert recovered_gcd == 8


@pytest.mark.quick_test
def test_find_mod_inverse():
    recovered_mod_inverse = find_mod_inverse(7, 26)
    assert recovered_mod_inverse == 15
