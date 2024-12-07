from typing import Optional

from django.db.models import QuerySet

from apps.documents.models import Document


class DocumentRepository:
    @staticmethod
    def get_document_by_id(document_id: int) -> Optional[Document]:
        """
        Fetch a document by its ID.
        """
        return Document.objects.filter(id=document_id).first()

    @staticmethod
    def get_documents_by_company(company_id: int) -> QuerySet:
        """
        Fetch all documents belonging to a specific company.
        """
        return Document.objects.filter(company_id=company_id)

    @staticmethod
    def create_document(data: dict) -> Document:
        """
        Create a new document.
        """
        return Document.objects.create(**data)

    @staticmethod
    def update_document(document: Document, **kwargs) -> Document:
        """
        Update an existing document.
        """
        for key, value in kwargs.items():
            setattr(document, key, value)
        document.save()
        return document

    @staticmethod
    def delete_document(document: Document) -> None:
        """
        Delete a document.
        """
        document.delete()
