from rest_framework import serializers
from apps.signers.models import Signer


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ["id", "token", "status", "name", "email", "external_id", "document"]


class SignerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    auth_mode = serializers.CharField(max_length=50, required=False, default="assinaturaTela")
    send_automatic_email = serializers.BooleanField(required=False, default=True)


class SignerUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50, required=False)
    name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    external_id = serializers.CharField(max_length=255, required=False)
    token = serializers.CharField(max_length=255)
