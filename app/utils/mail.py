"""
This module contains functions for sending emails.
The configuration for sending emails is performed using fastapi_mail ConnectionConfig class.
"""
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os

from app.config import Config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_FROM_NAME="Contacts App",
    MAIL_PORT=int(Config.MAIL_PORT),
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=os.path.join(BASE_DIR, "templates")
)


async def send_verification_email(email: EmailStr, token: str, background_tasks: BackgroundTasks):
    """
    Send a verification email to the user.
    Parameters:
        email (EmailStr): The email address of the user.
        token (str): The verification token.
        background_tasks (BackgroundTasks): The background tasks object.
    """
    link = f"{Config.APP_BASE_URL}/auth/verify-email?token={token}"
    message = MessageSchema(
        subject="Welcome! Confirm Your Email",
        recipients=[email],
        template_body={"confirmation_link": link},
        subtype="html",
    )
    fm = FastMail(conf)
    print(f"Sending email to {email} with token {token}")
    background_tasks.add_task(fm.send_message, message, template_name="verification_email.html")
