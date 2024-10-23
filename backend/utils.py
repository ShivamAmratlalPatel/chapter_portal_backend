"""Utility functions."""
from datetime import date, datetime
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

import pytz
from _decimal import Decimal
from pydantic import BaseModel, StringConstraints


def generate_uuid() -> UUID:
    """
    Generate a UUID4.

    Returns
        UUID: UUID4

    Examples
        >>> generate_uuid()
        UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')
    """
    return uuid4()


def datetime_now() -> datetime:
    """
    Get the current datetime for London.

    Returns
        datetime: current datetime

    """
    uk_tz = pytz.timezone("Europe/London")
    return datetime.now(tz=uk_tz)


def full_name_as_string(
    title: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> str:
    """
    Get a full name as a string.

    Args:
        title: title
        first_name: first name
        last_name: last name

    Returns:
        str: full name

    Examples:
        >>> full_name_as_string("Mr", "John", "Smith")
        'Mr John Smith'
        >>> full_name_as_string("Mr", None, "Smith")
        'Mr Smith'
        >>> full_name_as_string(None, "John", "Smith")
        'John Smith'
        >>> full_name_as_string(None, None, "Smith")
        'Smith'
        >>> full_name_as_string(None, None, None)
        ''

    """
    parts = [part.strip() for part in [title, first_name, last_name] if part]
    return " ".join(parts)


def convert_list_to_list(data: list, format_date: bool) -> list:
    """
    Recursively converts a list to a list, handling enum values and datetime fields.

    Args:
        data (list): The list to convert.
        format_date (bool): Specifies whether to format datetime and date fields as strings.

    Returns:
        list: The converted list.
    """
    result = []
    for value in data:
        if isinstance(value, Enum):
            result.append(value.value)
        elif isinstance(value, dict):
            result.append(convert_dict_to_dict(value, format_date))
        elif (format_date and isinstance(value, datetime | date)) or isinstance(
            value,
            UUID,
        ):
            result.append(str(value))
        elif isinstance(value, Decimal):
            result.append(float(value))
        elif isinstance(value, list):
            result.append(convert_list_to_list(value, format_date))
        elif isinstance(value, BaseModel):
            result.append(object_to_dict(value, format_date))
        else:
            result.append(value)
    return result


def convert_dict_to_dict(data: dict, format_date: bool) -> dict:
    """
    Recursively converts a dictionary to a dictionary, handling enum values and datetime fields.

    Args:
        data (dict): The dictionary to convert.
        format_date (bool): Specifies whether to format datetime and date fields as strings.

    Returns:
        dict: The converted dictionary.
    """
    result = {}

    for key, value in data.items():
        if isinstance(value, Enum):
            result[key] = value.value
        elif isinstance(value, dict):
            result[key] = convert_dict_to_dict(value, format_date)
        elif (format_date and isinstance(value, datetime | date)) or isinstance(
            value,
            UUID,
        ):
            result[key] = str(value)
        elif isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, list):
            result[key] = convert_list_to_list(value, format_date)
        elif isinstance(value, BaseModel):
            result[key] = object_to_dict(value, format_date)
        else:
            result[key] = value
    return result


def object_to_dict(data: BaseModel | dict, format_date: bool = True) -> dict:
    """
    Convert a Pydantic model or dictionary instance to a dictionary recursively, providing a JSON-like representation.

    Args:
        data (BaseModel | dict): The Pydantic model or dictionary to convert.
        format_date (bool, optional): Specifies whether to format datetime and date fields as strings. Defaults to False.

    Returns:
        dict: The dictionary representation of the model.
    """
    if isinstance(data, BaseModel):
        data = data.model_dump()
    return convert_dict_to_dict(data, format_date)


def space_in_postcode(postcode: str) -> str:
    """
    Add a space in a postcode.

    Args:
        postcode: postcode

    Returns:
        str: postcode with space

    """
    postcode = postcode.replace(" ", "")
    if len(postcode) in [5, 6, 7]:
        return postcode[:-3] + " " + postcode[-3:]
    else:
        return postcode


def short_address(
    street1: Annotated[str, StringConstraints(min_length=1, max_length=100)],
    post_code: Annotated[str, StringConstraints(min_length=1, max_length=100)],
    building_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    | None = None,
    sub_building: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    | None = None,
) -> str:
    """
    Get a short address.

    Args:
        street1 (str): street1
        post_code (str): post_code
        building_name (str, optional): building_name. Defaults to None.
        sub_building (str, optional): sub_building. Defaults to None.

    Returns:
        str: short address

    Examples:
        >>> short_address("1 Test Street", "SW1A 1AA")
        '1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "Test Building")
        'Test Building 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "Test Building", "Flat 1")
        'Flat 1 Test Building 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", None, "Flat 1")
        'Flat 1 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "Test Building", None)
        'Test Building 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", None, None)
        '1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "", "")
        '1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "Test Building", "")
        'Test Building 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "", "Flat 1")
        'Flat 1 1 Test Street, SW1A 1AA'
        >>> short_address("1 Test Street", "SW1A 1AA", "Test Building", "Flat 1")
        'Flat 1 Test Building 1 Test Street, SW1A 1AA'

    Raises:
        TypeError: street1 is required
        TypeError: post_code is required
    """
    if street1 is None or len(street1) == 0:
        msg = "street1 is required"
        raise TypeError(msg)
    if post_code is None or len(post_code) == 0:
        msg = "post_code is required"
        raise TypeError(msg)
    street_address = f"{street1.strip()}, {space_in_postcode(post_code)}"
    if building_name is not None and len(building_name) > 0:
        street_address = f"{building_name.strip()} {street_address.strip()}"
    if sub_building is not None and len(sub_building) > 0:
        street_address = f"{sub_building.strip()} {street_address.strip()}"
    return street_address
