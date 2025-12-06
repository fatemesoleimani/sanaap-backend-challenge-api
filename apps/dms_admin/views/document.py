from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiRequest
from rest_framework import viewsets, filters
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from apps.dms_admin.serializers.document import DocumentSerializer
from apps.document.models import Document
from core.pagination_handler import DefaultPagination
from core.permission import IsAdmin

from drf_spectacular.utils import extend_schema, OpenApiTypes

class DocumentAdminViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated & IsAdmin]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'title']
    search_fields = ['title']
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                },
                'required': ['title', 'file']
            }
        },
        responses=DocumentSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
