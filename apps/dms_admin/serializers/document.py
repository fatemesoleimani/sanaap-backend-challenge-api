from rest_framework import serializers

from apps.document.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    user = serializers.CharField(source="user__username", read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
