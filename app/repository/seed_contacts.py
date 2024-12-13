from faker import Faker
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repository.database import SessionLocal
from app.repository.models import Contact, User

fake = Faker()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__use_builtin=True
)


def seed_users(db: Session, num_users: int = 5):
    """
    Seed the database with fake users.
    """
    if db.query(User).count() > 0:
        print("Users table is not empty. Skipping user seeding.")
        return

    user_ids = []
    for _ in range(num_users):
        email = fake.unique.email()
        hashed_password = pwd_context.hash("password")
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_ids.append(user.id)

    print(f"Added {num_users} users into the database.")
    return user_ids


def seed_contacts(db: Session, user_ids: list[int], num_records: int = 10):
    """
    Seed the database with fake contacts associated with users.
    """
    if db.query(Contact).count() > 0:
        print("Contacts table is not empty. Skipping contact seeding.")
        return

    for _ in range(num_records):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
            additional_info=fake.sentence(),
            owner_id=fake.random_element(user_ids)  # Associate with a random user
        )
        db.add(contact)
    db.commit()
    print(f"Added {num_records} contacts into the database.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        # seed users first
        user_ids = seed_users(db, num_users=5)
        # seed contacts associated with those users
        seed_contacts(db, user_ids, num_records=20)
    finally:
        db.close()
