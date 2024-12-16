"""
Database Models.

This module contains SQLAlchemy models for the database, including `User` and `Contact`.
"""
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.repository.database import Base


class UserRole(PyEnum):
    """
    Enumeration for user roles.

    Attributes:
        USER: Regular user role.
        ADMIN: Administrator role.
    """
    USER = "user"
    ADMIN = "admin"

class User(Base):
    """
    User model for the application.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): Email address of the user.
        hashed_password (str): Encrypted password of the user.
        role (UserRole): Role of the user (user or admin).
        avatar (str): Path to the user's avatar image.
        is_active (bool): Indicates if the user account is active.
        is_verified (bool): Indicates if the user's email is verified.
        verification_token (str): Token used for email verification.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    avatar = Column(String, nullable=True)  # Path to avatar image
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="owner")


class Contact(Base):
    """
    Contact model for storing user contacts.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone (str): Phone number of the contact.
        birthday (date): Birthday of the contact.
        additional_info (str): Any additional information about the contact.
        owner_id (int): Foreign key referencing the user's ID.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to the User table

    owner = relationship("User", back_populates="contacts")
