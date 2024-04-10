"""Schemas for the backend."""
import re
from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator


class Message(BaseModel):
    """Message schema."""

    message: Annotated[str, StringConstraints(strict=True, min_length=1)]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Success",
            },
        },
    )


class Error(BaseModel):
    """Error schema."""

    detail: Annotated[str, StringConstraints(strict=True, min_length=1)]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Error",
            },
        },
    )


def validate_phone_number(phone_number: str | None) -> str | None:
    """
    Validate phone number.

    This function takes a phone number as input and checks if it is a valid international phone number.
    A valid phone number should be in the format of a plus sign (+) followed by one or more digits (0-9).
    The function allows optional spaces within the phone number, which are removed during validation.

    Args:
        phone_number (str | None): The phone number to be validated. It can be either a string or None.

    Returns:
        str | None: The validated phone number if it is valid. If the input phone number is None, it returns None.

    Raises:
        ValueError: If the input phone number is a string and does not match the valid phone number format.

    Example:
        >>> validate_phone_number("+1 555 1234567")
        '+15551234567'
        >>> validate_phone_number("+44 20 7123 4567")
        '+442071234567'
        >>> validate_phone_number(None)
        None

    Note:
        - The function uses regular expressions to match the phone number format, allowing flexibility in handling various formats.
        - The plus sign (+) at the beginning is mandatory, and there should be no other characters except digits (0-9).
        - Any spaces within the phone number are removed before validation.
        - The function raises a ValueError if the input phone number is a string but does not match the valid format.
        - If the input phone number is None, it is considered valid and returns None as the output.
    """
    # Regular expression pattern to match a valid phone number format: ^\+[0-9]+$
    regex = r"^\+[0-9]+$"

    # Remove any spaces from the phone number if it is a string
    if isinstance(phone_number, str):
        phone_number = phone_number.replace(" ", "")

    # If the phone number is not None and does not match the valid format, raise a ValueError
    if phone_number is not None and not re.search(regex, phone_number, re.I):
        msg = "Phone Number Invalid."
        raise ValueError(msg)

    return phone_number


class Address(BaseModel):
    """
    Address schema.

    Represents a physical address with various fields.

    Attributes
        county (str, optional): The county of the address.
        building_name (str): The name of the building.
        post_code (str): The postal code of the address.
        city (str): The city or locality of the address.
        street1 (str): The primary street address.
        sub_building (str, optional): The sub-building or apartment number.
        country (str, optional): The country of the address.
    """

    county: str | None = None
    building_name: str
    post_code: str
    city: str
    street1: str
    sub_building: str | None = None
    country: str | None = None

    @field_validator("post_code")
    @classmethod
    def validate_post_code(cls: "Address", value: str) -> str:
        """
        Validate the format of the postal code.

        Postal code must be a string containing valid alphanumeric characters.

        Args:
            value (Union[str, int]): The postal code to validate.

        Returns:
            str: The valid postal code.

        Raises:
            ValueError: If the postal code is not a string or contains invalid characters.
        """
        value = value.replace(" ", "")

        if not value.isalnum():
            msg = "Postal code must contain only alphanumeric characters."
            raise ValueError(msg)

        return value

    model_config = ConfigDict(from_attributes=True)


class SortBy(str, Enum):
    """SortBy enumeration."""

    date_asc = "date_asc"
    date_desc = "date_desc"
    a_z_asc = "a_z_asc"
    a_z_desc = "a_z_desc"
    action_required = "action_required"
    move_in_asc = "move_in_asc"
    move_in_desc = "move_in_desc"

    __slots__ = ()


class NextPage(BaseModel):
    """NextPage schema."""

    previous: bool
    cursor_column: datetime | date | str
    cursor_id: UUID


class PaginationResult(BaseModel):
    """PaginationResult schema."""

    next: NextPage | None
    previous: NextPage | None
    results: list[Any]
