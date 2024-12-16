"""
Contact Service.

This module contains the `ContactService` class, which provides functionality for managing user contacts.
"""
from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.schemas import ContactCreate
from app.repository.database import get_db
from app.repository.models import Contact, User
# we import get_current_user here because all contacts are meant to be fetched for the current user
from app.services.authentication import get_current_user


class ContactService:
    """
    A service class for managing contacts.

    Attributes:
        db (Session): Database session for queries.
        user (User): Currently authenticated user.
    """
    def __init__(self, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        self.db = db
        self.user = user

    def get_all_contacts(self):
        """
        Retrieve all contacts for the current user.

        Returns:
            List[Contact]: List of all contacts.
        """
        return self._get_contacts_for_user()

    def get_contact_by_id(self, contact_id: int):
        return self.db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.owner_id == self.user.id
        ).first()

    def create_contact(self, contact_data: ContactCreate):
        new_contact = Contact(**contact_data.model_dump(), owner_id=self.user.id)
        self.db.add(new_contact)
        self.db.commit()
        self.db.refresh(new_contact)
        return new_contact

    def update_contact(self, contact_id: int, updated_data: ContactCreate):
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return None
        for key, value in updated_data.model_dump().items():
            setattr(contact, key, value)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete_contact(self, contact_id: int):
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return False
        self.db.delete(contact)
        self.db.commit()
        return True

    def search_contacts(self, name: str = None, last_name: str = None, email: str = None):
        query = self._get_contacts_for_user()
        if name:
            query = query.filter(Contact.first_name.ilike(f"%{name}%"))
        if last_name:
            query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.filter(Contact.email.ilike(f"%{email}%"))
        return query.all()

    def get_upcoming_birthdays(self, start_date: date, end_date: date):
        upcoming_birthdays = []
        contacts = self._get_contacts_for_user()
        for contact in contacts:
            this_year_birthday = date(start_date.year, contact.birthday.month, contact.birthday.day)
            if this_year_birthday < start_date:
                this_year_birthday = date(start_date.year + 1, contact.birthday.month, contact.birthday.day)
            if start_date <= this_year_birthday <= end_date:
                upcoming_birthdays.append(contact)
        return upcoming_birthdays

    def _get_contacts_for_user(self):
        return self.db.query(Contact).filter(Contact.owner_id == self.user.id)
