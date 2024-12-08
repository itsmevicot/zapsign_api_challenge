import pytest
from rest_framework import status
from unittest.mock import patch


@pytest.mark.django_db
def test_list_documents_success(authenticated_user, test_document):
    """
    Test listing documents for a company.
    """
    response = authenticated_user.get("/api/v1/documents/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == test_document.name


@pytest.mark.django_db
@patch("apps.documents.service.ZapSignService.create_document_in_zapsign")
def test_create_document_success(mock_zapsign_service, authenticated_user):
    """
    Test creating a document with mocked ZapSign API call.
    """
    mock_zapsign_service.return_value = {
        "token": "zapsign-token",
        "status": "created",
        "open_id": 12345,
        "created_by": {"email": "creator@example.com"},
        "external_id": "zapsign-external-id",
        "signers": [
            {"token": "signer1-token", "status": "pending"},
            {"token": "signer2-token", "status": "pending"},
        ],
    }

    payload = {
        "name": "New Document",
        "url_pdf": "https://example.com/document.pdf",
        "signers": [
            {"name": "Signer 1", "email": "signer1@example.com"},
            {"name": "Signer 2", "email": "signer2@example.com"},
        ],
    }

    response = authenticated_user.post("/api/v1/documents/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == payload["name"]
    assert response.data["token"] == "zapsign-token"
    assert response.data["status"] == "created"
    assert len(response.data["signers"]) == 2


@pytest.mark.django_db
def test_get_document_success(authenticated_user, test_document):
    """
    Test retrieving a document by ID.
    """
    response = authenticated_user.get(f"/api/v1/documents/{test_document.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == test_document.name


@pytest.mark.django_db
def test_update_document_success(authenticated_user, test_document):
    """
    Test updating a document by ID.
    """
    payload = {"name": "Updated Document"}
    response = authenticated_user.put(
        f"/api/v1/documents/{test_document.id}/", payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == payload["name"]


@pytest.mark.django_db
def test_delete_document_success(authenticated_user, test_document):
    """
    Test deleting a document by ID.
    """
    response = authenticated_user.delete(f"/api/v1/documents/{test_document.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
