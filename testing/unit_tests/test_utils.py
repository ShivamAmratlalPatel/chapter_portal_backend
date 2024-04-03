"""Test utils.py functions."""
import datetime
from datetime import date, datetime
from enum import Enum
from uuid import UUID

import pytest
import pytz
from _decimal import Decimal
from pydantic import BaseModel

from backend.utils import (
    convert_dict_to_dict,
    convert_list_to_list,
    datetime_now,
    full_name_as_string,
    generate_uuid,
    object_to_dict,
    short_address,
    space_in_postcode,
)


def test_generate_uuid() -> None:
    """Test generate_uuid() returns a UUID."""
    assert isinstance(generate_uuid(), UUID)


def test_datetime_now() -> None:
    """Test datetime_now() returns a datetime."""
    assert isinstance(datetime_now(), datetime)


class TestFullNameAsString:
    """Test full_name_as_string() returns a string."""

    def test_full_name_as_string(self: "TestFullNameAsString") -> None:
        """Test full_name_as_string() returns a string."""
        assert full_name_as_string("Mr", "John", "Smith") == "Mr John Smith"
        assert full_name_as_string("Mr", None, "Smith") == "Mr Smith"
        assert full_name_as_string(None, "John", "Smith") == "John Smith"
        assert full_name_as_string(None, None, "Smith") == "Smith"
        assert not full_name_as_string(None, None, None)
        assert isinstance(full_name_as_string(None, None, None), str)

    def test_full_name_as_string_with_extra_spaces(
        self: "TestFullNameAsString",
    ) -> None:
        """Test full_name_as_string() returns a string with extra spaces."""
        assert full_name_as_string("Dr", "   Jane   ", "Doe   ") == "Dr Jane Doe"

    def test_full_name_as_string_with_empty_strings(
        self: "TestFullNameAsString",
    ) -> None:
        """Test full_name_as_string() returns a string with empty strings."""
        assert not full_name_as_string("", "", "")
        assert isinstance(full_name_as_string("", "", ""), str)

    def test_full_name_as_string_with_long_title(self: "TestFullNameAsString") -> None:
        """Test full_name_as_string() returns a string with a long title."""
        assert (
            full_name_as_string("Professor", "John", "Smith") == "Professor John Smith"
        )

    def test_full_name_as_string_with_unicode_characters(
        self: "TestFullNameAsString",
    ) -> None:
        """Test full_name_as_string() returns a string with unicode characters."""
        assert full_name_as_string("Dr", "Müller", "Östberg") == "Dr Müller Östberg"


class FakeModel(BaseModel):
    """Fake model."""

    data: dict


class MyEnum(Enum):
    """My enum."""

    VALUE1 = "First value"
    VALUE2 = "Second value"


class SubModel(BaseModel):
    """Sub model."""

    value: MyEnum


class MyModel(BaseModel):
    """My model."""

    name: str
    submodel: SubModel


