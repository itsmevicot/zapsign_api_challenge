from typing import Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.signers.serializers import SignerSerializer, SignerCreateSerializer, SignerUpdateSerializer
from apps.signers.service import SignerService


class SignerListView(APIView):
    """
    API view to handle signer listing and creation.
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
        operation_summary="List signers",
        responses={
            200: SignerSerializer(many=True)
        },
    )
    def get(self, request, document_id):
        """
        List signers for a document.
        """
        signers = self.signer_service.list_signers(document_id)
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
    def post(self, request, document_id):
        """
        Create a new signer for a document.
        """
        serializer = SignerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["document"] = document_id
        signer = self.signer_service.create_signer(data)
        return Response(SignerSerializer(signer).data, status=status.HTTP_201_CREATED)


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
    def get(self, request, document_id, signer_id):
        """
        Retrieve a signer for a specific document.
        """
        signer = self.signer_service.get_signer(signer_id, document_id)
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
    def put(self, request, document_id, signer_id):
        """
        Update a signer for a specific document.
        """
        serializer = SignerUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        signer = self.signer_service.update_signer(signer_id, document_id, data)
        return Response(SignerSerializer(signer).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["signers"],
        operation_summary="Delete a signer",
        responses={
            204: "Signer deleted successfully."
        },
    )
    def delete(self, request, document_id, signer_id):
        """
        Delete a signer for a specific document.
        """
        self.signer_service.delete_signer(signer_id, document_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
