from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.authentication.serializers import CompanyLoginSerializer
from apps.companies.models import Company

from utils.exceptions import InvalidCredentialsException


class LoginView(APIView):
    """
    Login endpoint for companies.
    """

    @staticmethod
    def post(request):
        serializer = CompanyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            company = Company.objects.get(email=email)
        except Company.DoesNotExist:
            raise InvalidCredentialsException()

        refresh = RefreshToken.for_user(company)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
