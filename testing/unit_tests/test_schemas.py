"""Test schemas.py module."""
import pytest
from pydantic import ValidationError

from backend.schemas import Address, Message, validate_phone_number


class TestMessage:
    """Test Message schema."""

    def test_message_schema(self: "TestMessage") -> None:
        """Test is to ensure that the message is valid."""
        message_data = {"message": "Hello, World!"}
        message = Message(**message_data)
        assert message.message == "Hello, World!"

    def test_message_schema_invalid_data(self: "TestMessage") -> None:
        """Test is to ensure that an exception is raised if the data is invalid."""
        message_data = {"message": 123}  # Invalid data type
        with pytest.raises(ValueError, match=r".*"):
            Message(**message_data)


class TestValidatePhoneNumber:
    """Test validate_phone_number() function."""

    def test_valid_phone_number(self: "TestValidatePhoneNumber") -> None:
        """Test is to ensure that the phone number is valid."""
        phone_number = "+1234567890"
        assert validate_phone_number(phone_number) == phone_number

    def test_invalid_phone_number(self: "TestValidatePhoneNumber") -> None:
        """
        Invalid phone number test

        Test is to ensure that an exception is raised if the phone number is
        invalid.
        """
        invalid_numbers = ["1234567890", "+abc123", ""]
        for number in invalid_numbers:
            with pytest.raises(ValueError, match=r".*"):
                validate_phone_number(number)

    def test_invalid_phone_number_exception_message(
        self: "TestValidatePhoneNumber",
    ) -> None:
        """Test is to ensure that the exception message is correct."""
        invalid_number = "1234567890"
        expected_msg = "Phone Number Invalid."
        with pytest.raises(ValueError, match=r".*") as exc_info:
            validate_phone_number(invalid_number)
        assert str(exc_info.value) == expected_msg

    def test_none_phone_number(self: "TestValidatePhoneNumber") -> None:
        """Test is to ensure that None is returned if the phone number is None."""
        assert validate_phone_number(None) is None

    def test_case_insensitive(self: "TestValidatePhoneNumber") -> None:
        """Test is to ensure that the phone number is case insensitive."""
        phone_number = "+aBcDeFgHiJ"
        expected_msg = "Phone Number Invalid."
        with pytest.raises(ValueError, match=r".*") as exc_info:
            validate_phone_number(phone_number)
        assert str(exc_info.value) == expected_msg

    def test_whitespace_phone_number(self: "TestValidatePhoneNumber") -> None:
        """Test is to ensure that the phone number is stripped of whitespace."""
        phone_number = "+12 3 45 67890"
        assert validate_phone_number(phone_number) == "+1234567890"

    def test_numeric_phone_number(self: "TestValidatePhoneNumber") -> None:
        """Test is to ensure that the phone number is not converted to a numeric value."""
        phone_number = "+123456789+441234567890"
        expected_msg = "Phone Number Invalid."
        with pytest.raises(ValueError, match=r".*") as exc_info:
            validate_phone_number(phone_number)
        assert str(exc_info.value) == expected_msg


class TestAddress:
    """Test Address schema."""

    def test_valid_address(self: "TestAddress") -> None:
        """Test that a valid Address instance can be created without any errors."""
        address_data = {
            "county": "Test County",
            "building_name": "Test Building",
            "post_code": "TE1 1ST",
            "city": "Test City",
            "street1": "123 Test Street",
            "sub_building": "Test Sub Building",
            "country": "Test Country",
        }
        address = Address(**address_data)
        assert address.county == "Test County"
        assert address.building_name == "Test Building"
        assert address.post_code == "TE11ST"
        assert address.city == "Test City"
        assert address.street1 == "123 Test Street"
        assert address.sub_building == "Test Sub Building"
        assert address.country == "Test Country"

    def test_optional_attributes(self: "TestAddress") -> None:
        """Test that creating an Address instance with optional attributes missing is allowed."""
        address_data = {
            "building_name": "Test Building",
            "post_code": "TE1 1ST",
            "city": "Test City",
            "street1": "123 Test Street",
        }
        address = Address(**address_data)
        assert address.county is None
        assert address.sub_building is None
        assert address.country is None

    def test_invalid_post_code(self: "TestAddress") -> None:
        """Test that an invalid postal code raises a validation error."""
        address_data = {
            "building_name": "Test Building",
            "post_code": "TE1-1ST",
            "city": "Test City",
            "street1": "123 Test Street",
        }
        with pytest.raises(ValidationError) as e:
            Address(**address_data)
        assert "Postal code must contain only alphanumeric characters." in str(e.value)

    def test_missing_required_attributes(self: "TestAddress") -> None:
        """Test that creating an Address instance without required attributes raises a validation error."""
        with pytest.raises(ValidationError):
            Address()

    def test_post_code_validation(self: "TestAddress") -> None:
        """Test that the validate_post_code function works as expected."""
        assert Address.validate_post_code("TE1 1ST") == "TE11ST"
        with pytest.raises(ValueError, match=r".*"):
            Address.validate_post_code("Invalid-Post Code")

    def test_address_serialization(self: "TestAddress") -> None:
        """Test serialization of the Address instance to a dictionary."""
        address_data = {
            "county": "Test County",
            "building_name": "Test Building",
            "post_code": "TE1 1ST",
            "city": "Test City",
            "street1": "123 Test Street",
            "sub_building": "Test Sub Building",
            "country": "Test Country",
        }
        address = Address(**address_data)
        serialized_address = address.model_dump()
        address_data["post_code"] = "TE11ST"
        assert serialized_address == address_data

    def test_address_deserialization(self: "TestAddress") -> None:
        """Test deserialization of a dictionary to an Address instance."""
        address_data = {
            "county": "Test County",
            "building_name": "Test Building",
            "post_code": "TE1 1ST",
            "city": "Test City",
            "street1": "123 Test Street",
            "sub_building": "Test Sub Building",
            "country": "Test Country",
        }
        address = Address.model_validate(address_data)
        assert address.county == "Test County"
        assert address.building_name == "Test Building"
        assert address.post_code == "TE11ST"
        assert address.city == "Test City"
        assert address.street1 == "123 Test Street"
        assert address.sub_building == "Test Sub Building"
        assert address.country == "Test Country"
