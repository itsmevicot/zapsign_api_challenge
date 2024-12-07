from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import TokenError

from utils.exceptions import ExceptionMessageBuilder


def custom_exception_handler(exc, context):
    """
    Custom exception handler for processing custom exceptions and default DRF exceptions.
    """
    if isinstance(exc, ExceptionMessageBuilder):
        return Response(
            {
                "error": {
                    "title": exc.title,
                    "message": exc.message,
                }
            },
            status=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, DRFValidationError):
        return Response(
            {
                "error": {
                    "title": "Validation Error",
                    "message": exc.detail,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, AttributeError):
        return Response(
            {
                "error": {
                    "title": "Server Error",
                    "message": "An unexpected error occurred. Please try again later."
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, TokenError):
        return Response(
            {
                "message": "The refresh token has already been invalidated or is no longer valid."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = exception_handler(exc, context)
    if response is not None:
        response.data["status_code"] = response.status_code

    return response
