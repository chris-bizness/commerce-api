import re
import string
import random
from common.constants import (
    COMMON_SEPARATORS,
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)
from common.enums import CardIssuer


def is_all_digits(maybe_all_digits):
    '''
    Returns True if the input string contains only digits (0-9), otherwise False
    '''
    return bool(re.fullmatch(r'\d+', maybe_all_digits))


def clean_card_number(card_number, *, var_name='card_number'):
    '''
    Many users tend to add spaces, dashes, or periods in between chunks of
    numbers on their credit cards. Clean the number by removing all the "spacer"
    characters from the card number, and assert the result is only digits.
    '''
    if not isinstance(card_number, str):
        raise TypeError(
            f"Expected {var_name} to be type 'str'. Got: {type(card_number)}"
        )

    for ignore in COMMON_SEPARATORS:
        card_number = card_number.replace(ignore, '')
    if not is_all_digits(card_number):
        raise ValueError(
            f"{var_name} must be string of digits. Got: {card_number}"
        )
    return card_number


def luhn_check(card_number):
    '''
    Takes the card number to check against the Luhn algorithm and returns
    True/False for whether it passed
    '''
    card_number = clean_card_number(card_number)
    valid_check_digit = str(_get_luhn_check_digit(card_number))
    cur_check_digit = card_number[-1:]
    return valid_check_digit == cur_check_digit


def _get_luhn_check_digit(card_number, *, is_incomplete=False):
    '''
    Takes as input a card_number (string) and a flag `is_incomplete` which
    denotes whether the card number contains the (either valid or invalid)
    check digit already

    https://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    card_number = clean_card_number(card_number)

    if not is_incomplete:
        card_number = card_number[:-1]

    check_sum = 0
    to_double, remaining = card_number[::-2], card_number[:-1][::-2]
    for digit in to_double:
        doubled = int(digit) * 2
        if doubled > 9:
            doubled -= 9
        check_sum += doubled
    check_sum += sum(int(x) for x in remaining)

    return (10 - (check_sum % 10)) % 10


def generate_card_number(prefix=None, *, num_digits=16):
    '''
    Generate a random card number that passes the Luhn algorithm, given:
        a prefix (optional)
            &
        the number of digits to generate (optional - defaults to 16)
    '''
    if num_digits < MIN_LENGTH or num_digits > MAX_LENGTH:
        raise ValueError(
            "Invalid length requested. Valid card numbers must be a length"
            f" between [{MIN_LENGTH}, {MAX_LENGTH}] inclusive."
        )

    if not prefix:
        prefix = ''
    else:
        # Make sure we only have digits and that when we're checking how many
        # digits to generate, we have the actual length without separators
        prefix = clean_card_number(prefix, var_name='prefix')
    length = len(prefix)
    if length > num_digits:
        raise ValueError(
            "Too many digits given in prefix. Card number of length "
            f"{num_digits} requested, but {length} digits already given.")
    if length == num_digits:
        check = _get_luhn_check_digit(prefix)
        if str(check) == prefix[-1]:
            return prefix
        raise ValueError(
            "Requested a card number of the same length as digits given, but "
            f"check digit is incorrect. Given '{prefix}', but check digit must "
            f"be '{check}'."
        )
    randoms_needed = num_digits - length - 1
    while randoms_needed > 0:
        prefix += random.choice(string.digits)
        randoms_needed -= 1

    check = _get_luhn_check_digit(prefix, is_incomplete=True)
    return prefix + str(check)


def generate_card_number_from_issuer(issuer):
    '''
    Pass in a string or CardIssuer enum to generate a random card number
    with a BIN matching one of that issuer's BIN ranges
    '''
    create_from = CardIssuer.from_string(issuer)
    if not create_from:
        raise ValueError(f"Unable to find CardIssuer matching '{issuer}'.")

    prefix_range = random.choice(create_from.bin_ranges)
    if isinstance(prefix_range, str):
        prefix = prefix_range
    else:
        start, end = prefix_range
        if start.startswith('0') or end.startswith('0'):
            # None of the BINs we care about right now begin with a 0,
            # so let's worry about this later
            raise NotImplementedError(
                "Implement a method that does not cast the start/end "
                "as integers because leading 0s will be lost."
            )
        prefix = str(random.randint(int(start), int(end)))
    return generate_card_number(
        prefix=prefix,
        num_digits=create_from.num_digits
    )
