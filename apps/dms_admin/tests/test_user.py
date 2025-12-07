from django.test import SimpleTestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.dms_admin.serializers.user import UserCreateSerializer, UserUpdateSerializer
from apps.dms_admin.views import UserViewSet
from core.pagination_handler import DefaultPagination


class TestUserViewSetUnit(SimpleTestCase):

    def setUp(self):
        self.view = UserViewSet()

    def test_get_serializer_class_create(self):
        self.view.action = "create"
        self.assertEqual(self.view.get_serializer_class(), UserCreateSerializer)

    def test_get_serializer_class_update(self):
        self.view.action = "update"
        self.assertEqual(self.view.get_serializer_class(), UserUpdateSerializer)

    def test_get_serializer_class_partial_update(self):
        self.view.action = "partial_update"
        self.assertEqual(self.view.get_serializer_class(), UserUpdateSerializer)

    def test_get_serializer_class_default(self):
        self.view.action = "list"
        self.assertEqual(self.view.get_serializer_class(), UserUpdateSerializer)

    def test_permission_classes_config(self):
        self.assertEqual(len(self.view.permission_classes), 1)
        combined = self.view.permission_classes[0]
        self.assertTrue(callable(combined))
        self.assertIn("OperandHolder", type(combined).__name__)

    def test_filter_backends_config(self):
        self.assertEqual(self.view.filter_backends, [DjangoFilterBackend, filters.SearchFilter])

    def test_search_fields(self):
        self.assertEqual(self.view.search_fields, ["username", "role"])

    def test_filterset_fields(self):
        self.assertEqual(self.view.filterset_fields, ["role"])

    def test_pagination_class(self):
        self.assertEqual(self.view.pagination_class, DefaultPagination)

    def test_queryset_is_defined(self):
        self.assertIsNotNone(self.view.queryset)
        self.assertTrue(hasattr(self.view.queryset, "model"))
