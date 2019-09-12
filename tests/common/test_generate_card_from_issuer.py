import pytest
from unittest.mock import patch, MagicMock
from common.algorithms import generate_card_number_from_issuer


@pytest.fixture
def gen_issuer():
    issuer = MagicMock()
    random_mock = MagicMock()
    gen_card = MagicMock()
    with patch(
        'common.algorithms.CardIssuer.from_string',
        MagicMock(return_value=issuer)
    ):
        with patch('common.algorithms.random', random_mock):
            with patch('common.algorithms.generate_card_number', gen_card):
                yield issuer, random_mock, gen_card


@patch('common.algorithms.CardIssuer')
def test_issuer_not_found_throws(issuer_mock):
    issuer_mock.from_string.return_value = None
    issuer = MagicMock()
    with pytest.raises(ValueError):
        generate_card_number_from_issuer(issuer)


def test_string_range_flow(gen_issuer):
    issuer, rand, gen_card = gen_issuer

    prefix = MagicMock(spec=str)

    rand.choice.return_value = prefix

    generate_card_number_from_issuer(MagicMock())

    rand.choice.assert_called_once_with(issuer.bin_ranges)
    gen_card.assert_called_once_with(
        prefix=prefix,
        num_digits=issuer.num_digits
    )


def test_tuple_range_flow(gen_issuer):
    issuer, rand, gen_card = gen_issuer

    _range = (MagicMock(), MagicMock())
    for x, as_int in zip(_range, [3476, 234388]):
        x.startswith.return_value = False
        x.int = x.__int__.return_value = as_int
    pref = '--super-unique-string-that-no-one-would-ever-use--'

    rand.choice.return_value = _range
    rand.randint.return_value = MagicMock(__str__=MagicMock(return_value=pref))

    generate_card_number_from_issuer(MagicMock())

    rand.choice.assert_called_once_with(issuer.bin_ranges)
    rand.randint.assert_called_once_with(_range[0].int, _range[1].int)
    gen_card.assert_called_once_with(
        prefix=pref,
        num_digits=issuer.num_digits
    )
