import re
import pytest
from unittest.mock import patch, MagicMock, call
from common.algorithms import generate_card_number, luhn_check
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)


def test_defaults_to_16_digits():
    '''
    16 digits is the most commonly-used payment card number length in the
    banking industry and is the most sane default
    '''
    number = generate_card_number()
    assert isinstance(number, str)
    assert len(number) == 16

    # Test AmEx prefix (usually 15 digits) - we don't want any hidden logic that
    # modifies the default length. This method should be straightforward
    number = generate_card_number('37')
    assert isinstance(number, str)
    assert len(number) == 16


def test_prefix_is_at_start_of_generated_number():
    '''
    The prefix determines the industry & the issuer - it's often required to
    test separate card issuers separately
    '''
    prefix = '3712'
    number = generate_card_number(prefix)
    assert number.startswith(prefix)

    prefix = '3712'
    number = generate_card_number(prefix, num_digits=8)
    assert number.startswith(prefix)

    prefix = '3712123'
    number = generate_card_number(prefix, num_digits=8)
    assert number.startswith(prefix)


def test_generates_exact_number_of_digits_given():
    number = generate_card_number(num_digits=MIN_LENGTH)
    assert isinstance(number, str)
    assert len(number) == MIN_LENGTH

    number = generate_card_number('37', num_digits=MAX_LENGTH)
    assert isinstance(number, str)
    assert len(number) == MAX_LENGTH

    number = generate_card_number('123456789', num_digits=10)
    assert isinstance(number, str)
    assert len(number) == 10

    number = generate_card_number('0' * 13, num_digits=13)
    assert isinstance(number, str)
    assert len(number) == 13


def test_cannot_generate_with_invalid_digit_count():
    '''
    This method should generate valid card numbers, so the length should adhere
    to the ISO standard
    '''
    with pytest.raises(ValueError):
        generate_card_number(num_digits=MIN_LENGTH-1)
    generate_card_number(num_digits=MIN_LENGTH)   # OK

    with pytest.raises(ValueError):
        generate_card_number(num_digits=MAX_LENGTH+1)
    generate_card_number(num_digits=MAX_LENGTH)   # OK


def test_fails_if_num_digits_less_than_prefix_length():
    '''
    If we want fewer digits than we pass in, it's not clear which end to remove
    digits from, so it should raise an exception so the bug can be caught early
    '''
    with pytest.raises(ValueError):
        generate_card_number('123456789', num_digits=8)

    with pytest.raises(ValueError):
        generate_card_number('12345678901234567')


def test_separators_in_the_prefix_do_not_effect_the_output():
    '''
    Separators should be stripped and not count into the # of digits desired
    '''
    number = generate_card_number("1 2 3 4 5 6", num_digits=14)
    assert bool(re.fullmatch(r"\d+", number))
    assert len(number) == 14

    number = generate_card_number("123-456", num_digits=18)
    assert bool(re.fullmatch(r"\d+", number))
    assert len(number) == 18

    number = generate_card_number("12. 34. 56.", num_digits=11)
    assert bool(re.fullmatch(r"\d+", number))
    assert len(number) == 11

    number = generate_card_number("12 | 34 | 56")
    assert bool(re.fullmatch(r"\d+", number))
    assert len(number) == 16


def test_if_num_digits_is_same_as_length_of_prefix_and_check_is_wrong_fails():
    '''
    This scenario is likely a typo, so raise an exception so the error can be
    caught early
    '''
    with pytest.raises(ValueError):
        generate_card_number('0' * 15 + '1')

    with pytest.raises(ValueError):
        generate_card_number('123456789', num_digits=9)

    with pytest.raises(ValueError):
        generate_card_number('1234567890', num_digits=10)


def test_if_num_digits_is_same_as_length_of_prefix_and_check_is_good_succeeds():
    ''' LGTM ¯\\_(ツ)_/¯ '''
    generate_card_number('4444 4444 4444 4448')     # OK
    generate_card_number('0000000000', num_digits=10)   # OK


@patch('common.algorithms.clean_card_number')
def test_passes_prefix_to_clean_card_number_for_correctness(clean_mock):
    '''
    Make sure the input is sanitized so that any separators are removed and so
    we don't try to generate a card number from alpha values
    '''
    prefix = MagicMock()
    clean_mock.return_value = ''
    generate_card_number(prefix)
    assert clean_mock.call_args_list[0] == call(prefix, var_name='prefix')

    clean_mock.reset_mock()
    prefix = MagicMock()
    generate_card_number(prefix, num_digits=12)
    assert clean_mock.call_args_list[0] == call(prefix, var_name='prefix')


def test_return_passes_luhn_algorithm():
    '''
    test both with & without prefix given with multiple lengths
    '''
    number = generate_card_number()
    assert luhn_check(number)

    number = generate_card_number(num_digits=15)
    assert luhn_check(number)

    number = generate_card_number('123456789', num_digits=10)
    assert luhn_check(number)

    number = generate_card_number('5612789', num_digits=17)
    assert luhn_check(number)

    number = generate_card_number('55', num_digits=MIN_LENGTH)
    assert luhn_check(number)

    number = generate_card_number('4', num_digits=MAX_LENGTH)
    assert luhn_check(number)