class TestConvertListToList:
    """Test convert_list_to_list()"""

    def test_convert_list_to_list(self: "TestConvertListToList") -> None:
        """Test convert_list_to_list() converts a list to a list."""
        data = [
            1,
            "string",
            MyEnum.VALUE1,
            {"nested": {"value": MyEnum.VALUE2}},
            datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            generate_uuid(),
            Decimal("3.14"),
            [2, 3, 4],
            [
                datetime(2022, 2, 2, tzinfo=pytz.timezone("Europe/London")),
                MyEnum.VALUE1,
                {"nested": {"value": MyEnum.VALUE2}},
            ],
        ]

        result = convert_list_to_list(data, format_date=False)

        assert result == [
            1,
            "string",
            "First value",
            {"nested": {"value": "Second value"}},
            datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            str(data[5]),
            float(data[6]),
            [2, 3, 4],
            [
                datetime(2022, 2, 2, tzinfo=pytz.timezone("Europe/London")),
                "First value",
                {"nested": {"value": "Second value"}},
            ],
        ]

    def test_convert_list_to_list_with_format_date(
        self: "TestConvertListToList",
    ) -> None:
        """Test convert_list_to_list() returns a list with formatted dates."""
        data = [
            datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            date(2022, 2, 2),
            [
                datetime(2022, 3, 3, tzinfo=pytz.timezone("Europe/London")),
                date(2022, 4, 4),
                {"nested": {"date": date(2022, 5, 5)}},
            ],
        ]

        result = convert_list_to_list(data, format_date=True)

        assert result == [
            str(datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London"))),
            "2022-02-02",
            [
                str(datetime(2022, 3, 3, tzinfo=pytz.timezone("Europe/London"))),
                "2022-04-04",
                {"nested": {"date": "2022-05-05"}},
            ],
        ]

    def test_convert_list_to_list_nested_lists(self: "TestConvertListToList") -> None:
        """Test convert_list_to_list() returns a list with nested lists."""
        data = [[1, 2, 3], [[4, 5], [6, 7]]]

        result = convert_list_to_list(data, format_date=False)

        assert result == [[1, 2, 3], [[4, 5], [6, 7]]]


class TestConvertDictToDict:
    """Test convert_dict_to_dict()"""

    def test_convert_dict_to_dict(self: "TestConvertDictToDict") -> None:
        """Test convert_dict_to_dict() returns a dict."""
        data = {
            "int_value": 42,
            "str_value": "string",
            "enum_value": MyEnum.VALUE1,
            "nested_dict": {"nested_value": MyEnum.VALUE2},
            "date_value": datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            "uuid_value": generate_uuid(),
            "decimal_value": Decimal("3.14"),
            "nested_list": [1, 2, 3],
            "mixed_list": [
                datetime(2022, 2, 2, tzinfo=pytz.timezone("Europe/London")),
                MyEnum.VALUE1,
                {"nested": {"value": MyEnum.VALUE2}},
            ],
        }

        result = convert_dict_to_dict(data, format_date=False)

        assert result == {
            "int_value": 42,
            "str_value": "string",
            "enum_value": "First value",
            "nested_dict": {"nested_value": "Second value"},
            "date_value": datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            "uuid_value": str(data["uuid_value"]),
            "decimal_value": float(data["decimal_value"]),
            "nested_list": [1, 2, 3],
            "mixed_list": [
                datetime(2022, 2, 2, tzinfo=pytz.timezone("Europe/London")),
                "First value",
                {"nested": {"value": "Second value"}},
            ],
        }

    def test_convert_dict_to_dict_with_format_date(
        self: "TestConvertDictToDict",
    ) -> None:
        """Test convert_dict_to_dict() with format_date=True."""
        data = {
            "date_value": datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            "nested_dict": {"nested_date": date(2022, 2, 2)},
            "nested_list": [
                datetime(2022, 3, 3, tzinfo=pytz.timezone("Europe/London")),
                date(2022, 4, 4),
                {"nested": {"date": date(2022, 5, 5)}},
            ],
        }

        result = convert_dict_to_dict(data, format_date=True)

        assert result == {
            "date_value": str(
                datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
            ),
            "nested_dict": {"nested_date": "2022-02-02"},
            "nested_list": [
                str(datetime(2022, 3, 3, tzinfo=pytz.timezone("Europe/London"))),
                "2022-04-04",
                {"nested": {"date": "2022-05-05"}},
            ],
        }

    def test_convert_dict_to_dict_nested_dicts(self: "TestConvertDictToDict") -> None:
        """Test convert_dict_to_dict() with nested dicts."""
        data = {
            "nested_dict": {
                "key1": "value1",
                "key2": "value2",
                "key3": {"nested_key": "nested_value"},
            },
        }

        result = convert_dict_to_dict(data, format_date=False)

        assert result == {
            "nested_dict": {
                "key1": "value1",
                "key2": "value2",
                "key3": {"nested_key": "nested_value"},
            },
        }


class TestModelToDict:
    """Test model_to_dict() returns a dict."""

    def test_model_to_dict_returns_dict(self: "TestModelToDict") -> None:
        """Test model_to_dict() returns a dict."""
        data = FakeModel(data={})
        result = object_to_dict(data)
        assert isinstance(result, dict)

    def test_model_to_dict_returns_same_dict_when_no_changes_needed(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() returns the same dict when no changes needed."""
        data = FakeModel(data={"name": "John", "age": 25})
        result = object_to_dict(data)
        assert result == {
            "data": {
                "name": "John",
                "age": 25,
            },
        }

    def test_model_to_dict_converts_nested_dict_values_to_strings(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() converts nested dict values to strings."""
        data = FakeModel(data={"nested": {"value1": 10, "value2": True}})
        result = object_to_dict(data)
        assert result == {
            "data": {"nested": {"value1": 10, "value2": True}},
        }

    def test_model_to_dict_does_not_convert_nested_dict_values_of_allowed_types(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() does not convert nested dict values of allowed types."""
        data = FakeModel(
            data={
                "nested": {
                    "value1": [1, 2, 3],
                    "value2": 3.14,
                    "value3": 42,
                    "value4": False,
                },
            },
        )
        result = object_to_dict(data)
        assert result == {
            "data": {
                "nested": {
                    "value1": [1, 2, 3],
                    "value2": 3.14,
                    "value3": 42,
                    "value4": False,
                },
            },
        }

    def test_model_to_dict_removes_key_with_value_none(self: "TestModelToDict") -> None:
        """Test model_to_dict() removes key with value None."""
        data = FakeModel(data={"name": "John", "age": None})
        result = object_to_dict(data)
        assert "age" not in result

    def test_model_to_dict_formats_date_when_format_date_true(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() formats date when format_date=True."""
        data = FakeModel(data={"date": date(2023, 7, 13)})
        result = object_to_dict(data, format_date=True)
        assert result == {
            "data": {
                "date": "2023-07-13",
            },
        }

    def test_model_to_dict_formats_datetime_when_format_date_true(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() formats datetime when format_date=True."""
        data = FakeModel(
            data={
                "datetime": datetime(
                    2023,
                    7,
                    13,
                    15,
                    30,
                    tzinfo=pytz.timezone("Europe/London"),
                ),
            },
        )
        result = object_to_dict(data, format_date=True)
        assert result == {
            "data": {
                "datetime": str(
                    datetime(
                        2023,
                        7,
                        13,
                        15,
                        30,
                        tzinfo=pytz.timezone("Europe/London"),
                    ),
                ),
            },
        }

    def test_model_to_dict_does_not_format_date_when_format_date_false(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() does not format date when format_date=False."""
        data = FakeModel(data={"date": date(2023, 7, 13)})
        result = object_to_dict(data, format_date=False)
        assert result == {
            "data": {
                "date": date(2023, 7, 13),
            },
        }

    def test_model_to_dict_catches_enum_attributes(self: "TestModelToDict") -> None:
        """Test model_to_dict() catches enum attributes."""

        class ExampleEnum(Enum):
            VALUE1 = 1
            VALUE2 = 2

        data = FakeModel(data={"enum_value": ExampleEnum.VALUE1})
        result = object_to_dict(data)
        assert result == {
            "data": {
                "enum_value": 1,
            },
        }

    def test_model_to_dict_converts_non_dict_values_to_strings(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() converts non-dict values to strings."""
        data = FakeModel(data={"name": "John", "age": 25})
        result = object_to_dict(data)
        assert result == {
            "data": {
                "name": "John",
                "age": 25,
            },
        }

    def test_model_to_dict_returns_empty_dict_when_input_empty_dict(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() returns an empty dict when input is an empty dict."""
        data = FakeModel(data={})
        result = object_to_dict(data)
        assert result == {
            "data": {},
        }

    def test_model_to_dict_handles_nested_dicts_with_none_values(
        self: "TestModelToDict",
    ) -> None:
        """Test model_to_dict() handles nested dicts with None values."""
        data = FakeModel(data={"nested": {"value1": None}})
        result = object_to_dict(data)
        assert result == {
            "data": {
                "nested": {"value1": None},
            },
        }

    def test_convert_model_to_dict(self: "TestModelToDict") -> None:
        """Test model_to_dict() converts a model to a dict."""
        submodel_instance = SubModel(value=MyEnum.VALUE1)
        my_instance = MyModel(name="John", submodel=submodel_instance)

        result = object_to_dict(my_instance)

        assert result == {"name": "John", "submodel": {"value": "First value"}}

    def test_format_date_true(self: "TestModelToDict") -> None:
        """Test model_to_dict() formats date when format_date=True."""

        class ExampleModel(BaseModel):
            date: datetime = datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London"))

        instance = ExampleModel()
        result = object_to_dict(instance, format_date=True)

        assert result == {
            "date": str(datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London"))),
        }

    def test_format_date_false(self: "TestModelToDict") -> None:
        """Test model_to_dict() does not format date when format_date=False."""

        class ExampleModel(BaseModel):
            date: datetime = datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London"))

        instance = ExampleModel()
        result = object_to_dict(instance, format_date=False)

        assert result == {
            "date": datetime(2022, 1, 1, 0, 0, tzinfo=pytz.timezone("Europe/London")),
        }

    def test_convert_uuid_to_str(self: "TestModelToDict") -> None:
        """Test model_to_dict() converts UUID to str."""

        class ExampleModel(BaseModel):
            uuid_value: UUID = generate_uuid()

        instance = ExampleModel()
        result = object_to_dict(instance)

        assert isinstance(result["uuid_value"], str)
        assert UUID(result["uuid_value"]) == instance.uuid_value

    def test_convert_decimal_to_float(self: "TestModelToDict") -> None:
        """Test model_to_dict() converts Decimal to float."""

        class ExampleModel(BaseModel):
            decimal_value: Decimal = Decimal("3.14")

        instance = ExampleModel()
        result = object_to_dict(instance)

        assert isinstance(result["decimal_value"], float)
        assert result["decimal_value"] == float(instance.decimal_value)

    def test_nested_dict_with_enum_date_uuid_decimal(self: "TestModelToDict") -> None:
        """Test model_to_dict() converts nested dict with enum, date, UUID and Decimal."""

        class NestedModel(BaseModel):
            enum_value: MyEnum
            date_value: datetime
            uuid_value: UUID
            decimal_value: Decimal

        class ExampleModel(BaseModel):
            nested: NestedModel

        instance = ExampleModel(
            nested=NestedModel(
                enum_value=MyEnum.VALUE2,
                date_value=datetime(2022, 1, 1, tzinfo=pytz.timezone("Europe/London")),
                uuid_value=generate_uuid(),
                decimal_value=Decimal("3.14"),
            ),
        )
        result = object_to_dict(instance, format_date=False)

        assert result == {
            "nested": {
                "enum_value": "Second value",
                "date_value": datetime(
                    2022,
                    1,
                    1,
                    tzinfo=pytz.timezone("Europe/London"),
                ),
                "uuid_value": str(instance.nested.uuid_value),
                "decimal_value": float(instance.nested.decimal_value),
            },
        }


def test_space_in_postcode() -> None:
    """Test space_in_postcode() function."""
    # Test case: Valid 5-digit postcode
    assert space_in_postcode("12345") == "12 345"

    # Test case: Valid 6-digit postcode
    assert space_in_postcode("123456") == "123 456"

    # Test case: Valid 7-digit postcode
    assert space_in_postcode("1234567") == "1234 567"

    # Test case: Postcode with leading and trailing spaces
    assert space_in_postcode("  1234567  ") == "1234 567"

    # Test case: Postcode with spaces in the middle
    assert space_in_postcode("12 34567") == "1234 567"

    # Test case: Postcode with no spaces
    assert space_in_postcode("12345678") == "12345678"

    # Test case: Postcode with extra spaces
    assert space_in_postcode("   12   34567   ") == "1234 567"

    # Test case: Postcode with non-digit characters
    assert space_in_postcode("12A4567") == "12A4 567"

    # Test case: Postcode with invalid length (less than 5 digits)
    assert space_in_postcode("123") == "123"

    # Test case: Postcode with invalid length (more than 7 digits)
    assert space_in_postcode("12345678") == "12345678"

    # Test case: Empty string
    assert not space_in_postcode("")
    assert isinstance(space_in_postcode(""), str)

    # Test case: Postcode with only spaces
    assert not space_in_postcode("     ")
    assert isinstance(space_in_postcode("     "), str)


@pytest.mark.parametrize(
    ("street1", "post_code", "building_name", "sub_building", "expected"),
    [
        ("Main Street", "12345", None, None, "Main Street, 12 345"),
        ("Main Street", "12345", "Building A", None, "Building A Main Street, 12 345"),
        ("Main Street", "12345", None, "Suite 101", "Suite 101 Main Street, 12 345"),
        (
            "Main Street",
            "12345",
            "Building A",
            "Suite 101",
            "Suite 101 Building A Main Street, 12 345",
        ),
        ("2nd Avenue", "56789", None, None, "2nd Avenue, 56 789"),
        (
            "2nd Avenue",
            "56789",
            "Office Building",
            None,
            "Office Building 2nd Avenue, 56 789",
        ),
        ("2nd Avenue", "56789", None, "Floor 5", "Floor 5 2nd Avenue, 56 789"),
        (
            "2nd Avenue",
            "56789",
            "Office Building",
            "Floor 5",
            "Floor 5 Office Building 2nd Avenue, 56 789",
        ),
        ("High Street", "00000", None, None, "High Street, 00 000"),
        ("High Street", "00000", "Tower", None, "Tower High Street, 00 000"),
        (
            "High Street",
            "00000",
            None,
            "Apartment 1B",
            "Apartment 1B High Street, 00 000",
        ),
        (
            "High Street",
            "00000",
            "Tower",
            "Apartment 1B",
            "Apartment 1B Tower High Street, 00 000",
        ),
    ],
)
def test_short_address(
    street1: str,
    post_code: str,
    building_name: str,
    sub_building: str,
    expected: str,
) -> None:
    """Test cases for short_address()"""
    assert short_address(street1, post_code, building_name, sub_building) == expected


def test_short_address_with_spaces() -> None:
    """Test cases for fields with leading/trailing spaces"""
    # Test case: Postcode with spaces
    assert (
        short_address("Main Street", "12 345", "Building A", None)
        == "Building A Main Street, 12 345"
    )

    # Test case: Street name with leading/trailing spaces
    assert (
        short_address("  Main Street  ", "12345", None, None) == "Main Street, 12 345"
    )

    # Test case: Building name with leading/trailing spaces
    assert (
        short_address("Main Street", "12345", "  Building A  ", None)
        == "Building A Main Street, 12 345"
    )

    # Test case: Sub-building with leading/trailing spaces
    assert (
        short_address("Main Street", "12345", None, "  Suite 101  ")
        == "Suite 101 Main Street, 12 345"
    )


def test_short_address_with_empty_fields() -> None:
    """Test cases for empty fields"""
    # Test case: Empty building name
    assert short_address("Main Street", "12345", "", None) == "Main Street, 12 345"

    # Test case: Empty sub-building
    assert (
        short_address("Main Street", "12345", "Building A", "")
        == "Building A Main Street, 12 345"
    )

    # Test case: Empty street1
    with pytest.raises(TypeError):
        short_address("", "12345", "Building A", "Suite 101")

    # Test case: Empty post_code
    with pytest.raises(TypeError):
        short_address("Main Street", "", "Building A", "Suite 101")


def test_short_address_with_none_fields() -> None:
    """Test cases for None fields"""
    # Test case: None building name
    assert short_address("Main Street", "12345", None, None) == "Main Street, 12 345"

    # Test case: None sub-building
    assert (
        short_address("Main Street", "12345", "Building A", None)
        == "Building A Main Street, 12 345"
    )

    # Test case: None street1
    with pytest.raises(TypeError):
        short_address(None, "12345", "Building A", "Suite 101")

    # Test case: None post_code
    with pytest.raises(TypeError):
        short_address("Main Street", None, "Building A", "Suite 101")


def test_short_address_with_invalid_postcode() -> None:
    """Test cases for invalid postcode"""
    # Test case: Invalid length postcode
    assert (
        short_address("Main Street", "1234", "Building A", None)
        == "Building A Main Street, 1234"
    )

    # Test case: Postcode with non-digit characters
    assert (
        short_address("Main Street", "12A45", "Building A", None)
        == "Building A Main Street, 12 A45"
    )
