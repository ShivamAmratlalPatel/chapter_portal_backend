"""Fake data for testing purposes."""
from secrets import choice
from uuid import UUID

from faker import Faker

from backend.schemas import Address

fake = Faker(locale="en_GB")


def fake_title() -> str:
    """Return a fake title."""
    return fake.prefix()


def fake_first_name() -> str:
    """Return a fake first name."""
    return fake.first_name()


def fake_last_name() -> str:
    """Return a fake last name."""
    return fake.last_name()


def fake_name() -> str:
    """Return a fake name."""
    return fake.name()


def fake_zone() -> str:
    """Return a fake zone."""
    return choice(["North", "South", "London", "Central"])


def fake_email() -> str:
    """Return a fake email address."""
    return fake.free_email()


def fake_phone_number() -> str:
    """Return a fake phone number."""
    return fake.cellphone_number()


def fake_building_name() -> str:
    """Return a fake building name."""
    return fake.building_number()


def fake_post_code() -> str:
    """Return a fake post code."""
    return fake.postcode()


def fake_city() -> str:
    """Return a fake city."""
    return fake.city()


def fake_street1() -> str:
    """Return a fake street1."""
    return fake.street_address()


def fake_county() -> str:
    """Return a fake county."""
    return fake.county()


def fake_sub_building() -> str:
    """Return a fake sub_building."""
    return fake.secondary_address()


def fake_country() -> str:
    """Return a fake country."""
    return fake.country()


def fake_address(required_fields_only: bool) -> Address:
    """
    Return a fake address.

    Args:
        required_fields_only (bool): Whether to return only required fields.

    Returns:
        Address: A fake address.
    """
    address_data = {
        "building_name": fake_building_name(),
        "post_code": fake_post_code(),
        "city": fake_city(),
        "street1": fake_street1(),
    }

    if not required_fields_only:
        address_data.update(
            {
                "county": fake_county(),
                "sub_building": fake_sub_building(),
                "country": fake_country(),
            },
        )

    return Address(**address_data)


def fake_chapter() -> dict:
    """Return a fake chapter."""
    return {
        "name": fake_name(),
        "zone": fake_zone(),
        "email": fake_email(),
    }


def fake_sport_name() -> str:
    """Return a fake sport."""
    return choice(["Football", "Netball", "Cricket", "Kho Kho", "Kabaddi"])


def fake_sport() -> dict:
    """Return a fake sport."""
    return {
        "name": fake_sport_name(),
    }


def fake_team(chapter_id: UUID, sport_id: UUID) -> dict:
    """Return a fake team."""
    return {
        "name": fake_name(),
        "chapter_id": chapter_id,
        "sport_id": sport_id,
    }


def fake_pitch() -> dict:
    """Return a fake pitch."""
    return {
        "name": fake_name(),
    }
