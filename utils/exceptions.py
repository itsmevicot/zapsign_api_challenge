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
    def __init__(self, company_id: int):
        self.title = "Company Not Found"
        self.message = f"Company with ID {company_id} not found."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedCompanyAccessException(ExceptionMessageBuilder):
    def __init__(self, company_id: int):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to access company ID {company_id}."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}


class InvalidCredentialsException(ExceptionMessageBuilder):
    def __init__(self):
        self.title = "Invalid Credentials"
        self.message = "The provided email or password is incorrect."
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = {"title": self.title, "message": self.message}


class DocumentNotFoundException(ExceptionMessageBuilder):
    def __init__(self, document_id: int):
        self.title = "Document Not Found"
        self.message = f"Document with ID {document_id} not found."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedDocumentAccessException(ExceptionMessageBuilder):
    def __init__(self, document_id: int):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to access document ID {document_id}."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}


class SignerNotFoundException(ExceptionMessageBuilder):
    def __init__(self, signer_id: int):
        self.title = "Signer Not Found"
        self.message = f"Signer with ID {signer_id} not found."
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {"title": self.title, "message": self.message}


class UnauthorizedSignerAccessException(ExceptionMessageBuilder):
    def __init__(self, signer_id: int):
        self.title = "Unauthorized Access"
        self.message = f"You are not authorized to access signer ID {signer_id}."
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = {"title": self.title, "message": self.message}
