import logging
from typing import Optional, List
from django.db import transaction

from apps.companies.models import Company
from apps.companies.repository import CompanyRepository
from utils.exceptions import CompanyNotFoundException, UnauthorizedCompanyAccessException

logger = logging.getLogger(__name__)


class CompanyService:
    def __init__(
        self,
        company_repository: Optional[CompanyRepository] = None
    ):
        self.company_repository = company_repository or CompanyRepository()

    def get_company(self, company_id: int, authenticated_company: Company) -> Company:
        """
        Retrieve a company by its ID and validate ownership.
        """
        try:
            logger.info(f"Fetching company with ID: {company_id} for authenticated company ID: {authenticated_company.id}.")
            company = self.company_repository.get_company_by_id(company_id)
            if not company:
                logger.error(f"Company with ID {company_id} not found.")
                raise CompanyNotFoundException(company_id)
            if company != authenticated_company:
                logger.error(f"Unauthorized access to company ID {company_id} by company ID {authenticated_company.id}.")
                raise UnauthorizedCompanyAccessException(company_id)
            return company
        except CompanyNotFoundException:
            raise
        except UnauthorizedCompanyAccessException:
            raise
        except Exception as e:
            logger.error(f"An error occurred while fetching company ID {company_id}: {str(e)}")
            raise

    def list_companies(self, is_active: Optional[bool] = None) -> List[Company]:
        """
        List all companies, optionally filtering by active status.
        """
        try:
            logger.info("Fetching companies.")
            return list(self.company_repository.get_all_companies(is_active))
        except Exception as e:
            logger.error(f"An error occurred while listing companies: {str(e)}")
            raise

    @transaction.atomic
    def create_company(self, data: dict) -> Company:
        """
        Create a new company.
        """
        try:
            logger.info(f"Creating a new company with data: {data}")
            return self.company_repository.create_company(data)
        except Exception as e:
            logger.error(f"An error occurred while creating a company: {str(e)}")
            raise

    @transaction.atomic
    def update_company(self, company_id: int, data: dict, authenticated_company: Company) -> Company:
        """
        Update an existing company.
        """
        try:
            company = self.get_company(company_id, authenticated_company)
            logger.info(f"Updating company ID {company_id} for authenticated company ID {authenticated_company.id} with data: {data}")
            return self.company_repository.update_company(company, **data)
        except CompanyNotFoundException:
            raise
        except UnauthorizedCompanyAccessException:
            raise
        except Exception as e:
            logger.error(f"An error occurred while updating company ID {company_id}: {str(e)}")
            raise

    @transaction.atomic
    def delete_company(self, company_id: int, authenticated_company: Company) -> None:
        """
        Delete a company.
        """
        try:
            company = self.get_company(company_id, authenticated_company)
            logger.info(f"Deleting company ID {company_id} for authenticated company ID {authenticated_company.id}.")
            self.company_repository.delete_company(company)
        except CompanyNotFoundException:
            raise
        except UnauthorizedCompanyAccessException:
            raise
        except Exception as e:
            logger.error(f"An error occurred while deleting company ID {company_id}: {str(e)}")
            raise
