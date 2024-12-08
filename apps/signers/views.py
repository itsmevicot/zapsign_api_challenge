from typing import Optional

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.signers.serializers import SignerSerializer, SignerCreateSerializer, SignerUpdateSerializer
from apps.signers.services import SignerService


class SignerListView(APIView):
    """
    API view to handle signer listing and creation.
    """

    permission_classes = [IsAuthenticated]

    def __init__(
            self,
            signer_service: Optional[SignerService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.signer_service = signer_service or SignerService()

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="List signers",
        responses={
            200: SignerSerializer(many=True)
        },
    )
    def get(self, request, document_id):
        """
        List signers for a document.
        """
        signers = self.signer_service.list_signers(document_id, request.user)
        serializer = SignerSerializer(signers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="Create a signer",
        request_body=SignerCreateSerializer,
        responses={
            201: SignerSerializer
        },
    )
    @transaction.atomic
    def post(self, request, document_id, *args, **kwargs):
        """
        Create a new signer for a document.
        """
        serializer = SignerCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        signers = [
            self.signer_service.create_signer({**signer_data, "document_id": document_id}, request.user)
            for signer_data in serializer.validated_data
        ]
        return Response(SignerSerializer(signers, many=True).data, status=status.HTTP_201_CREATED)


class SignerDetailView(APIView):
    """
    API view to handle signer details, updates, and deletions.
    """

    def __init__(
        self,
        signer_service: Optional[SignerService] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.signer_service = signer_service or SignerService()

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="Retrieve a signer",
        responses={
            200: SignerSerializer
        },
    )
    def get(self, request, signer_id):
        """
        Retrieve a signer by ID.
        """
        signer = self.signer_service.get_signer(signer_id, request.user)
        serializer = SignerSerializer(signer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="Update a signer",
        request_body=SignerUpdateSerializer,
        responses={
            200: SignerSerializer
        },
    )
    @transaction.atomic
    def put(self, request, signer_id):
        """
        Update a signer by ID.
        """
        serializer = SignerUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        signer = self.signer_service.update_signer(signer_id, company=request.user, data=serializer.validated_data)
        return Response(SignerSerializer(signer).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="Delete a signer",
        responses={
            204: "Signer deleted successfully."
        },
    )
    @transaction.atomic
    def delete(self, request, signer_id):
        """
        Delete a signer by ID.
        """
        self.signer_service.delete_signer(signer_id, company=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
