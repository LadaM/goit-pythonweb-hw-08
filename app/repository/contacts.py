from datetime import date

from sqlalchemy.orm import Session

from app.api.schemas import ContactCreate
from app.repository.models import Contact, User


def get_all_contacts(db: Session, user: User):
    return get_contacts_for_user(db, user)


def get_contact_by_id(db: Session, contact_id: int, user: User):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()


def create_contact(db: Session, contact: ContactCreate, user: User):
    new_contact = Contact(**contact.model_dump(), owner_id=user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def update_contact(db: Session, contact_id: int, updated_data: ContactCreate, user: User):
    contact = get_contact_by_id(db, contact_id, user)
    if not contact:
        return None
    for key, value in updated_data.model_dump().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int, user: User):
    contact = get_contact_by_id(db, contact_id, user)
    if not contact:
        return False
    db.delete(contact)
    db.commit()
    return True


def search_contacts(
        db: Session,
        user: User,
        name: str = None,
        last_name: str = None,
        email: str = None
):
    query = get_contacts_for_user(db, user)
    if name:
        query = query.filter(Contact.first_name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


def get_upcoming_birthdays(db: Session, user: User, start_date: date, end_date: date):
    upcoming_birthdays = []

    # Get only the user's contacts
    contacts = get_contacts_for_user(db, user)
    for contact in contacts:
        this_year_birthday = date(start_date.year, contact.birthday.month, contact.birthday.day)

        if this_year_birthday < start_date:
            this_year_birthday = date(start_date.year + 1, contact.birthday.month, contact.birthday.day)

        if start_date <= this_year_birthday <= end_date:
            upcoming_birthdays.append(contact)

    return upcoming_birthdays

# common method for getting contacts of the user
def get_contacts_for_user(db, user):
    return db.query(Contact).filter(Contact.owner_id == user.id).all()
