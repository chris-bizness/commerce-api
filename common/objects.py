from common.bin_tests import (
    is_visa,
    is_master_card,
    is_discover_card,
    is_american_express,
)
from common.enums import CardIssuer
from common.algorithms import luhn_check, clean_card_number
from common.constants import (
    IIN_LENGTH,
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH
)


# Common banks' BIN tests
COMMON_BIN_TESTS = {
    CardIssuer.AMEX: is_american_express,
    CardIssuer.DISCOVER: is_discover_card,
    CardIssuer.MASTER_CARD: is_master_card,
    CardIssuer.VISA: is_visa,
}


class PaymentCardNumber:
    """
    A class encapsulating common functionality used for payment card numbers
    """

    def __init__(self, card_number: str):
        self.value = card_number

    @property
    def value(self) -> str:
        return self._number

    @value.setter
    def value(self, new_value: str) -> str:
        self._number = clean_card_number(new_value)
        return self._number

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
        return (
            MIN_LENGTH <= len(self._number) <= MAX_LENGTH
            and luhn_check(self.value)
        )

    @property
    def issuer(self) -> str:
        '''
        The issuer of the card number determined by the IIN
        '''
        for issuer, test_func in COMMON_BIN_TESTS.items():
            if test_func(self._number):
                return issuer.value
        return None
