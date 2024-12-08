import pytest
from unittest.mock import patch
from rest_framework import status

from apps.companies.models import Company
from apps.documents.models import Document
from apps.signers.models import Signer
from rest_framework.test import APIClient


@pytest.fixture
def test_company(db):
    """
    Fixture to create a test company.
    """
    return Company.objects.create(
        email="test@company.com",
        name="Test Company",
        api_token="123e4567-e89b-12d3-a456-426614174000"
    )


@pytest.fixture
def test_document(db, test_company):
    """
    Fixture to create a test document.
    """
    return Document.objects.create(
        name="Test Document",
        company=test_company
    )


@pytest.fixture
def test_signer(db, test_document):
    """
    Fixture to create a test signer.
    """
    return Signer.objects.create(
        token="123e4567-e89b-12d3-a456-426614174000",
        status="pending",
        name="Test Signer",
        email="test@signer.com",
        document=test_document
    )


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


@pytest.mark.django_db
@patch("apps.signers.views.SignerService")
def test_list_signers(mock_service, authenticated_api_client, test_document):
    """
    Test retrieving a list of signers for a document.
    """
    mock_service.return_value.list_signers.return_value = [
        Signer(id=1, name="Signer 1", email="signer1@test.com", status="pending", document=test_document),
        Signer(id=2, name="Signer 2", email="signer2@test.com", status="completed", document=test_document),
    ]

    response = authenticated_api_client.get(f"/api/v1/signers/?document_id={test_document.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Signer 1"
    assert response.data[1]["status"] == "completed"


@pytest.mark.django_db
@patch("apps.signers.views.SignerService")
def test_create_signer(mock_service, authenticated_api_client, test_document):
    """
    Test creating a new signer for a document.
    """
    mock_service.return_value.create_signer.return_value = Signer(
        id=1,
        token="123e4567-e89b-12d3-a456-426614174000",
        status="pending",
        name="New Signer",
        email="new@signer.com",
        document=test_document
    )

    response = authenticated_api_client.post(
        f"/api/v1/signers/?document_id={test_document.id}",
        {
            "token": "123e4567-e89b-12d3-a456-426614174000",
            "status": "pending",
            "name": "New Signer",
            "email": "new@signer.com"
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "New Signer"
    assert response.data["email"] == "new@signer.com"


@pytest.mark.django_db
@patch("apps.signers.views.SignerService")
def test_get_signer_details(mock_service, authenticated_api_client, test_document, test_signer):
    """
    Test retrieving details of a specific signer.
    """
    mock_service.return_value.get_signer.return_value = test_signer

    response = authenticated_api_client.get(f"/api/v1/signers/{test_signer.id}/?document_id={test_document.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == test_signer.name
    assert response.data["email"] == test_signer.email


@pytest.mark.django_db
@patch("apps.signers.views.SignerService")
def test_update_signer(mock_service, authenticated_api_client, test_document, test_signer):
    """
    Test updating a signer for a document.
    """
    updated_data = {
        "name": "Updated Signer",
        "email": "updated@signer.com",
        "status": "completed",
    }
    mock_service.return_value.update_signer.return_value = Signer(
        id=test_signer.id,
        token=test_signer.token,
        document=test_document,
        **updated_data
    )

    response = authenticated_api_client.put(
        f"/api/v1/signers/{test_signer.id}/?document_id={test_document.id}",
        updated_data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Signer"
    assert response.data["status"] == "completed"


@pytest.mark.django_db
@patch("apps.signers.views.SignerService")
def test_delete_signer(mock_service, authenticated_api_client, test_document, test_signer):
    """
    Test deleting a signer for a document.
    """
    mock_service.return_value.delete_signer.return_value = None

    response = authenticated_api_client.delete(f"/api/v1/signers/{test_signer.id}/?document_id={test_document.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
