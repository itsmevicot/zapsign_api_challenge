import logging
from typing import Optional

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.companies.models import Company
from apps.companies.repository import CompanyRepository
from utils.exceptions import InvalidCredentialsException, MissingRefreshTokenException, FailedToBlacklistTokenException, \
    PasswordValidationException, CompanyAlreadyExistsException, RegistrationFailedException

logger = logging.getLogger(__name__)


class AuthenticationService:

    def __init__(
            self,
            company_repository: Optional[CompanyRepository] = None,
    ):
        self.company_repository = company_repository or CompanyRepository()

    def login(self, email: str, password: str):
        logger.info(f"Attempting login for email: {email}")

        try:
            company = self.company_repository.get_company_by_email(email)
        except Company.DoesNotExist:
            logger.warning(f"Login failed: Company with email {email} does not exist.")
            raise InvalidCredentialsException()

        if not check_password(password, company.password):
            logger.warning(f"Login failed: Invalid password for email {email}.")
            raise InvalidCredentialsException()

        refresh = RefreshToken.for_user(company)
        refresh['company_id'] = str(company.id)
        logger.info(f"Login successful for email: {email}")

        self.company_repository.update_company(company, last_login=timezone.now())

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def register(self, company_data: dict):
        logger.info(f"Registering company: {company_data.get('email')}")

        password = company_data.pop('password')
        password_validation_errors = []
        try:
            validate_password(password)
        except Exception as e:
            password_validation_errors = e.messages if hasattr(e, 'messages') else [str(e)]

        if password_validation_errors:
            logger.error(f"Password validation failed: {password_validation_errors}")
            raise PasswordValidationException(errors=password_validation_errors)

        company_data['password'] = make_password(password)

        email = company_data.get('email')
        if self.company_repository.company_exists_by_email(email):
            logger.error(f"Registration failed: Company with email {email} already exists.")
            raise CompanyAlreadyExistsException(email=email)

        try:
            company = self.company_repository.create_company(company_data)
            logger.info(f"Company registered successfully: {company.email}")
            return company
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            raise RegistrationFailedException()

    def logout(self, refresh_token: str):
        logger.info("Attempting logout with refresh token.")

        if not refresh_token:
            logger.error("Logout failed: Refresh token is missing.")
            raise MissingRefreshTokenException()

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("Logout successful.")
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            raise FailedToBlacklistTokenException(reason=str(e))
