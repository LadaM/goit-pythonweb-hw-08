from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from fastapi import BackgroundTasks

from app.repository.models import User
from app.services.user_service import UserService


# Mocking dependencies
@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.mark.asyncio
async def test_get_user_by_email(mock_db_session):
    mock_user = User(id=1, email="test@example.com", is_verified=True)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    service = UserService(db=mock_db_session)

    user = service.get_user_by_email(email="test@example.com")

    mock_db_session.query.assert_called_once()
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_user(mock_db_session):
    service = UserService(db=mock_db_session)

    user = service.create_user(email="newuser@example.com", password="password123")

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(user)
    assert user.email == "newuser@example.com"
    assert user.hashed_password is not None


@pytest.mark.asyncio
async def test_create_user_with_verification(mock_db_session):
    mock_background_tasks = MagicMock(spec=BackgroundTasks)
    service = UserService(db=mock_db_session)

    with patch("app.services.user_service.create_email_verification_token", return_value="token123") as mock_token, \
            patch("app.utils.mail.send_verification_email", new_callable=AsyncMock):
        user = await service.create_user_with_verification(
            email="test@example.com", password="password123", background_tasks=mock_background_tasks
        )

        mock_token.assert_called_once_with("test@example.com")
        mock_db_session.commit.assert_called()
        assert user.email == "test@example.com"
        assert user.verification_token == "token123"


@pytest.mark.asyncio
async def test_resend_verification_email(mock_db_session):
    mock_user = User(email="test@example.com", verification_token=None)
    mock_background_tasks = MagicMock(spec=BackgroundTasks)
    service = UserService(db=mock_db_session)

    with patch("app.services.user_service.create_email_verification_token", return_value="token456") as mock_token, \
            patch("app.utils.mail.send_verification_email", new_callable=AsyncMock):
        await service.resend_verification_email(user=mock_user, background_tasks=mock_background_tasks)

        mock_token.assert_called_once_with("test@example.com")
        mock_db_session.commit.assert_called()
        assert mock_user.verification_token == "token456"


@pytest.mark.asyncio
async def test_verify_password(mock_db_session):
    service = UserService(db=mock_db_session)
    plain_password = "password123"
    hashed_password = service.create_user("test@example.com", plain_password).hashed_password

    result = service.verify_password(plain_password, hashed_password)

    assert result is True
