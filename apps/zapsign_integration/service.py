import logging
from typing import Optional, Dict
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ZapSignService:
    """
    Service class responsible for handling business rules related to
    ZapSign API integration.
    """

    def __init__(
            self,
            api_base_url: Optional[str] = None,
            api_token: Optional[str] = None
    ):
        """
        Initializes the ZapSignService with optional configurations.
        """
        self.api_base_url = api_base_url or settings.ZAPSIGN_BASE_URL
        self.api_token = api_token or settings.ZAPSIGN_API_TOKEN

    def get_headers(self) -> Dict[str, str]:
        """
        Returns the headers required for ZapSign API requests.
        """
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def create_document_in_zapsign(
            self,
            name: str,
            signers: list,
            base64_pdf: str = None,
            url_pdf: str = None
    ) -> dict:
        """
        Creates a document in the ZapSign API.
        """
        try:
            if not base64_pdf and not url_pdf:
                logger.error("Failed to create document: Neither base64_pdf nor url_pdf was provided.")
                raise ValueError("You must provide either a base64-encoded PDF or a URL.")

            payload = {
                "name": name,
                "signers": signers
            }

            if base64_pdf:
                payload["base64_pdf"] = base64_pdf
            elif url_pdf:
                payload["url_pdf"] = url_pdf

            logger.info(f"Creating document with payload: {payload}")
            response = requests.post(self.api_base_url, headers=self.get_headers(), json=payload)

            if response.status_code != 201:
                logger.error(f"Failed to create document: {response.text}")
                response.raise_for_status()

            logger.info("Document created successfully.")
            return response.json()
        except Exception as e:
            logger.error(f"An error occurred while creating a document: {str(e)}")
            raise

    def get_document(self, document_token: str) -> dict:
        """
        Retrieves a document's details from the ZapSign API.
        """
        try:
            url = f"{self.api_base_url}{document_token}/"
            logger.info(f"Fetching document with token: {document_token}")
            response = requests.get(url, headers=self.get_headers())

            if response.status_code != 200:
                logger.error(f"Failed to fetch document: {response.text}")
                response.raise_for_status()

            logger.info("Document retrieved successfully.")
            return response.json()
        except Exception as e:
            logger.error(f"An error occurred while fetching the document with token {document_token}: {str(e)}")
            raise

    def delete_document(self, document_token: str) -> dict:
        """
        Deletes a document from the ZapSign API.
        """
        try:
            url = f"{self.api_base_url}{document_token}/"
            logger.info(f"Deleting document with token: {document_token}")
            response = requests.delete(url, headers=self.get_headers())

            if response.status_code not in [200, 204]:
                logger.error(f"Failed to delete document: {response.text}")
                response.raise_for_status()

            logger.info("Document deleted successfully.")
            return {"message": "Document deleted successfully."}
        except Exception as e:
            logger.error(f"An error occurred while deleting the document with token {document_token}: {str(e)}")
            raise
