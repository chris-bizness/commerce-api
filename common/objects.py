from common.bin_tests import (
    is_visa,
    is_master_card,
    is_discover_card,
    is_american_express,
)
from common.algorithms import luhn_check
from typing import NoReturn

# In 2017, the ISO updated its payment card number standard to
#   lengthen the IIN from 6 digits to 8 (ISO/IEC 7812-1:2017)
# The standard will be enforced by most major banks starting in 2022
IIN_LENGTH = 6  # TODO: Update this value in 2022


# Common banks' BIN tests
COMMON_BIN_TESTS = {
    'American Express': is_american_express,
    'Discover Card': is_discover_card,
    'MasterCard': is_master_card,
    'Visa': is_visa,
}


class PaymentCardNumber:
    """
    A class encapsulating common functionality used for payment card numbers
    """

    def __init__(self, card_number: str):
        self._number: str = card_number
        self._validity_checked_for: str = None
        self._is_valid: bool = None

    @property
    def mii(self) -> str:
        '''
        The Major Industry Identifier
        The first digit of the card number
        '''
        return self._number[:1]     # Use slice notation to guarantee safety

    # TODO: Update the `iin` docstring when IIN_LENGTH changes
    @property
    def iin(self) -> str:
        '''
        The Issuer Identification Number (AKA the Bank Identification Number)
        The first 6 digits (soon to be 8) in a payment card number
        '''
        return self._number[:IIN_LENGTH]

    @property
    def account_number(self) -> str:
        '''
        The personal identification number stored as part of the payment card
        number.
        The card number with the check digit and the IIN removed.
        '''
        return self._number[IIN_LENGTH:-1]

    @property
    def check_digit(self) -> str:
        '''
        The final digit of the payment card number
        Used by the Luhn algorithm to minimize errors from typos & accidents
        '''
        return self._number[-1:]    # Use slice notation to guarantee safety

    @property
    def is_valid(self) -> bool:
        '''
        Uses the Luhn algorithm and card number length to determine validity
        Does not guarantee the card number is in use
        '''
        if self._is_valid is None or self._validity_checked_for != self._number:
            self._set_validity()
        return self._is_valid

    @property
    def issuer(self):
        '''
        The issuer of the card number determined by the IIN
        '''
        for issuer, test_func in COMMON_BIN_TESTS.items():
            if test_func(self._number):
                return issuer
        return None

    def _set_validity(self) -> NoReturn:
        self._validity_checked_for, self._is_valid = (
            self._number,
            luhn_check(self._number)
        )
