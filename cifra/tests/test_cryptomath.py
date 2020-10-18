import pytest

from cifra.cipher.cryptomath import gcd, find_mod_inverse, find_factors, \
    find_common_factors


@pytest.mark.quick_test
def test_gcd():
    recovered_gcd = gcd(24, 32)
    assert recovered_gcd == 8


@pytest.mark.quick_test
def test_find_mod_inverse():
    recovered_mod_inverse = find_mod_inverse(7, 26)
    assert recovered_mod_inverse == 15

@pytest.mark.quick_test
def test_find_factors():
    expected_results = {
        8: [2, 4, 8],
        24: [2, 3, 4, 6, 8, 12, 24],
        32: [2, 4, 8, 16, 32],
        48: [2, 3, 4, 6, 8, 12, 16, 24, 48]
    }
    for number_to_test in expected_results:
        returned_factors = find_factors(number_to_test)
        assert returned_factors == expected_results[number_to_test]


@pytest.mark.quick_test
def test_find_common_factors():
    factors_to_test = {
        8: [2, 4, 8],
        24: [2, 3, 4, 6, 8, 12, 24],
        32: [2, 4, 8, 16, 32],
        48: [2, 3, 4, 6, 8, 12, 16, 24, 48]
    }
    expected_result = {2, 4, 8}
    returned_factors = find_common_factors(*(factor_list for factor_list in factors_to_test.values()))
    assert returned_factors == expected_result
