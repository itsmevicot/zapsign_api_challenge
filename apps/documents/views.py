from typing import Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.documents.serializers import DocumentSerializer, DocumentCreateSerializer, DocumentUpdateSerializer
from apps.documents.service import DocumentService


class DocumentListView(APIView):
    """
    API view to handle document listing and creation.
    """

    def __init__(
            self,
            document_service: Optional[DocumentService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.document_service = document_service or DocumentService()

    @swagger_auto_schema(
        tags=["documents"],
        operation_summary="List documents",
        responses={
            200: DocumentSerializer(many=True)
        },
    )
    def get(self, request, *args, **kwargs):
        """
        List documents for a company.
        """
        documents = self.document_service.list_documents(request.user.id)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["documents"],
        operation_summary="Create a document",
        request_body=DocumentCreateSerializer,
        responses={
            201: DocumentSerializer
        },
    )
    def post(self, request, company_id):
        """
        Create a new document for a company.
        """
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["company_id"] = company_id
        document = self.document_service.create_document(data)
        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)


class DocumentDetailView(APIView):
    """
    API view to handle document details, updates, and deletions.
    """

    def __init__(
            self,
            document_service: Optional[DocumentService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.document_service = document_service or DocumentService()

    @swagger_auto_schema(
        tags=["documents"],
        operation_summary="Retrieve a document",
        responses={
            200: DocumentSerializer
        },
    )
    def get(self, request, document_id):
        """
        Retrieve a document for a specific company.
        """
        document = self.document_service.get_document(document_id, request.user)
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["documents"],
        operation_summary="Update a document",
        request_body=DocumentUpdateSerializer,
        responses={
            200: DocumentSerializer
        },
    )
    def put(self, request, company_id, document_id):
        """
        Update a document for a specific company.
        """
        serializer = DocumentUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        document = self.document_service.update_document(document_id, company_id, data)
        return Response(DocumentSerializer(document).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["documents"],
        operation_summary="Delete a document",
        responses={
            204: "Document deleted successfully."
        },
    )
    def delete(self, request, company_id, document_id):
        """
        Delete a document for a specific company.
        """
        self.document_service.delete_document(document_id, company_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
