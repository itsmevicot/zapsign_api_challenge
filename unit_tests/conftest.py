import pytest
from rest_framework.test import APIClient
from apps.companies.models import Company
from apps.documents.models import Document
from apps.signers.models import Signer


@pytest.fixture
def api_client():
    """
    Provides a default unauthenticated API client.
    """
    return APIClient()


@pytest.fixture
def mocked_authentication_service(mocker):
    """
    Mocks the AuthenticationService.
    """
    return mocker.patch("apps.authentication.service.AuthenticationService", autospec=True)


@pytest.fixture
def authenticated_user(db):
    """
    Provides an authenticated API client for a test company.
    Creates the company if it doesn't already exist.
    """
    company = Company.objects.create_user(
        email="test@company.com",
        password="securepassword",
        name="Test Company",
        api_token="123e4567-e89b-12d3-a456-426614174000",
        is_active=True,
    )
    client = APIClient()
    client.force_authenticate(user=company)
    return client


@pytest.fixture
def authenticated_superuser(db):
    """
    Provides an authenticated API client for a superuser.
    Creates the superuser if it doesn't already exist.
    """
    superuser = Company.objects.create_superuser(
        email="superuser@test.com",
        password="securepassword",
        name="Superuser Company",
        api_token="123e4567-e89b-12d3-a456-426614174000",
        is_active=True,
    )
    client = APIClient()
    client.force_authenticate(user=superuser)
    return client


@pytest.fixture
def test_company(db):
    """
    Creates and returns a test company.
    """
    return Company.objects.create(
        email="test@company.com",
        name="Test Company",
        api_token="123e4567-e89b-12d3-a456-426614174000",
    )


@pytest.fixture
def test_document(db, test_company):
    """
    Creates and returns a test document for a test company.
    """
    return Document.objects.create(
        name="Test Document",
        company=test_company,
    )


@pytest.fixture
def test_signer(db, test_document):
    """
    Creates and returns a test signer for a test document.
    """
    return Signer.objects.create(
        token="123e4567-e89b-12d3-a456-426614174000",
        status="pending",
        name="Test Signer",
        email="test@signer.com",
        document=test_document,
    )
