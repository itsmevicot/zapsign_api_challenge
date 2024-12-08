import pytest
from unittest.mock import patch
from rest_framework import status

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer


@pytest.fixture
def authenticated_superuser(db, api_client):
    """
    Fixture to create and authenticate a superuser.
    """
    superuser = Company.objects.create_superuser(
        email="superuser@test.com",
        name="Superuser",
        password="supersecurepassword",
    )
    api_client.force_authenticate(user=superuser)
    return superuser


@pytest.fixture
def authenticated_user(db, api_client):
    """
    Fixture to create and authenticate a regular user.
    """
    user = Company.objects.create_user(
        email="user@test.com",
        name="Regular User",
        password="securepassword",
    )
    api_client.force_authenticate(user=user)
    return user

@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_list_companies(mock_service, api_client, authenticated_superuser):
    """
    Test retrieving a list of companies.
    """
    mock_service.return_value.list_companies.return_value = [
        Company(id=1, email="company1@test.com", name="Company 1", is_active=True),
        Company(id=2, email="company2@test.com", name="Company 2", is_active=False),
    ]

    api_client.force_authenticate(user=authenticated_superuser)
    response = api_client.get("/api/v1/companies/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["email"] == "company1@test.com"
    assert response.data[1]["is_active"] is False


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_create_company(mock_service, api_client, authenticated_superuser):
    """
    Test creating a new company.
    """
    mock_service.return_value.create_company.return_value = Company(
        id=1,
        email="newcompany@test.com",
        name="New Company",
        api_token="123e4567-e89b-12d3-a456-426614174000",
        is_active=True,
    )

    api_client.force_authenticate(user=authenticated_superuser)
    response = api_client.post(
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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == "newcompany@test.com"


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_get_company_details(mock_service, api_client, authenticated_user):
    """
    Test retrieving details of a specific company.
    """
    mock_service.return_value.get_company.return_value = Company(
        id=1,
        email="company1@test.com",
        name="Company 1",
        api_token="123e4567-e89b-12d3-a456-426614174000",
        is_active=True,
    )

    api_client.force_authenticate(user=authenticated_user)
    response = api_client.get("/api/v1/companies/1/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "company1@test.com"


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_update_company(mock_service, api_client, authenticated_user):
    """
    Test updating a company.
    """
    mock_service.return_value.update_company.return_value = Company(
        id=1,
        email="company1@test.com",
        name="Updated Company",
        api_token="123e4567-e89b-12d3-a456-426614174000",
        is_active=False,
    )

    api_client.force_authenticate(user=authenticated_user)
    response = api_client.put(
        "/api/v1/companies/1/",
        {"name": "Updated Company", "is_active": False},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Company"
    assert response.data["is_active"] is False


@pytest.mark.django_db
@patch("apps.companies.views.CompanyService")
def test_delete_company(mock_service, api_client, authenticated_user):
    """
    Test deleting a company.
    """
    mock_service.return_value.delete_company.return_value = None

    api_client.force_authenticate(user=authenticated_user)
    response = api_client.delete("/api/v1/companies/1/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
