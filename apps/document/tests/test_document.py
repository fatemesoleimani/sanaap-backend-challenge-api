from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.document.models import Document
from apps.user.choices import UserRoleChoices

User = get_user_model()


class DocumentViewSetTests(APITestCase):
    def setUp(self):
        # Create users
        self.viewer = User.objects.create_user(
            username='viewer', password='pass', role=UserRoleChoices.viewer
        )
        self.editor = User.objects.create_user(
            username='editor', password='pass', role=UserRoleChoices.editor
        )

        # Base URL
        self.list_url = reverse('document-list')

        # Pre-created document
        self.document = Document.objects.create(
            title="Initial Doc",
            file=self.create_file(),
            user=self.editor
        )

    # ----------------------------
    # Helper: create test file
    # ----------------------------
    @staticmethod
    def create_file(name="test.txt", content=b"test data"):
        return SimpleUploadedFile(name, content, content_type="text/plain")

    # ----------------------------
    # Viewer Test: LIST allowed
    # ----------------------------
    def test_viewer_can_list_documents(self):
        self.client.force_authenticate(self.viewer)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ----------------------------
    # Viewer Test: CREATE forbidden
    # ----------------------------
    def test_viewer_cannot_create_document(self):
        self.client.force_authenticate(self.viewer)
        data = {"title": "X", "file": self.create_file()}
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------
    # Editor Test: CREATE allowed
    # ----------------------------
    def test_editor_can_create_document(self):
        self.client.force_authenticate(self.editor)
        data = {"title": "New Doc", "file": self.create_file()}
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)

    # ----------------------------
    # Viewer Test: UPDATE forbidden
    # ----------------------------
    def test_viewer_cannot_update_document(self):
        self.client.force_authenticate(self.viewer)
        url = reverse('document-detail', args=[self.document.id])
        data = {"title": "Hacked Title"}
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------
    # Editor Test: UPDATE allowed
    # ----------------------------
    def test_editor_can_update_document(self):
        self.client.force_authenticate(self.editor)
        url = reverse('document-detail', args=[self.document.id])
        data = {"title": "Updated", "file": self.create_file("updated.txt")}
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.document.refresh_from_db()
        self.assertEqual(self.document.title, "Updated")

    # ----------------------------
    # Delete forbidden for all
    # ----------------------------
    def test_anyone_cannot_delete_document(self):
        for user in [self.viewer, self.editor]:
            self.client.force_authenticate(user)
            url = reverse('document-detail', args=[self.document.id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------
    # Pagination
    # ----------------------------
    def test_pagination(self):
        self.client.force_authenticate(self.viewer)

        for i in range(15):
            Document.objects.create(title=f"Doc {i}", user=self.editor)

        response = self.client.get(self.list_url + "?page=1&page_size=10")
        self.assertEqual(len(response.data["results"]), 10)

    # ----------------------------
    # Filter
    # ----------------------------
    def test_filter_by_title(self):
        self.client.force_authenticate(self.viewer)

        Document.objects.create(title="Special Title", user=self.editor)

        response = self.client.get(self.list_url + "?title=Special Title")
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Special Title")

    # ----------------------------
    # Search
    # ----------------------------
    def test_search_documents(self):
        self.client.force_authenticate(self.viewer)

        Document.objects.create(title="Alpha Doc", user=self.editor)
        Document.objects.create(title="Beta Doc", user=self.editor)

        response = self.client.get(self.list_url + "?search=Alpha")
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Alpha Doc")

    # ----------------------------
    # Ordering
    # ----------------------------
    def test_ordering_by_title(self):
        self.client.force_authenticate(self.viewer)

        Document.objects.create(title="B Doc", user=self.editor)
        Document.objects.create(title="A Doc", user=self.editor)

        response = self.client.get(self.list_url + "?ordering=title")
        titles = [obj["title"] for obj in response.data["results"]]
        self.assertEqual(titles, sorted(titles))
