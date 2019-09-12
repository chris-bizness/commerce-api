from enum import Enum


class CardIssuer(Enum):
    VISA = 'Visa'
    AMEX = 'American Express'
    DISCOVER = 'Discover Card'
    MASTER_CARD = 'Master Card'

    @property
    def num_digits(self):
        '''
        The length of the card number for the card issuer
        '''
        return 15 if self is self.MASTER_CARD else 16

    @property
    def bin_ranges(self):
        '''
        Get a list of BIN prefixes and/or BIN prefix ranges for the issuer
        '''
        prefixes = {
            self.VISA: ['4'],
            self.MASTER_CARD: [('2221', '2720'), ('51', '55')],
            self.DISCOVER: ['6011', '65', ('622126', '622925'), ('644', '649')],
            self.AMEX: ['34', '37'],
        }
        return prefixes.get(self, [])

    @classmethod
    def from_string(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            return None

        def _cleanse_str(val):
            remove_all_of = ' _'
            val = val.lower()
            for char in remove_all_of:
                val = val.replace(char, '')
            return val

        value = _cleanse_str(value)
        for enum in cls:
            if value in (_cleanse_str(enum.name), _cleanse_str(enum.value)):
                return enum
        return None
