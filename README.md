# goit-pythonweb-hw-08

Тема 8. Домашня робота
Fullstack Web Development with Python course

## Project Structure
```
goit-pythonweb-hw-08/
├── app/
│   ├── __init__.py            
│   ├── db/
│   │   ├── __init__.py         
│   │   ├── database.py         # Database engine and session setup
│   │   ├── models.py           # SQLAlchemy models
│   │   └── crud.py             # CRUD operations for the database
│   ├── api/
│   │   ├── __init__.py         
│   │   ├── main.py             # FastAPI application instance
│   │   ├── routers/
│   │   │   ├── __init__.py     
│   │   │   └── contacts.py     # Contacts-related endpoints
│   │   └── schemas.py          # Pydantic schemas for validation
├── alembic/                    # Alembic migrations directory
│   ├── env.py                  # Alembic configuration file
│   ├── versions/               # Database migration versions
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   └── test_contacts.py        # Tests for the contacts API
├── .env                        # Environment variables (e.g., DB connection string)
├── .gitignore                  # Ignore unnecessary files in Git
├── pyproject.toml              # Poetry dependencies and settings
└── README.md                   # Project documentation
```

## Environment Setup
1. Clone the repository:
    ```
    git clone https://github.com/LadaM/goit-pythonweb-hw-08
    cd goit-pythonweb-hw-08
    ```
2. Install dependencies using Poetry:
   ```poetry install```
3. Create a `.env` file:
   `cp .env.example .env`
4. Update the `.env` file with your PostgreSQL connection details:
    ```
   DATABASE_URL=postgresql://username:password@localhost:5432/contacts_db
    ```