
# In 2017, the ISO updated its payment card number standard to
#   lengthen the IIN from 6 digits to 8 (ISO/IEC 7812-1:2017)
# The standard will be enforced by most major banks starting in 2022
IIN_LENGTH = 6  # TODO: Update this value (most likely in 2022)


# According to the ISO standard, there needs to be a 6-digit IIN, 1 digit to
# serve as the "check digit", and at least 1 digit for the personal account
# number. The PAN can have up to 12 digits (12 + 6 + 1 = 19)
MIN_PAYMENT_CARD_NUMBER_LENGTH = 8
MAX_PAYMENT_CARD_NUMBER_LENGTH = 19


# Users tend to input their card numbers with spacers where the card shows them
# These tend to be the most common spacer characters
COMMON_SEPARATORS = [' ', '.', ',', '|', ':', ';', '-', '\t']
