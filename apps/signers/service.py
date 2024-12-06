import logging
from typing import Optional, List
from django.db import transaction

from apps.signers.models import Signer
from apps.signers.repository import SignerRepository
from utils.exceptions import SignerNotFoundException, UnauthorizedSignerAccessException

logger = logging.getLogger(__name__)


class SignerService:
    def __init__(
            self,
            signer_repository: Optional[SignerRepository] = None
    ):
        self.signer_repository = signer_repository or SignerRepository()

    def get_signer(self, signer_id: int, document_id: int) -> Signer:
        """
        Retrieve a signer by ID and validate its association with the document.
        """
        try:
            logger.info(f"Fetching signer with ID {signer_id} for document ID {document_id}.")
            signer = self.signer_repository.get_signer_by_id(signer_id)
            if not signer:
                logger.error(f"Signer with ID {signer_id} not found.")
                raise SignerNotFoundException(signer_id)
            if signer.document_id != document_id:
                logger.error(f"Unauthorized access to signer ID {signer_id} for document ID {document_id}.")
                raise UnauthorizedSignerAccessException(signer_id)
            return signer
        except (SignerNotFoundException, UnauthorizedSignerAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching signer ID {signer_id}: {str(e)}")
            raise

    def list_signers(self, document_id: int) -> List[Signer]:
        """
        List all signers for a specific document.
        """
        try:
            logger.info(f"Fetching signers for document ID {document_id}.")
            return list(self.signer_repository.get_signers_by_document(document_id))
        except Exception as e:
            logger.error(f"An unexpected error occurred while listing signers for document ID {document_id}: {str(e)}")
            raise

    @transaction.atomic
    def create_signer(self, data: dict) -> Signer:
        """
        Create a new signer.
        """
        try:
            logger.info(f"Creating a new signer with data: {data}")
            return self.signer_repository.create_signer(data)
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating a signer: {str(e)}")
            raise

    @transaction.atomic
    def update_signer(self, signer_id: int, document_id: int, data: dict) -> Signer:
        """
        Update an existing signer.
        """
        try:
            signer = self.get_signer(signer_id, document_id)
            logger.info(f"Updating signer ID {signer_id} for document ID {document_id} with data: {data}")
            return self.signer_repository.update_signer(signer, **data)
        except (SignerNotFoundException, UnauthorizedSignerAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while updating signer ID {signer_id}: {str(e)}")
            raise

    @transaction.atomic
    def delete_signer(self, signer_id: int, document_id: int) -> None:
        """
        Delete a signer.
        """
        try:
            signer = self.get_signer(signer_id, document_id)
            logger.info(f"Deleting signer ID {signer_id} for document ID {document_id}.")
            self.signer_repository.delete_signer(signer)
        except (SignerNotFoundException, UnauthorizedSignerAccessException):
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting signer ID {signer_id}: {str(e)}")
            raise
