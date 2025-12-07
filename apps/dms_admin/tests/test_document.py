from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.document.models import Document
from apps.user.choices import UserRoleChoices

User = get_user_model()


class DocumentAdminViewSetTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True,
                                                   is_superuser=True, role=UserRoleChoices.admin)
        self.client.force_authenticate(user=self.admin_user)
        self.url = reverse('admin_document-list')
        self.document = Document.objects.create(
            title="Initial Title",
            file=self.create_test_file(),
            user=self.admin_user
        )

    def test_create_document(self):
        data = {
            'title': 'Test Document',
            'file': self.create_test_file()  # Assume this method creates a temporary file
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(Document.objects.first().title, 'Test Document')

    def test_update_document(self):
        data = {
            'title': 'Updated Title',
            'file': self.create_test_file(),
        }

        response = self.client.put(
            reverse('admin_document-detail', args=[self.document.id]),
            data,
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_documents(self):
        Document.objects.create(title='Doc 1', user=self.admin_user)
        Document.objects.create(title='Doc 2', user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 3)

    @staticmethod
    def create_test_file(filename='test.txt', content=b'Test content'):
        return SimpleUploadedFile(filename, content, content_type='text/plain')
