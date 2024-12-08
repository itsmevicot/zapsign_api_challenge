from typing import Optional

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.serializers import LoginSerializer, TokenResponseSerializer, LogoutResponseSerializer
from apps.authentication.services import AuthenticationService
from apps.companies.serializers import CompanyCreateSerializer, CompanyCreateResponseSerializer


class LoginView(APIView):
    """
    Login endpoint for companies.
    """
    permission_classes = [AllowAny]

    def __init__(
            self,
            authentication_service: Optional[AuthenticationService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.authentication_service = authentication_service or AuthenticationService()

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        tokens = self.authentication_service.login(email, password)

        response_serializer = TokenResponseSerializer(data=tokens)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Register endpoint for companies.
    """
    permission_classes = [AllowAny]

    def __init__(
            self,
            authentication_service: Optional[AuthenticationService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.authentication_service = authentication_service or AuthenticationService()

    def post(self, request, *args, **kwargs):
        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = self.authentication_service.register(serializer.validated_data)

        return Response(CompanyCreateResponseSerializer(company).data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    Logout endpoint for companies.
    """
    permission_classes = [AllowAny]

    def __init__(
            self,
            authentication_service: Optional[AuthenticationService] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.authentication_service = authentication_service or AuthenticationService()

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        self.authentication_service.logout(refresh_token)

        response_serializer = LogoutResponseSerializer(data={"message": "Logout successful."})
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
