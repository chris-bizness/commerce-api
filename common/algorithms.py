import re


def is_all_digits(maybe_all_digits):
    return bool(re.fullmatch(r'\d+', maybe_all_digits))


def clean_card_number(card_number):
    '''
    Many users tend to add spaces, dashes, or periods in between chunks of
    numbers on their credit cards. Clean the number by removing all the "spacer"
    characters from the card number, and assert the result is only digits.
    '''
    if not isinstance(card_number, str):
        raise TypeError(
            f"Expected card_number to be type 'str'. Got: {type(card_number)}"
        )

    ignore_characters = [' ', '.', ',', '|', ':', ';', '-']
    for ignore in ignore_characters:
        card_number = card_number.replace(ignore, '')
    if not is_all_digits(card_number):
        raise ValueError(
            f"Card number must be string of digits. Got: {card_number}"
        )
    return card_number


def luhn_check(card_number: str) -> bool:
    '''
    Takes the card number to check against the Luhn algorithm and returns
    True/False for whether it passed
    '''
    card_number = clean_card_number(card_number)
    valid_check_digit = _get_luhn_check_digit(card_number)
    return valid_check_digit == card_number[-1:]


def _get_luhn_check_digit(
    card_number: str,
    *,
    is_incomplete: bool = False
) -> int:
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
        doubled = digit * 2
        clamped = (doubled - 1) % 9 + 1
        check_sum += clamped
    check_sum += sum(int(x) for x in remaining)

    return 10 - (check_sum % 10)
