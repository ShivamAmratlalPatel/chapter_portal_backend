"""Test event models."""
from sqlalchemy.orm import Session

from backend.events.event_models import ChapterEventAssociation, Event, EventType
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.setup.save_testing_chapter import save_testing_chapter


def test_event_type_creation(session: Session) -> None:
    """
    Test creating an event type.

    Args:
        session (Session): Database session

    Returns:
        None

    """
    # Create an event type
    event_type = EventType(
        name="Conference",
    )
    session.add(event_type)
    session.commit()

    # Retrieve the event type
    retrieved_event_type = session.query(EventType).filter_by(name="Conference").first()

    # Check if the retrieved event type matches the created one
    assert retrieved_event_type is not None
    assert retrieved_event_type.name == "Conference"


def test_event_creation(session: Session) -> None:
    """
    Test creating an event.

    Args:
        session (Session): Database session

    Returns:
        None

    """
    # Create an event type
    event_type = EventType(
        name="Workshop",
    )
    session.add(event_type)
    session.commit()

    # Create an event associated with the event type
    event = Event(
        name="Python Workshop",
        event_type_id=event_type.id,
    )
    session.add(event)
    session.commit()

    # Retrieve the event
    retrieved_event = session.query(Event).filter_by(name="Python Workshop").first()

    # Check if the retrieved event matches the created one
    assert retrieved_event is not None
    assert retrieved_event.name == "Python Workshop"
    assert retrieved_event.event_type_id == event_type.id


def test_chapter_event_association(session: Session) -> None:
    """
    Test creating a chapter event association.

    Args:
        session (Session): Database session

    Returns:
        None

    """
    # Create an event type
    event_type = EventType(
        name="Seminar",
    )
    session.add(event_type)
    session.commit()

    # Create an event associated with the event type
    event = Event(
        name="AI Seminar",
        event_type_id=event_type.id,
    )
    session.add(event)
    session.commit()

    chapter = save_testing_chapter(session)

    # Create a chapter event association
    chapter_event_association = ChapterEventAssociation(
        chapter_id=chapter.id,
        event_id=event.id,
    )
    session.add(chapter_event_association)
    session.commit()

    # Retrieve the chapter event association
    retrieved_association = session.query(ChapterEventAssociation).first()

    # Check if the retrieved association matches the created one
    assert retrieved_association is not None
    assert retrieved_association.chapter_id == chapter.id
    assert retrieved_association.event_id == event.id
