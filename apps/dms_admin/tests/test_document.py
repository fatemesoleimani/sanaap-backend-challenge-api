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
        self.admin_user = User.objects.create_user(
            username='admin',
            password='password',
            is_staff=True,
            is_superuser=True,
            role=UserRoleChoices.admin
        )
        self.client.force_authenticate(user=self.admin_user)

        self.url = reverse('admin_document-list')

        self.document = Document.objects.create(
            title="Initial Title",
            file=self.create_test_file(),
            user=self.admin_user
        )

    # ---------------------------
    # Create Test
    # ---------------------------
    def test_create_document(self):
        data = {
            'title': 'Test Document',
            'file': self.create_test_file()
        }
        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(Document.objects.first().title, 'Test Document')

    # ---------------------------
    # Update Test
    # ---------------------------
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
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, "Updated Title")

    # ---------------------------
    # Delete Test
    # ---------------------------
    def test_delete_document(self):
        response = self.client.delete(
            reverse('admin_document-detail', args=[self.document.id])
        )
        # Admin allowed to delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 0)

    # ---------------------------
    # List Test
    # ---------------------------
    def test_list_documents(self):
        Document.objects.create(title='Doc 1', user=self.admin_user)
        Document.objects.create(title='Doc 2', user=self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 3)

    # ---------------------------
    # Pagination Test
    # ---------------------------
    def test_pagination(self):
        for i in range(20):
            Document.objects.create(title=f'Doc {i}', user=self.admin_user)

        response = self.client.get(self.url + "?page=1&page_size=10")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    # ---------------------------
    # Filter Test
    # ---------------------------
    def test_filter_by_title(self):
        Document.objects.create(title='Special Title', user=self.admin_user)

        response = self.client.get(self.url + "?title=Special Title")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Special Title")

    # ---------------------------
    # Search Test
    # ---------------------------
    def test_search_by_title(self):
        Document.objects.create(title='Alpha Document', user=self.admin_user)
        Document.objects.create(title='Beta Document', user=self.admin_user)

        response = self.client.get(self.url + "?search=Alpha")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Alpha Document")

    # ---------------------------
    # Ordering Test
    # ---------------------------
    def test_ordering(self):
        d1 = Document.objects.create(title='A Title', user=self.admin_user)
        d2 = Document.objects.create(title='B Title', user=self.admin_user)

        response = self.client.get(self.url + "?ordering=title")

        titles = [item["title"] for item in response.data["results"]]

        self.assertEqual(titles, sorted(titles))

    # ---------------------------
    # Test Helper
    # ---------------------------
    @staticmethod
    def create_test_file(filename='test.txt', content=b'Test content'):
        return SimpleUploadedFile(filename, content, content_type='text/plain')
