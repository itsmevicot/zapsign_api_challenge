import pytest
from unittest.mock import patch
from rest_framework import status

from apps.authentication.serializers import TokenResponseSerializer
from utils.exceptions import (
    InvalidCredentialsException,
    CompanyAlreadyExistsException,
    MissingRefreshTokenException,
    FailedToBlacklistTokenException,
)


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_login_success(mock_auth_service, api_client):
    mock_auth_service.return_value.login.return_value = {
        "refresh": "test_refresh_token",
        "access": "test_access_token",
    }

    response = api_client.post(
        "/api/v1/auth/login/",
        {"email": "test@company.com", "password": "securepassword"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert TokenResponseSerializer(data=response.data).is_valid()


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_login_invalid_credentials(mock_auth_service, api_client):
    mock_auth_service.return_value.login.side_effect = InvalidCredentialsException()

    response = api_client.post(
        "/api/v1/auth/login/",
        {"email": "nonexistent@company.com", "password": "wrongpassword"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["title"] == "Invalid Credentials"
    assert response.data["error"]["message"] == "The provided email or password is incorrect."


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_register_success(mock_auth_service, api_client):
    mock_auth_service.return_value.register.return_value = {
        "id": 1,
        "email": "new@company.com",
        "name": "New Company",
        "api_token": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": "2024-08-12T12:00:00Z",
    }

    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "new@company.com",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "name": "New Company",
            "api_token": "123e4567-e89b-12d3-a456-426614174000",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == "new@company.com"


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_register_existing_email(mock_auth_service, api_client):
    mock_auth_service.return_value.register.side_effect = CompanyAlreadyExistsException(
        email="test@company.com"
    )

    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "test@company.com",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "name": "Duplicate Company",
            "api_token": "123e4567-e89b-12d3-a456-426614174000",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data["error"]["title"] == "Company Already Exists"
    assert response.data["error"]["message"] == "A company with the email 'test@company.com' already exists."


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_logout_success(mock_auth_service, api_client):
    response = api_client.post(
        "/api/v1/auth/logout/",
        {"refresh": "valid_refresh_token"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Logout successful."


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_logout_missing_token(mock_auth_service, api_client):
    mock_auth_service.return_value.logout.side_effect = MissingRefreshTokenException()

    response = api_client.post(
        "/api/v1/auth/logout/",
        {},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["title"] == "Refresh Token Missing"
    assert response.data["error"]["message"] == "The refresh token is required but was not provided."


@pytest.mark.django_db
@patch("apps.authentication.views.AuthenticationService")
def test_logout_blacklist_failure(mock_auth_service, api_client):
    mock_auth_service.return_value.logout.side_effect = FailedToBlacklistTokenException(
        reason="Token invalid."
    )

    response = api_client.post(
        "/api/v1/auth/logout/",
        {"refresh": "invalid_refresh_token"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["title"] == "Failed to Blacklist Token"
    assert response.data["error"]["message"] == "An error occurred while blacklisting the refresh token: Token invalid."