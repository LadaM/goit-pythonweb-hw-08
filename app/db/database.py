from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config

engine = create_engine(Config.DATABASE_URL)

# Configure the session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
