import uuid

from rest_framework import serializers

from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "email", "name", "api_token", "is_active", "created_at", "last_update_at"]


class CompanyCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=255, required=True)
    api_token = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Validate that the password and repeat_password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        data.pop('confirm_password', None)
        return data

    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if Company.objects.filter(email=value).exists():
            raise serializers.ValidationError("A company with this email already exists.")
        return value

    def validate_api_token(self, value):
        """
        Validate that the api_token is a valid UUID if provided.
        """
        try:
            uuid.UUID(value)
        except ValueError:
            raise serializers.ValidationError("The API token must be a valid UUID.")

        return value


class CompanyCreateResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField()


class CompanyUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField(required=False)
    api_token = serializers.CharField(max_length=255, required=False)
