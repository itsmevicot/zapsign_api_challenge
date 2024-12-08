import uuid
from unittest.mock import patch

import pytest
from rest_framework import status

from utils.exceptions import (
    UnauthorizedCompanyAccessException,
)


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_list_companies_as_superuser(mock_service, authenticated_superuser):
    """
    Test retrieving a list of companies as a superuser.
    """
    mock_service.return_value.list_companies.return_value = [
        {
            "id": 1,
            "email": "company1@test.com",
            "name": "Company 1",
            "api_token": str(uuid.uuid4()),
            "is_active": True,
            "created_at": "2024-12-07T12:00:00Z",
            "last_update_at": "2024-12-08T12:00:00Z",
        },
        {
            "id": 2,
            "email": "company2@test.com",
            "name": "Company 2",
            "api_token": str(uuid.uuid4()),
            "is_active": False,
            "created_at": "2024-12-06T12:00:00Z",
            "last_update_at": "2024-12-07T12:00:00Z",
        },
    ]

    response = authenticated_superuser.get("/api/v1/companies/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["email"] == "company1@test.com"
    assert response.data[1]["is_active"] is False


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_list_companies_as_regular_user(mock_service, authenticated_user):
    """
    Test retrieving a list of companies as a regular user.
    """
    response = authenticated_user.get("/api/v1/companies/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_create_company_not_allowed(mock_service, authenticated_superuser):
    """
    Test attempting to create a company (not implemented).
    """
    response = authenticated_superuser.post(
        "/api/v1/companies/",
        {
            "email": "newcompany@test.com",
            "name": "New Company",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "api_token": "123e4567-e89b-12d3-a456-426614174000",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_get_company_details(mock_service, authenticated_user):
    """
    Test retrieving details of a company.
    """
    mock_service.return_value.get_company.return_value = {
        "id": 1,
        "email": "company1@test.com",
        "name": "Company 1",
        "api_token": "123e4567-e89b-12d3-a456-426614174000",
        "is_active": True,
    }

    response = authenticated_user.get("/api/v1/companies/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "company1@test.com"


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_get_company_details_unauthorized(mock_service, authenticated_user):
    """
    Test retrieving details of a company the user does not have access to.
    """
    exception = mock_service.return_value.get_company.side_effect = UnauthorizedCompanyAccessException()

    response = authenticated_user.get("/api/v1/companies/1/")
    assert response.status_code == exception.status_code

    assert "error" in response.data
    assert response.data["error"]["title"] == exception.title
    assert response.data["error"]["message"] == exception.message


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_delete_company_as_superuser(mock_service, authenticated_superuser):
    """
    Test deleting a company as a superuser.
    """
    mock_service.return_value.delete_company.return_value = None

    response = authenticated_superuser.delete("/api/v1/companies/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_delete_company_as_regular_user(mock_service, authenticated_user):
    """
    Test attempting to delete a company as a regular user.
    """
    response = authenticated_user.delete("/api/v1/companies/1/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
