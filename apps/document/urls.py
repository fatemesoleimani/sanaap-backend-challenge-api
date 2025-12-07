from rest_framework.routers import DefaultRouter

from apps.document.views import DocumentViewSet

router = DefaultRouter()
router.register('', DocumentViewSet, basename='document')

urlpatterns = router.urls
