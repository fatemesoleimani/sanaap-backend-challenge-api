from rest_framework import serializers

from apps.document.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)
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
