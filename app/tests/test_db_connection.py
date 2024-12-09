from sqlalchemy import inspect
from app.db.database import engine

def test_connection():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if tables:
            print(f"Connection successful! Tables in the database: {tables}")
        else:
            print("Connection successful, but no tables found in the database.")
    except Exception as e:
        print(f"Failed to connect to the database. Error: {e}")

if __name__ == "__main__":
    test_connection()
