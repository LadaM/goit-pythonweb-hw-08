import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Application URL
    APP_BASE_URL = os.getenv("APP_BASE_URL")

    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Mail Configuration
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    @staticmethod
    def validate():
        # Validate database config
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in the environment variables")
        if not Config.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in the environment variables")

        # Validate mail config
        if not Config.MAIL_USERNAME:
            raise ValueError("MAIL_USERNAME is not set in the environment variables")
        if not Config.MAIL_PASSWORD:
            raise ValueError("MAIL_PASSWORD is not set in the environment variables")
        if not Config.MAIL_FROM:
            raise ValueError("MAIL_FROM is not set in the environment variables")
        if not Config.MAIL_PORT:
            raise ValueError("MAIL_PORT is not set in the environment variables")
        if not Config.MAIL_SERVER:
            raise ValueError("MAIL_SERVER is not set in the environment variables")

        # Validate application URL
        if not Config.APP_BASE_URL:
            raise ValueError("APP_BASE_URL is not set in the environment variables")

# Validate configuration on import
Config.validate()
