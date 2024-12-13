import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas import ContactCreate, ContactResponse
from app.repository import crud
from app.repository.database import get_db
from app.services.user_service import get_current_user

# only logged-in users can access contacts
router = APIRouter(dependencies=[Depends(get_current_user)])
DEFAULT_PERIOD = 7 # days

@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate,
                   db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@router.get("/", response_model=list[ContactResponse])
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_all_contacts(db)

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted"}


@router.get("/search/", response_model=list[ContactResponse])
def search_contacts(
        name: str = Query(None),
        last_name: str = Query(None),
        email: str = Query(None),
        db: Session = Depends(get_db)
):
    contacts = crud.search_contacts(db, name, last_name, email)
    if not contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts


@router.get("/birthdays/", response_model=list[ContactResponse])
def get_upcoming_birthdays(days: int = DEFAULT_PERIOD, db: Session = Depends(get_db)):
    if days < 1:
        raise HTTPException(status_code=400, detail="Period must be non-negative")
    if days > 365:
        raise HTTPException(status_code=400, detail="Period must be less than a year")
    contacts = crud.get_upcoming_birthdays(db, datetime.date.today(), datetime.date.today() + datetime.timedelta(days=days))
    return contacts
