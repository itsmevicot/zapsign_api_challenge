import pytest
from rest_framework import status


@pytest.mark.django_db
def test_list_signers_success(authenticated_user, test_document, signers):
    """
    Test listing signers for a document owned by the company.
    """
    response = authenticated_user.get(f"/api/v1/signers/document/{test_document.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == signers[0].name
    assert response.data[1]["name"] == signers[1].name


@pytest.mark.django_db
def test_create_signer_success(authenticated_user, test_document):
    """
    Test creating signers for a document owned by the company.
    """
    payload = [
        {"name": "New Signer 1", "email": "new_signer1@example.com"},
        {"name": "New Signer 2", "email": "new_signer2@example.com"},
    ]
    response = authenticated_user.post(
        f"/api/v1/signers/document/{test_document.id}/", payload, format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 2
    assert response.data[0]["name"] == payload[0]["name"]
    assert response.data[1]["email"] == payload[1]["email"]


@pytest.mark.django_db
def test_get_signer_success(authenticated_user, test_signer):
    """
    Test retrieving a signer by ID.
    """
    response = authenticated_user.get(f"/api/v1/signers/{test_signer.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == test_signer.name
    assert response.data["email"] == test_signer.email


@pytest.mark.django_db
def test_update_signer_success(authenticated_user, test_signer):
    """
    Test updating a signer by ID.
    """
    payload = {"name": "Updated Signer", "email": "updated@example.com"}
    response = authenticated_user.put(
        f"/api/v1/signers/{test_signer.id}/", payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == payload["name"]
    assert response.data["email"] == payload["email"]


@pytest.mark.django_db
def test_delete_signer_success(authenticated_user, test_signer):
    """
    Test deleting a signer by ID.
    """
    response = authenticated_user.delete(f"/api/v1/signers/{test_signer.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
