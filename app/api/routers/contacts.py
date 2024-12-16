"""
Contact Routers

This module contains routes for managing user contacts.
"""
import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer

from app.api.schemas import ContactCreate, ContactResponse
from app.services.contact_service import ContactService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
DEFAULT_PERIOD = 7  # days

router = APIRouter(prefix="/contacts", tags=["Contacts"],
    dependencies=[Depends(oauth2_scheme)]  # Enforce security globally for all endpoints
)

@router.get("/", response_model=list[ContactResponse])
def read_contacts(
        contact_service: ContactService = Depends()
):
    """Retrieve all contacts for the current user."""
    return contact_service.get_all_contacts()


@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(
    contact_id: int,
        contact_service: ContactService = Depends()
):
    contact = contact_service.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate,
                   contact_service: ContactService = Depends()
):
    return contact_service.create_contact(contact)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreate,
                   contact_service: ContactService = Depends()
):
    updated_contact = contact_service.update_contact(contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, contact_service: ContactService = Depends()):
    deleted = contact_service.delete_contact(contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted"}


@router.get("/search/", response_model=list[ContactResponse])
def search_contacts(
        name: str = Query(None),
        last_name: str = Query(None),
        email: str = Query(None),
        contact_service: ContactService = Depends()
):
    contacts = contact_service.search_contacts(name, last_name, email)
    if not contacts:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return contacts


@router.get("/birthdays/", response_model=list[ContactResponse])
def get_upcoming_birthdays(
        days: int = DEFAULT_PERIOD,
        contact_service: ContactService = Depends()
):
    if days < 1:
        raise HTTPException(status_code=400, detail="Period must be non-negative")
    if days > 365:
        raise HTTPException(status_code=400, detail="Period must be less than a year")
    contacts = contact_service.get_upcoming_birthdays(
        datetime.date.today(), datetime.date.today() + datetime.timedelta(days=days)
    )
    return contacts
