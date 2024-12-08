from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException


class ExceptionInterface:
    title: Optional[str] = "Something went wrong"
    status_code: Optional[int] = 500
    message: Optional[str] = "An error occurred while processing your request"


class ExceptionMessageBuilder(APIException):
    def __init__(self, ex_info: ExceptionInterface):
        self.title = ex_info.title
        self.status_code = ex_info.status_code
        self.message = ex_info.message


class CompanyNotFoundException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Company Not Found"
        self.message = f"Company was not found or doesn't exist."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedCompanyAccessException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to access this company."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}


class InvalidCredentialsException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Invalid Credentials"
        self.message = "The provided email or password is incorrect."
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = {"title": self.title, "message": self.message}


class DocumentNotFoundException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Document Not Found"
        self.message = f"Document was not found or doesn't exist."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedDocumentAccessException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to access this document."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}


class SignerNotFoundException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Signer Not Found"
        self.message = f"Signer was not found or doesn't exist."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedSignerAccessException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to view information about this signer."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}


class FailedToCreateDocumentException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Failed to Create Document"
        self.message = "The document could not be created in the database."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = {"title": self.title, "message": self.message}


class FailedToCreateDocumentInZapSignException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Failed to Create Document in ZapSign"
        self.message = "The document could not be created in the ZapSign API."
        self.status_code = status.HTTP_502_BAD_GATEWAY
        self.detail = {"title": self.title, "message": self.message}


class MissingZapSignResponseFieldsException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Missing Fields in ZapSign Response"
        self.message = "The ZapSign API response is missing required fields."
        self.status_code = status.HTTP_502_BAD_GATEWAY
        self.detail = {"title": self.title, "message": self.message}


class FailedToUpdateDocumentException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Failed to Update Document"
        self.message = "The document could not be updated with ZapSign details."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = {"title": self.title, "message": self.message}


class FailedToCreateSignerException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Failed to Create Signer"
        self.message = "The signer could not be added to the document."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = {"title": self.title, "message": self.message}


class MissingRefreshTokenException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Refresh Token Missing"
        self.message = "The refresh token is required but was not provided."
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {"title": self.title, "message": self.message}


class FailedToBlacklistTokenException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Failed to Blacklist Token"
        self.message = f"An error occurred while blacklisting the refresh token."
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {"title": self.title, "message": self.message}


class CompanyAlreadyExistsException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Company Already Exists"
        self.message = f"A company with this email already exists."
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = {"title": self.title, "message": self.message}


class PasswordValidationException(ExceptionMessageBuilder):
    def __init__(self, errors: list):
        self.title = "Password Validation Failed"
        self.message = "The password provided does not meet the security requirements."
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {"title": self.title, "message": self.message, "errors": errors}


class RegistrationFailedException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Registration Failed"
        self.message = "An unexpected error occurred during registration."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = {"title": self.title, "message": self.message}
