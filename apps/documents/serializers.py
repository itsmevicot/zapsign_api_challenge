from rest_framework import serializers
from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id", "open_id", "token", "name", "status", "created_at", "last_updated_at",
            "created_by", "company", "external_id"
        ]


class DocumentCreateSerializer(serializers.Serializer):
    open_id = serializers.IntegerField()
    token = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)
    created_by = serializers.CharField(max_length=255)
    company = serializers.IntegerField()


class DocumentUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=50, required=False)
    external_id = serializers.CharField(max_length=255, required=False)
