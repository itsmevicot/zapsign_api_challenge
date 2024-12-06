from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
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

    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    return response
