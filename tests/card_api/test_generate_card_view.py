from furl import furl
from rest_framework.test import APIClient
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)


def _test(**kwargs):
    client = APIClient()
    return client.get(furl('/card-number/generate', args=kwargs).url)


def test_returns_400_for_bad_length():
    assert _test(length=MIN_LENGTH - 1).status_code == 400
    assert _test(length=MAX_LENGTH + 1).status_code == 400
    assert _test(length='zero').status_code == 400


def test_returns_400_for_invalid_prefix():
    assert _test(prefix='a').status_code == 400
    assert _test(prefix='0000 0000 0000 0000 0000').status_code == 400
    assert _test(prefix='...').status_code == 400


def test_returns_400_if_issuer_not_found():
    assert _test(issuer="bob hope").status_code == 400
    assert _test(issuer="vias").status_code == 400
    assert _test(issuer="VIZA").status_code == 400


def test_without_query_string_params_returns_16_digits():
    json_resp = _test().data
    assert 'number' in json_resp
    assert len(json_resp['number']) == 16
    assert json_resp['details']['isValid']


def test_returns_400_if_issuer_and_anything_else_set():
    assert _test(issuer='visa', length=16).status_code == 400
    assert _test(issuer='visa', prefix='419235').status_code == 400
    assert _test(issuer='visa', prefix='419235', length=16).status_code == 400


def test_prefix_works_as_expected():
    prefix = '98347'
    json_resp = _test(prefix=prefix).data
    assert json_resp['number'].startswith(prefix)
    assert json_resp['details']['isValid']

    prefix = '12345567'
    json_resp = _test(prefix=prefix, length=14).data
    num = json_resp['number']
    assert num.startswith(prefix)
    assert len(num) == 14
    assert json_resp['details']['isValid']

    json_resp = _test(length=MIN_LENGTH).data
    assert len(json_resp['number']) == MIN_LENGTH

    prefix = '19'
    json_resp = _test(prefix=prefix, length=MIN_LENGTH).data
    num = json_resp['number']
    assert len(num) == MIN_LENGTH
    assert num.startswith(prefix)


def test_issuer_works_as_expected():
    json_resp = _test(issuer='amex').data
    num = json_resp['number']
    issuer = json_resp['details']['issuer'].lower().replace(' ', '')
    assert num.startswith('34') or num.startswith('37')
    assert issuer == 'americanexpress'

    json_resp = _test(issuer='American Express').data
    num = json_resp['number']
    issuer = json_resp['details']['issuer'].lower().replace(' ', '')
    assert num.startswith('34') or num.startswith('37')
    assert issuer == 'americanexpress'

    json_resp = _test(issuer='VISA').data
    num = json_resp['number']
    issuer = json_resp['details']['issuer'].lower().replace(' ', '')
    assert num.startswith('4')
    assert issuer == 'visa'
