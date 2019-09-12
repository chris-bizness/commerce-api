"""
    Test luhn_check
"""
import pytest
import string
from common.algorithms import luhn_check


def test_requires_string_input():
    with pytest.raises(TypeError):
        luhn_check(4111111111111111)

    with pytest.raises(TypeError):
        luhn_check(None)


def test_requires_digit_input():
    with pytest.raises(ValueError):
        luhn_check("ff0000")

    with pytest.raises(ValueError):
        luhn_check("four five")

    with pytest.raises(ValueError):
        luhn_check("")

    with pytest.raises(ValueError):
        luhn_check("----")


def test_strips_filler_characters():
    assert luhn_check(" 4111 1111 1111 1111 ") is True
    assert luhn_check("4111-1111-1111-1111") is True
    assert luhn_check("4111.1111.1111.1111") is True
    assert luhn_check("4111|1111|1111|1111") is True
    assert luhn_check("4111:1111:1111:1111") is True
    assert luhn_check(".-: 4111 | 1111 | 1111 | 1111 :-.") is True

    assert luhn_check("4111 1111 1111 1114") is False


def test_passes_common_fakes():
    assert luhn_check("4111111111111111") is True
    assert luhn_check("4444444444444448") is True


def test_fails_with_incorrect_check_digit():
    assert luhn_check("4111111111111110") is False
    assert luhn_check("4111111111111112") is False
    assert luhn_check("4111111111111113") is False
    assert luhn_check("4111111111111114") is False
    assert luhn_check("4111111111111115") is False
    assert luhn_check("4111111111111116") is False
    assert luhn_check("4111111111111117") is False
    assert luhn_check("4111111111111118") is False
    assert luhn_check("4111111111111119") is False

    assert luhn_check("4444444444444440") is False
    assert luhn_check("4444444444444441") is False
    assert luhn_check("4444444444444442") is False
    assert luhn_check("4444444444444443") is False
    assert luhn_check("4444444444444444") is False
    assert luhn_check("4444444444444445") is False
    assert luhn_check("4444444444444446") is False
    assert luhn_check("4444444444444447") is False
    assert luhn_check("4444444444444449") is False


def test_passes_with_generated_card_numbers():
    # cards generated from http://www.getcreditcardnumbers.com/
    card_numbers = [
        # Visa
        "4393638352371292",
        "4061357847532811",
        "4929788549317527",

        # Am Ex
        "373941476764901",
        "344132697731657",
        "345959434906872",

        # Master Card
        "5555555555554444",
        "5278728158565051",
        "5530905498002995",

        # Discover
        "6011111111111117",
        "6011058150190850",
        "6011590615964099",
    ]
    for card_num in card_numbers:
        assert luhn_check(card_num) is True

        for digit in string.digits:
            if digit != card_num[-1:]:
                # assert every other value for the check digit fails
                assert luhn_check(f"{card_num[:-1]}{digit}") is False
