import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.authentication import get_current_user, get_current_admin_user
from app.repository.models import User, UserRole

# Mocking user service
@pytest.fixture
def mock_user_service():
    service = MagicMock()
    return service

def test_get_current_user_valid_token(mock_user_service):
    mock_user_service.get_user_by_email.return_value = User(
        email="test@example.com", is_verified=True
    )

    with patch("app.services.authentication.verify_access_token", return_value="test@example.com"):
        user = get_current_user(
            token="valid_token",  # Simulating dependency injection for the token
            user_service=mock_user_service
        )

    assert user.email == "test@example.com"
    assert user.is_verified is True

def test_get_current_user_invalid_token(mock_user_service):
    mock_user_service.get_user_by_email.return_value = None

    with patch("app.services.authentication.verify_access_token", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                token="invalid_token",  # Simulating dependency injection for the token
                user_service=mock_user_service
            )

    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in exc_info.value.detail

def test_get_current_user_unverified_user(mock_user_service):
    mock_user_service.get_user_by_email.return_value = User(
        email="test@example.com", is_verified=False
    )

    with patch("app.services.authentication.verify_access_token", return_value="test@example.com"):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(
                token="valid_token",  # Simulating dependency injection for the token
                user_service=mock_user_service
            )

    assert exc_info.value.status_code == 403
    assert "User is not verified" in exc_info.value.detail

def test_get_current_admin_user():
    current_user = User(email="admin@example.com", role=UserRole.ADMIN)

    admin_user = get_current_admin_user(current_user=current_user)

    assert admin_user.role == UserRole.ADMIN

def test_get_current_admin_user_non_admin():
    current_user = User(email="user@example.com", role=UserRole.USER)

    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(current_user=current_user)

    assert exc_info.value.status_code == 403
    assert "Admins only" in exc_info.value.detail
