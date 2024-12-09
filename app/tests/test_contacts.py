import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.schemas import ContactCreate
from app.repository import crud
from app.repository.database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_contact():
    return ContactCreate(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        phone="1234567890",
        birthday="1990-01-01",
        additional_info="Test user"
    )


def test_create_contact(db_session, sample_contact):
    contact = crud.create_contact(db_session, sample_contact)
    assert contact.id is not None
    assert contact.first_name == sample_contact.first_name


def test_get_all_contacts(db_session, sample_contact):
    crud.create_contact(db_session, sample_contact)
    contacts = crud.get_all_contacts(db_session)
    assert len(contacts) == 1
    assert contacts[0].first_name == sample_contact.first_name


def test_get_contact_by_id(db_session, sample_contact):
    contact = crud.create_contact(db_session, sample_contact)
    fetched_contact = crud.get_contact_by_id(db_session, contact.id)
    assert fetched_contact is not None
    assert fetched_contact.email == sample_contact.email


def test_update_contact(db_session, sample_contact):
    contact = crud.create_contact(db_session, sample_contact)
    updated_data = ContactCreate(
        first_name="Jane",
        last_name="Doe",
        email="janedoe@example.com",
        phone="0987654321",
        birthday="1992-02-02",
        additional_info="Updated user"
    )
    updated_contact = crud.update_contact(db_session, contact.id, updated_data)
    assert updated_contact.first_name == updated_data.first_name
    assert updated_contact.email == updated_data.email


def test_delete_contact(db_session, sample_contact):
    contact = crud.create_contact(db_session, sample_contact)
    deleted_contact = crud.delete_contact(db_session, contact.id)
    assert deleted_contact is not None
    assert crud.get_contact_by_id(db_session, contact.id) is None
