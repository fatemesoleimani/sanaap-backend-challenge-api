from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from apps.dms_admin.serializers.user import UserCreateSerializer, UserUpdateSerializer
from apps.user.models import User
from core.pagination_handler import DefaultPagination
from core.permission import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated & IsAdmin]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'role']

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserUpdateSerializer
