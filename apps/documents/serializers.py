from rest_framework import serializers
from apps.documents.models import Document
from apps.signers.serializers import SignerSerializer, SignerCreateSerializer


class DocumentSerializer(serializers.ModelSerializer):
    signers = SignerSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            "id", "open_id", "token", "name", "status", "created_at", "last_updated_at",
            "created_by", "company", "external_id", "signers"
        ]


class DocumentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    url_pdf = serializers.URLField(required=True)
    signers = SignerCreateSerializer(many=True)

    def validate(self, data):
        if not data.get("signers"):
            raise serializers.ValidationError("At least one signer is required.")
        return data


class DocumentUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=50, required=False)
    external_id = serializers.CharField(max_length=255, required=False)
