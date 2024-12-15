# goit-pythonweb-hw-12

Тема 12. Домашня робота
Fullstack Web Development with Python course

## Project Structure
```
goit-pythonweb-hw-08/
├── alembic/                    
│   ├── env.py                  # Alembic configuration file
│   ├── versions/               # Database migration versions
├── app/
│   ├── repository/
│   │   ├── __init__.py         
│   │   ├── database.py         # Database engine and session setup
│   │   ├── models.py           # SQLAlchemy models
│   │   └── seed_contacts.py    # run for adding a few contacts to the database
│   ├── api/
│   │   ├── __init__.py         
│   │   ├── routers/
│   │   │   ├── __init__.py     
│   │   │   └── contacts.py     # Contacts-related endpoints
│   │   └── schemas.py          # Pydantic schemas for validation
|   ├── tests/                      
│   │   ├── __init__.py
│   │   └── test_db_connection.py   # Test database connection         
│   ├── config.py                   # Project configuration (loading environment variables)
│   └── main.py             # FastAPI application instance
├── .env                        # Environment variables (e.g., DB connection string)
├── alembic.ini                 # Alembic configuration file
├── docker-compose.yml          
├── dockerfile             
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
5. To ensure that the database is set up correctly, the table `contacts` should be created. This project uses Alembic to manage database schema migrations. You must apply migrations to create the required tables, including the contacts table.
To apply migrations, run the following command:
   `alembic upgrade head`

## Running the Application
To run the application, run the following command:
   `poetry run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000`

## API Documentation
The documentation of the API is available at http://localhost:8000/docs
![img.png](img.png)

## Running the Application in Docker
Run the following command to build the Docker images:
`docker-compose build`

To run the application in Docker, use the following command:
`docker-compose up`