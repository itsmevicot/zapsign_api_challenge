from typing import Optional

from django.db.models import QuerySet

from apps.signers.models import Signer


class SignerRepository:
    @staticmethod
    def get_signer_by_id(signer_id: int) -> Optional[Signer]:
        """
        Fetch a signer by its ID.
        """
        return Signer.objects.filter(id=signer_id).first()

    @staticmethod
    def get_signers_by_document(document_id: int) -> QuerySet:
        """
        Fetch all signers for a specific document.
        """
        return Signer.objects.filter(document_id=document_id)

    @staticmethod
    def create_signer(data: dict) -> Signer:
        """
        Create a new signer.
        """
        return Signer.objects.create(**data)

    @staticmethod
    def update_signer(signer: Signer, data: dict) -> Signer:
        """
        Update an existing signer with new data.
        """
        for field, value in data.items():
            setattr(signer, field, value)
        signer.save()
        return signer

    @staticmethod
    def delete_signer(signer: Signer) -> None:
        """
        Delete a signer.
        """
        signer.delete()
