import logging
from typing import Optional, List
from django.db import transaction

from apps.documents.models import Document
from apps.documents.repository import DocumentRepository
from apps.signers.repository import SignerRepository
from apps.zapsign_integration.service import ZapSignService
from utils.exceptions import DocumentNotFoundException, UnauthorizedDocumentAccessException, \
    FailedToCreateDocumentException, FailedToCreateSignerException, FailedToCreateDocumentInZapSignException, \
    MissingZapSignResponseFieldsException, FailedToUpdateDocumentException

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        document_repository: Optional[DocumentRepository] = None,
        signer_repository: Optional[SignerRepository] = None,
        zap_sign_service: Optional[ZapSignService] = None,
    ):
        self.document_repository = document_repository or DocumentRepository()
        self.signer_repository = signer_repository or SignerRepository()
        self.zap_sign_service = zap_sign_service or ZapSignService()

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
        Create a new document in the local database, send details to ZapSign API,
        and update the document with ZapSign's response.
        """
        try:
            logger.info(f"Starting the creation process for a new document with data: {data}")

            document = self.document_repository.create_document(data)

            if document:
                logger.info(f"Document created in local database with ID {document.id}.")
            else:
                logger.error("Failed to create document in local database.")
                raise FailedToCreateDocumentException()

            zap_sign_payload = {
                "name": document.name,
                "signers": data.get("signers"),
                "base64_pdf": data.get("base64_pdf"),
                "url_pdf": data.get("url_pdf"),
            }

            zap_sign_response = self.zap_sign_service.create_document_in_zapsign(**zap_sign_payload)

            if zap_sign_response:
                logger.info(f"ZapSign API response: {zap_sign_response}")
            else:
                logger.error("Failed to create document in ZapSign API.")
                raise FailedToCreateDocumentInZapSignException()

            document_update_data = {
                "token": zap_sign_response.get("token"),
                "status": zap_sign_response.get("status"),
                "open_id": zap_sign_response.get("open_id"),
                "zap_sign_created_by": zap_sign_response["created_by"]["email"],
                "zap_sign_external_id": zap_sign_response.get("external_id"),
            }

            if not all(document_update_data.values()):
                logger.error("Missing fields in ZapSign response.")
                raise MissingZapSignResponseFieldsException()

            updated_document = self.document_repository.update_document(document, **document_update_data)

            if updated_document:
                logger.info(f"Document updated with ZapSign details: {document_update_data}")
            else:
                logger.error("Failed to update document with ZapSign details.")
                raise FailedToUpdateDocumentException()

            for signer in zap_sign_response.get("signers", []):
                signer_data = {
                    "token": signer.get("token"),
                    "status": signer.get("status"),
                    "name": signer.get("name"),
                    "email": signer.get("email"),
                    "external_id": signer.get("external_id"),
                    "document": updated_document,
                }
                created_signer = self.signer_repository.create_signer(signer_data)
                if created_signer:
                    logger.info(f"Signer created with ID {created_signer.id} for document {updated_document.id}.")
                else:
                    logger.error(f"Failed to create signer with data {signer_data} for document {updated_document.id}.")
                    raise FailedToCreateSignerException()

            return updated_document

        except FailedToCreateDocumentException as e:
            logger.error(f"Failed to create document. Details: {str(e)}")
            raise

        except FailedToCreateDocumentInZapSignException as e:
            logger.error(f"Failed to create document in ZapSign. Details: {str(e)}")
            raise

        except MissingZapSignResponseFieldsException as e:
            logger.error(f"Missing fields in ZapSign response. Details: {str(e)}")
            raise

        except FailedToUpdateDocumentException as e:
            logger.error(f"Failed to update document. Details: {str(e)}")
            raise

        except FailedToCreateSignerException as e:
            logger.error(f"Failed to create signer. Details: {str(e)}")
            raise

        except ValueError as ve:
            logger.error(f"Validation error during document creation: {str(ve)}")
            raise

        except Exception as e:
            logger.error(f"An unexpected error occurred during document creation: {str(e)}")
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
