from typing import Optional

from django.db.models import QuerySet

from apps.companies.models import Company


class CompanyRepository:
    @staticmethod
    def get_company_by_id(company_id: int) -> Optional[Company]:
        """
        Fetch a company by its ID.
        """
        return Company.objects.filter(id=company_id).first()

    @staticmethod
    def get_all_companies(is_active: Optional[bool] = None) -> QuerySet:
        """
        Fetch all companies, optionally filtering by their active status.
        """
        companies = Company.objects.all()
        if is_active is not None:
            companies = companies.filter(is_active=is_active)
        return companies

    @staticmethod
    def create_company(data: dict) -> Company:
        """
        Create a new company.
        """
        return Company.objects.create(**data)

    @staticmethod
    def update_company(company: Company, **kwargs) -> Company:
        """
        Update an existing company.
        """
        for key, value in kwargs.items():
            setattr(company, key, value)
        company.save()
        return company

    @staticmethod
    def delete_company(company: Company, hard_delete: bool = False) -> None:
        """
        Delete a company.
        """
        if hard_delete:
            company.delete()
        else:
            company.is_active = False
            company.save()
