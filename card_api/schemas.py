from rest_framework.schemas.openapi import AutoSchema
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)


NUMBER_DETAIL_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "isValid": {
            "type": "bool",
            "example": True,
        },
        "majorIndustryIdentifier": {
            "type": "string",
            "pattern": r"\d",
            "example": "4"
        },
        "issuerIdentificationNumber": {
            "type": "string",
            "pattern": r"\d{6}",
            "example": "123456"
        },
        "personalAccountNumber": {
            "type": "string",
            "pattern": r"\d{1,12}",
            "example": "123456789012"
        },
        "checkDigit": {
            "type": "string",
            "pattern": r"\d",
            "example": "8"
        }
    }
}


class _Schema(AutoSchema):
    request_body = None
    responses = None
    parameters = None

    def get_operation(self, *args, **kwargs):
        retval = super().get_operation(*args, **kwargs)
        if self.request_body:
            retval['requestBody'] = self.request_body
        if self.responses:
            retval['responses'] = self.responses
        if self.parameters:
            retval['parameters'] = self.parameters
        return retval


class ValidateCardSchema(_Schema):
    request_body = {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "string",
                            "pattern": r"[0123456789 .-|:;]+",
                            "description": (
                                "The payment card number to validate. "
                                "Common separators; such as spaces, "
                                "dashes, periods, etc.; are allowed "
                                "between digits."
                            ),
                            "example": "0000 0000 0000 0000",
                        }
                    },
                    "required": ["number"]
                }
            }
        }
    }

    responses = {
        "200": {
            "description": "A payment card number descriptor object",
            "content": {
                "application/json": {
                    "schema": NUMBER_DETAIL_RESPONSE_SCHEMA
                }
            }
        },
        "400": {
            "description": (
                f"`number` is less than {MIN_LENGTH} digits, "
                f"greater than {MAX_LENGTH} digits, "
                "or contains invalid characters"
            )
        },
        "default": {
            "description": "Unexpected error"
        }
    }


class GenerateCardSchema(_Schema):
    responses = {
        "200": {
            "description": "A payment card number object",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "number": {
                                "type": "string",
                                "pattern": r"\d{8,19}",
                                "example": "4024007168211802"
                            },
                            "details": NUMBER_DETAIL_RESPONSE_SCHEMA,
                        }
                    }
                }
            }
        },
        "400": {
            "description": "`issuer`, `prefix`, or `length` is an invalid value"
        },
        "default": {
            "description": "Unexpected error"
        }
    }

    parameters = [{
        "in": "query",
        "name": "issuer",
        "schema": {
            "type": "string"
        },
        "description": "The CardIssuer for the generated card to have the BIN "
        "and length of. May not be used with `length` or `prefix`."
    }, {
        "in": "query",
        "name": "length",
        "schema": {
            "type": "integer"
        },
        "description": "Specify the number of digits for the generated card to "
        "contain."
    }, {
        "in": "query",
        "name": "prefix",
        "schema": {
            "type": "string"
        },
        "description": "The digits for the generated card to begin with."
    }]
