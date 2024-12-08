from rest_framework import serializers
from apps.signers.models import Signer


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ["id", "token", "status", "name", "email", "external_id", "document"]


class SignerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class SignerUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50, required=False)
    name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    external_id = serializers.CharField(max_length=255, required=False)
    token = serializers.CharField(max_length=255)
