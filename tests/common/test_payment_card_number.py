'''
Many of the tests refer to the ISO specification for a payment card number.
An easy-to-read version can be found on Wikipedia:
    https://en.wikipedia.org/wiki/Payment_card_number
'''
from common.enums import CardIssuer
from unittest.mock import patch, MagicMock
from common.objects import PaymentCardNumber


def test_mii_returns_first_digit():
    '''
    The first digit is the MII
    '''
    assert PaymentCardNumber("0123456789").mii == "0"
    assert PaymentCardNumber("9876543210").mii == "9"
    assert PaymentCardNumber("5019283746").mii == "5"


def test_iin_returns_first_6_digits():
    '''
    The first 6 (soon-to-be 8) digits are the IIN
    '''
    assert PaymentCardNumber("5019283746").iin == "501928"
    assert PaymentCardNumber("0000000000").iin == "000000"
    assert PaymentCardNumber("2810746359").iin == "281074"
    assert PaymentCardNumber("0123456789").iin == "012345"
    assert PaymentCardNumber("9357018246").iin == "935701"


def test_check_digit_returns_last_digit():
    '''
    The final digit is the "check digit"
    '''
    assert PaymentCardNumber("5019283746").check_digit == "6"
    assert PaymentCardNumber("0000000000").check_digit == "0"
    assert PaymentCardNumber("2810746395").check_digit == "5"
    assert PaymentCardNumber("0123456789").check_digit == "9"
    assert PaymentCardNumber("9357018246").check_digit == "6"


def test_account_number_excludes_check_digit_and_iin():
    '''
    the account number is the user-specific part of the card number
    which excludes the check digit and the IIN
    '''
    def _test(value):
        return PaymentCardNumber(value).account_number
    # The ISO spec says it can be up to 12 digits long
    assert _test("0123456899437865120") == "689943786512"
    # test variable sizes
    assert _test("5019283746") == "374"
    assert _test("000000000000000") == "00000000"
    assert _test("01234567") == "6"
    assert _test("93570182469815") == "8246981"


def test_is_valid_checks_number_length():
    '''
    A card number must have:
        - 6 (soon to be 8) digits for the IIN
        - 1 digit for the check digit
        - at least 1 digit for the account number, up to a max of 12
    '''
    # too small
    assert PaymentCardNumber("0" * 7).is_valid is False
    assert PaymentCardNumber("0000000").is_valid is False
    assert PaymentCardNumber("00000-00").is_valid is False
    assert PaymentCardNumber("    0    ").is_valid is False
    assert PaymentCardNumber("0       0").is_valid is False
    assert PaymentCardNumber("0   0   0").is_valid is False
    assert PaymentCardNumber("1   2   3").is_valid is False

    assert PaymentCardNumber("0" * 20).is_valid is False
    assert PaymentCardNumber("12345678901234567890").is_valid is False

    assert PaymentCardNumber("0" * 8).is_valid is True
    assert PaymentCardNumber("0" * 19).is_valid is True


@patch('common.objects.luhn_check')
def test_is_valid_uses_luhn_algorithm(luhn_check_mock):
    '''
    For a card to be valid, it must pass the Luhn algorithm, which checks
    the "check digit" to prevent errors from typos & accidents
    '''
    luhn_check_mock.return_value = False
    obj = PaymentCardNumber("4444 4444 4444 4448")
    assert obj.is_valid is False
    luhn_check_mock.assert_called_once_with("4444444444444448")

    luhn_check_mock.reset_mock()
    luhn_check_mock.return_value = True
    assert obj.is_valid is True
    luhn_check_mock.assert_called_once_with("4444444444444448")


def test_failing_issuer_returns_None():
    '''
    If an issuer can't be determined, it should return a sane default
    '''
    assert PaymentCardNumber("0" * 16).issuer is None
    assert PaymentCardNumber("9236 4763 8920 3974").issuer is None


@patch('common.objects.COMMON_BIN_TESTS')
def test_issuer_returns_issuer_matching_passing_test(bin_test_mocks):
    '''
    If the corresponding BIN test is passed, the issuer's name is returned
    '''
    amex_mock, disc_mock, mc_mock, v_mock = [MagicMock() for i in range(4)]
    bin_test_mocks.items.return_value = {
        CardIssuer.VISA: v_mock,
        CardIssuer.AMEX: amex_mock,
        CardIssuer.DISCOVER: disc_mock,
        CardIssuer.MASTER_CARD: mc_mock,
    }.items()

    def _test(obj) -> str:
        issuer = obj.issuer
        if not issuer:
            return issuer
        # Strings tend to change and spaces are added or caps are changed
        # This helps ensure we don't need to rewrite this test every time a
        # minor string change occurs
        return issuer.lower().replace(' ', '')

    def _reset():
        for mock in [amex_mock, disc_mock, mc_mock, v_mock]:
            mock.return_value = False

    _reset()
    card = PaymentCardNumber("0" * 16)
    v_mock.return_value = True
    assert _test(card) == 'visa'

    _reset()
    amex_mock.return_value = True
    assert _test(card) == 'americanexpress'

    _reset()
    disc_mock.return_value = True
    assert _test(card) == 'discovercard'

    _reset()
    mc_mock.return_value = True
    assert _test(card) == 'mastercard'
