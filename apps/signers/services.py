import logging
from typing import Optional, List
from django.db import transaction
from django.db.models import QuerySet

from apps.companies.models import Company
from apps.documents.service import DocumentService
from apps.signers.models import Signer
from apps.signers.repository import SignerRepository
from utils.exceptions import SignerNotFoundException, UnauthorizedSignerAccessException

logger = logging.getLogger(__name__)


class SignerService:
    def __init__(
            self,
            signer_repository: Optional[SignerRepository] = None,
            document_service: Optional[DocumentService] = None,
    ):
        self.signer_repository = signer_repository or SignerRepository()
        self.document_service = document_service or DocumentService()

    def get_signer(self, signer_id: int, company: Company) -> Signer:
        """
        Retrieve a signer by ID and validate its association with the company.
        """
        try:
            logger.info(f"Fetching signer with ID {signer_id}.")

            signer = self.signer_repository.get_signer_by_id(signer_id)

            if not signer:
                logger.error(f"Signer with ID {signer_id} not found.")
                raise SignerNotFoundException()

            self.document_service.validate_document_ownership(document_id=signer.document_id, company=company)

            return signer
        except SignerNotFoundException:
            raise
        except UnauthorizedSignerAccessException:
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching signer ID {signer_id}: {str(e)}")
            raise

    def list_signers(self, document_id: int, company: Company) -> QuerySet:
        """
        List all signers for a specific document if it belongs to the company.
        """
        try:
            logger.info(f"Fetching signers for document ID {document_id}.")

            self.document_service.validate_document_ownership(document_id=document_id, company=company)

            return self.signer_repository.get_signers_by_document(document_id)
        except Exception as e:
            logger.error(f"An unexpected error occurred while listing signers for document ID {document_id}: {str(e)}")
            raise

    @transaction.atomic
    def create_signer(self, data: dict, company: Company) -> Signer:
        """
        Create a new signer.
        """
        try:
            logger.info(f"Creating a new signer with data: {data}")
            self.document_service.validate_document_ownership(document_id=data["document_id"], company=company)
            allowed_fields = {"name", "email", "document_id"}
            filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
            return self.signer_repository.create_signer(filtered_data)
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating a signer: {str(e)}")
            raise

    @transaction.atomic
    def update_signer(self, signer_id: int, company: Company, data: dict) -> Signer:
        """
        Update a signer and validate its association with the company.
        """
        signer = self.get_signer(signer_id, company)
        logger.info(f"Updating signer with ID {signer_id}.")

        return self.signer_repository.update_signer(signer, data)

    @transaction.atomic
    def delete_signer(self, signer_id: int, company: Company):
        """
        Delete a signer and validate its association with the company.
        """
        signer = self.get_signer(signer_id, company)
        logger.info(f"Deleting signer with ID {signer_id}.")

        self.signer_repository.delete_signer(signer)
