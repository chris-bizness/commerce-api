import re
import string
from rest_framework import serializers
from common.constants import COMMON_SEPARATORS


def validate_contains_only_digits_and_separators(value):
    allowed_characters = re.escape(string.digits + ''.join(COMMON_SEPARATORS))
    only_allowed = re.match(f"[{allowed_characters}]+$", value)
    if not only_allowed:
        raise serializers.ValidationError(
            f"Only digits and common separators ({','.join(COMMON_SEPARATORS)})"
            " are allowed"
        )


class LengthWithoutSeparatorsValidator:
    def __init__(self, *, min=None, max=None):
        if min is None and max is None:
            raise ValueError("At least one of (min, max) requires a value")
        self._min = min
        self._max = max

    def __call__(self, value):
        if not isinstance(value, str):
            return  # SRP
        for separator in COMMON_SEPARATORS:
            value = value.replace(separator, '')
        if isinstance(self._min, int) and len(value) < self._min:
            raise serializers.ValidationError(
                f"Value must have at least {self._min}"
                f" character{'' if self._min == 1 else 's'}."
            )
        if isinstance(self._max, int) and len(value) > self._max:
            raise serializers.ValidationError(
                f"Value must have {self._max}"
                f" character{'' if self._max == 1 else 's'} or fewer."
            )
