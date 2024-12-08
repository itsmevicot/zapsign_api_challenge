import pytest
from rest_framework.test import APIClient

from apps.companies.models import Company


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mocked_authentication_service(mocker):
    return mocker.patch("apps.authentication.service.AuthenticationService", autospec=True)


@pytest.fixture
def test_company(db):
    """
    Create and return a test company.
    """
    return Company.objects.create(
        name="Test Company",
        email="test@company.com",
        api_token="123e4567-e89b-12d3-a456-426614174000"
    )


@pytest.fixture
def authenticated_client(api_client, test_company):
    """
    Authenticate the API client using the test company.
    """
    api_client.force_authenticate(user=test_company)
    return api_client
