from typing import Optional
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.companies.serializers import CompanySerializer, CompanyCreateSerializer, CompanyUpdateSerializer
from apps.companies.service import CompanyService
from utils.permissions import IsSuperUser


class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(
            self,
            company_service: Optional[CompanyService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.company_service = company_service or CompanyService()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsSuperUser()]
        return super().get_permissions()

    @swagger_auto_schema(
        tags=["companies"],
        operation_summary="List companies",
        operation_description="Retrieve a list of all companies, optionally filtering by active status.",
        responses={
            200: CompanySerializer(many=True)
        },
    )
    def get(self, request):
        """
        Get a list of companies.
        """
        is_active = request.query_params.get("is_active", None)
        companies = self.company_service.list_companies(is_active=is_active)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["companies"],
        operation_summary="Create a company",
        operation_description="Create a new company.",
        request_body=CompanyCreateSerializer,
        responses={
            201: CompanySerializer
        },
    )
    def post(self, request):
        """
        Create a new company.
        """
        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.company_service.create_company(serializer.validated_data)
        return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(
            self,
            company_service: Optional[CompanyService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.company_service = company_service or CompanyService()

    @swagger_auto_schema(
        tags=["companies"],
        operation_summary="Get company details",
        responses={
            200: CompanySerializer
        },
    )
    def get(self, request, company_id: int, *args, **kwargs):
        """
        Get details of a company.
        """
        company = self.company_service.get_company(company_id, request.user)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["companies"],
        operation_summary="Update a company",
        request_body=CompanyUpdateSerializer,
        responses={
            200: CompanySerializer
        },
    )
    def put(self, request, company_id: int):
        """
        Update an existing company.
        """
        serializer = CompanyUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        company = self.company_service.update_company(company_id, serializer.validated_data)
        return Response(CompanySerializer(company).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["companies"],
        operation_summary="Delete a company",
        responses={
            204: "Company deleted successfully."
        },
    )
    def delete(self, request, company_id: int):
        """
        Delete a company.
        """
        self.company_service.delete_company(company_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
