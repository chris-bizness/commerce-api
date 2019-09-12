"""
    All BIN range values found @ https://www.bincodes.com/bin-list/
"""


def is_visa(card_number):
    return card_number.startswith("4")


def is_master_card(card_number):
    return (
        "2221" <= card_number[:4] <= "2720"
        or "51" <= card_number[:2] <= "55"
    )


def is_discover_card(card_number):
    return (
        card_number.startswith("6011")
        or card_number.startswith("65")
        or "622126" <= card_number[:6] <= "622925"
        or "644" <= card_number[:3] <= "649"
    )


def is_american_express(card_number):
    return (
        card_number.startswith("34")
        or card_number.startswith("37")
    )
