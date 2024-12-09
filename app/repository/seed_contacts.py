from sqlalchemy.orm import Session
from faker import Faker
from app.repository.database import SessionLocal
from app.repository.models import Contact

fake = Faker()

def seed_data(db: Session, num_records: int = 10):
    if db.query(Contact).count() > 0:
        print("Contacts table is not empty. Skipping seed data.")
        return

    for _ in range(num_records):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
            additional_info=fake.sentence()
        )
        db.add(contact)
    db.commit()
    print(f"Added {num_records} contacts into the database.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db, num_records=20)
    finally:
        db.close()
