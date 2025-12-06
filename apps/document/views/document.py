from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.document.models import Document
from apps.document.serializers import DocumentSerializer
from core.pagination_handler import DefaultPagination
from core.permission import IsEditor, IsViewer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user__username", "title"]
    search_fields = ["title"]
    ordering_fields = ["id", "title", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        """
        Only editor + viewer allowed.
        - viewer: list + retrieve
        - editor: list + retrieve + create + update
        - NO DELETE for both
        """

        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated, IsViewer]
        elif self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsEditor]
        elif self.action == "destroy":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

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

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Delete not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
