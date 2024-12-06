import logging
from typing import Optional, List
from django.db import transaction

from apps.documents.models import Document
from apps.documents.repository import DocumentRepository
from utils.exceptions import DocumentNotFoundException, UnauthorizedDocumentAccessException

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
            self,
            document_repository: Optional[DocumentRepository] = None
    ):
        self.document_repository = document_repository or DocumentRepository()

    def get_document(self, document_id: int, company_id: int) -> Document:
        """
        Retrieve a document by ID and validate ownership.
        """
        try:
            logger.info(f"Fetching document with ID {document_id} for company ID {company_id}.")
            document = self.document_repository.get_document_by_id(document_id)
            if not document:
                logger.error(f"Document with ID {document_id} not found.")
                raise DocumentNotFoundException(document_id)
            if document.company_id != company_id:
                logger.error(f"Unauthorized access to document ID {document_id} by company ID {company_id}.")
                raise UnauthorizedDocumentAccessException(document_id)
            return document
        except (DocumentNotFoundException, UnauthorizedDocumentAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching document ID {document_id}: {str(e)}")
            raise

    def list_documents(self, company_id: int) -> List[Document]:
        """
        List all documents for a specific company.
        """
        try:
            logger.info(f"Fetching documents for company ID {company_id}.")
            return list(self.document_repository.get_documents_by_company(company_id))
        except Exception as e:
            logger.error(f"An unexpected error occurred while listing documents for company ID {company_id}: {str(e)}")
            raise

    @transaction.atomic
    def create_document(self, data: dict) -> Document:
        """
        Create a new document.
        """
        try:
            logger.info(f"Creating a new document with data: {data}")
            return self.document_repository.create_document(data)
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating a document: {str(e)}")
            raise

    @transaction.atomic
    def update_document(self, document_id: int, company_id: int, data: dict) -> Document:
        """
        Update an existing document.
        """
        try:
            document = self.get_document(document_id, company_id)
            logger.info(f"Updating document ID {document_id} for company ID {company_id} with data: {data}")
            return self.document_repository.update_document(document, **data)
        except (DocumentNotFoundException, UnauthorizedDocumentAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while updating document ID {document_id}: {str(e)}")
            raise

    @transaction.atomic
    def delete_document(self, document_id: int, company_id: int) -> None:
        """
        Delete a document.
        """
        try:
            document = self.get_document(document_id, company_id)
            logger.info(f"Deleting document ID {document_id} for company ID {company_id}.")
            self.document_repository.delete_document(document)
        except (DocumentNotFoundException, UnauthorizedDocumentAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting document ID {document_id}: {str(e)}")
            raise
