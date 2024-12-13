import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def validate():
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in the environment variables")
        if not Config.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in the environment variables")

# Validate configuration on import
Config.validate()
