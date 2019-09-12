from common.bin_tests import (
    is_visa,
    is_master_card,
    is_discover_card,
    is_american_express
)
from unittest.mock import MagicMock, Mock


def test_is_visa_works_for_anything_starting_with_4():
    should_pass = [
        "412565432354",
        "498234980",
        "48327",
        "4444444444444444",
        "4"
    ]
    for test in should_pass:
        assert is_visa(test) is True


def test_is_visa_false_for_anything_not_starting_with_4():
    class RestrictedCalls:
        startswith = None

    def _not_4(start):
        return start != '4'

    # don't allow slices, etc.
    _input = Mock(spec=RestrictedCalls)
    _input.startswith.side_effect = _not_4

    assert is_visa(_input) is False


def test_is_master_card_succeeds_between_2221_2720_and_51_55():
    should_pass = [
        # 2221 - 2720
        "222100000000000",
        "2720999999999999",
        "26129849389023",
        "2354789387128947",
        "2222222222222222",

        # 51 - 55
        "5599999999999999",
        "5100000000000000",
        "51",
        "55",
        "5234545654212434",
        "534545654212434",
        "54545654212434",
    ]

    for test in should_pass:
        assert is_master_card(test) is True

    should_fail = [
        "0000000000000000",
        "1111111111111111",
        "1000000000000000",
        "2122222222222222",
        "2000000000000000",
        "3333333333333333",
        "3000000000000000",
        "4444444444444444",
        "4000000000000000",
        "5655555555555555",
        "5000000000000000",
        "6666666666666666",
        "6000000000000000",
        "7777777777777777",
        "7000000000000000",
        "8888888888888888",
        "8000000000000000",
        "9999999999999999",
        "9000000000000000",

        "2220.9999999999999999999",  # not a number, doesn't round
        "2721000000000000",

        "50.9999999999999999999",  # not a number, doesn't round
        "5099999999999999",
        "5600000000000000",
    ]

    for test in should_fail:
        assert is_master_card(test) is False


def test_is_discover_card_true_for_65_6011_between_622126_622925_and_644_649():
    should_pass = [
        # 65
        "6500000000000000",
        "6537647638642923",
        "6588387487337781",
        "6599999999999999",

        # 6011
        "6011000000000000",
        "6011828943758979",
        "6011128378374397",
        "6011999999999999",

        # 622126 - 622925
        "6221260000000000",
        "6223874589393899",
        "6224897385409893",
        "6225874589387289",
        "6226373282992388",
        "6227487847838489",
        "6228873483773889",
        "6229259999999999",

        # 644 - 649
        "6440000000000000",
        "6452384789792734",
        "6462873489892340",
        "6472938478987389",
        "6488937489289374",
        "6490000000000000",
        "6499999999999999",
    ]

    for test in should_pass:
        assert is_discover_card(test) is True

    should_fail = [
        "0000000000000000",
        "1111111111111111",
        "1000000000000000",
        "2222222222222222",
        "2000000000000000",
        "3333333333333333",
        "3000000000000000",
        "4444444444444444",
        "4000000000000000",
        "5555555555555555",
        "5000000000000000",
        "6666666666666666",
        "6000000000000000",
        "7777777777777777",
        "7000000000000000",
        "8888888888888888",
        "8000000000000000",
        "9999999999999999",
        "9000000000000000",

        "6010.9999999999999999999",  # not a number, doesn't round
        "622125.9999999999999999999",  # not a number, doesn't round
        "643.9999999999999999999",  # not a number, doesn't round
        "64.9999999999999999999",  # not a number, doesn't round

        "6600000000000000",
        "6012000000000000",
        "6229260000000000",

    ]

    for test in should_fail:
        assert is_discover_card(test) is False


def test_is_american_express_true_for_34_start_or_37_start():
    class RestrictedCalls:
        startswith = None

    def _only_34_37(string):
        return string in ['34', '37']

    # don't allow slices, etc.
    _input = Mock(spec=RestrictedCalls)
    _input.startswith.side_effect = _only_34_37

    assert is_american_express(_input) is True

    assert is_american_express("343273489765637823") is True
    assert is_american_express("37982734878923") is True
    assert is_american_express("340000000000000000") is True
    assert is_american_express("379999999999999999") is True


def test_is_american_express_false_for_anything_else():
    class RestrictedCalls:
        startswith = None

    def _not_34_37(string):
        return string not in ['34', '37']

    # don't allow slices, etc.
    _input = Mock(spec=RestrictedCalls)
    _input.startswith.side_effect = _not_34_37

    assert is_american_express(_input) is False

    assert is_american_express("35234789686234931") is False
    assert is_american_express("36892346786839274") is False
