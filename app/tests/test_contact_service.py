from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from app.api.schemas import ContactCreate
from app.repository.models import Contact, User
from app.services.contact_service import ContactService


# Mocking dependencies - db_session, current_user
@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def mock_current_user():
    return User(id=1, email="test@example.com", is_verified=True)


def test_get_all_contacts(mock_db_session, mock_current_user):
    mock_db_session.query.return_value.filter.return_value = [
        Contact(id=1, first_name="John", last_name="Doe", owner_id=1),
        Contact(id=2, first_name="Jane", last_name="Smith", owner_id=1),
    ]

    service = ContactService(db=mock_db_session, user=mock_current_user)

    contacts = service.get_all_contacts()

    assert len(contacts) == 2
    assert contacts[0].first_name == "John"
    assert contacts[1].first_name == "Jane"


def test_create_contact(mock_db_session, mock_current_user):
    mock_contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        birthday=date(1990, 1, 1),
        phone="123456789",
        additional_info="Friend from school"
    )

    service = ContactService(db=mock_db_session, user=mock_current_user)

    new_contact = service.create_contact(contact_data=mock_contact_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert new_contact.first_name == "John"
    assert new_contact.owner_id == mock_current_user.id


def test_delete_contact(mock_db_session, mock_current_user):
    mock_contact = Contact(id=1, first_name="John", owner_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_contact

    service = ContactService(db=mock_db_session, user=mock_current_user)

    result = service.delete_contact(contact_id=1)

    mock_db_session.delete.assert_called_once_with(mock_contact)
    mock_db_session.commit.assert_called_once()
    assert result is True


def test_delete_contact_not_found(mock_db_session, mock_current_user):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    service = ContactService(db=mock_db_session, user=mock_current_user)

    result = service.delete_contact(contact_id=999)

    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()
    assert result is False


def test_get_contacts_for_user(mock_db_session, mock_current_user):
    mock_db_session.query.return_value.filter.return_value = [
        Contact(id=1, first_name="John", last_name="Doe", owner_id=1),
        Contact(id=2, first_name="Jane", last_name="Smith", owner_id=1),
    ]

    service = ContactService(db=mock_db_session, user=mock_current_user)

    contacts = service._get_contacts_for_user()

    mock_db_session.query.assert_called_once_with(Contact)
    assert mock_db_session.query.return_value.filter.call_count == 1
    assert len(contacts) == 2
    assert contacts[0].first_name == "John"
    assert contacts[1].first_name == "Jane"


def test_get_upcoming_birthdays(mock_db_session, mock_current_user):
    today = date.today()
    upcoming_birthday = today + timedelta(days=5)
    contacts = [
        Contact(id=1, first_name="John", last_name="Doe", birthday=upcoming_birthday, owner_id=1),
        Contact(id=2, first_name="Jane", last_name="Smith", birthday=today + timedelta(days=15), owner_id=1),
    ]
    mock_db_session.query.return_value.filter.return_value = contacts

    service = ContactService(db=mock_db_session, user=mock_current_user)

    start_date = today
    end_date = today + timedelta(days=10)
    birthdays = service.get_upcoming_birthdays(start_date=start_date, end_date=end_date)

    assert len(birthdays) == 1
    assert birthdays[0].first_name == "John"
