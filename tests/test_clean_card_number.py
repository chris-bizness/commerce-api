import pytest
import string
from common.algorithms import clean_card_number, COMMON_SEPARATORS


def test_requires_string_input():
    '''
    Don't allow integer inputs because leading zeroes could get lost
    '''
    with pytest.raises(TypeError):
        clean_card_number(None)

    with pytest.raises(TypeError):
        clean_card_number(4444444444444448)

    with pytest.raises(TypeError):
        clean_card_number(["4444444444444448"])

    with pytest.raises(TypeError):
        clean_card_number(tuple(["4"] * 15 + ["8"]))


def test_strips_all_COMMON_SEPARATORS():
    '''
    Having separators between short groups of digits in a card number makes it
    easier to read and is commonly found in raw user input
    '''
    expected = "0000000000000000"
    for i in COMMON_SEPARATORS:
        # Try a lot of different patterns to make sure there aren't predefined
        # patterns allowed
        spaced_numbers = f"0000{i}0000{i}0000{i}0000"
        actual = clean_card_number(spaced_numbers)
        assert actual == expected

        spaced_numbers = f"{i}0000{i}0000{i}0000{i}0000{i}"
        actual = clean_card_number(spaced_numbers)
        assert actual == expected

        spaced_numbers = f"000{i}000{i}000{i}000{i}000{i}0"
        actual = clean_card_number(spaced_numbers)
        assert actual == expected

        spaced_numbers = i.join(expected)
        actual = clean_card_number(spaced_numbers)
        assert actual == expected

    all_separators = ''.join(COMMON_SEPARATORS)
    spaced_numbers = all_separators.join(expected)
    actual = clean_card_number(spaced_numbers)
    assert actual == expected


def test_requires_all_digits():
    '''
    We want some validation that what was passed can be a valid card number
    Otherwise we have to bake that validation into all the other methods
    '''
    allowed_characters = ''.join(COMMON_SEPARATORS) + string.digits
    for idx in range(256):
        char = chr(idx)
        test = f"0000 0000 00{char}0 0000"

        if char in allowed_characters:
            clean_card_number(test)     # should not raise Exception
        else:
            with pytest.raises(ValueError):
                clean_card_number(test)
