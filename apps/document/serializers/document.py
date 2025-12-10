from rest_framework import serializers

from apps.document.models.document import Document
from common.validators import validate_image_file
from dms.settings import AWS_S3_ENDPOINT_PUBLIC_URL


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, validators=[validate_image_file])
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields['file'].required = True

    def update(self, instance, validated_data):
        file = validated_data.get('file', None)
        if file and instance.file:
            instance.file.delete(save=False)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        file_url = data.get("file")
        if file_url:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(file_url)
            public_parsed = urlparse(AWS_S3_ENDPOINT_PUBLIC_URL)

            replaced = parsed._replace(
                scheme=public_parsed.scheme,
                netloc=public_parsed.netloc,
            )
            data["file"] = urlunparse(replaced)
        return data
