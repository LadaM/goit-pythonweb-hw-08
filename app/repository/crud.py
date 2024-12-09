from sqlalchemy.orm import Session

from app.api.schemas import ContactCreate
from app.repository.models import Contact


def create_contact(db: Session, contact: ContactCreate):
    new_contact = Contact(**contact.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def get_all_contacts(db: Session):
    return db.query(Contact).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, updated_data: ContactCreate):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return None
    for key, value in updated_data.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


def search_contacts(db: Session, name: str = None, last_name: str = None, email: str = None):
    query = db.query(Contact)
    if name:
        query = query.filter(Contact.first_name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()
