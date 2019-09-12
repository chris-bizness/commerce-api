from rest_framework.test import APIClient


def _test(number):
    client = APIClient()
    return client.post('/validate/', {'number': number}, format='json')


def test_returns_0s_for_8_0s():
    response = _test('0' * 8)

    assert response.status_code == 200

    data = response.data

    assert data['isValid'] is True
    assert data['majorIndustryIdentifier'] == '0'
    assert data['issuerIdentificationNumber'] == '000000'
    assert data['personalAccountNumber'] == '0'
    assert data['checkDigit'] == '0'


def test_issuer_returned_if_detectable():
    '''
    If the card issuer can be determined, return the information
    '''
    response = _test(f"{'4' * 15}8")

    assert response.status_code == 200

    data = response.data

    assert data['isValid'] is True
    assert data['majorIndustryIdentifier'] == '4'
    assert data['issuerIdentificationNumber'] == '4' * 6
    assert data['personalAccountNumber'] == '4' * 9
    assert data['checkDigit'] == '8'

    assert 'issuer' in data and data['issuer'].lower() == 'visa'


def test_issuer_not_returned_if_invalid():
    '''
    While we may have enough data to determine the issuer of the invalid card
    number from the IIN, we shouldn't imply they issued this number since the
    number isn't valid
    '''
    response = _test(f"{'4' * 15}7")

    assert response.status_code == 200

    data = response.data

    assert data['isValid'] is False
    assert data['majorIndustryIdentifier'] == '4'
    assert data['issuerIdentificationNumber'] == '4' * 6
    assert data['personalAccountNumber'] == '4' * 9
    assert data['checkDigit'] == '7'

    assert 'issuer' not in data


def test_plenty_of_room_for_separators():
    '''
    It's usually best not to make assumptions about how users will input data
    '''
    sep = " -:;|;:- "
    response = _test(f"0{sep}" * 18 + "0")
    assert response.status_code == 200


def test_maximum_of_19_digits():
    '''
    Payment cards can only have a max of 19 digits, so warn the client that
    they're exceeding the threshold
    '''
    response = _test("0000 0000 0000 0000 000")
    assert response.status_code == 200
    response = _test("0000 0000 0000 0000 0000")
    assert response.status_code == 400
    response = _test("0000 0000 0000 0000 0000 0000 0000 000")
    assert response.status_code == 400


def test_minimum_of_8_digits():
    '''
    Payment cards must have at least 8 digits, so warn the client that the value
    entered cannot be a card with specific reasoning
    '''
    response = _test("0000 0000")
    assert response.status_code == 200
    response = _test("0000 000")
    assert response.status_code == 400
    response = _test("0000")
    assert response.status_code == 400
    response = _test("0")
    assert response.status_code == 400


def test_returns_400_if_wrong_input_type_given():
    response = _test(None)
    assert response.status_code == 400


def test_returns_400_if_blank_string_given():
    response = _test('')
    assert response.status_code == 400


def test_returns_400_if_non_digits_included():
    response = _test('0a1b2c3d4e5f6')
    assert response.status_code == 400
