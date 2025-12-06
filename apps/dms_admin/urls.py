from rest_framework.routers import DefaultRouter

from apps.dms_admin.views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='admin_users')
router.register('document', DocumentAdminViewSet, basename='admin_document')

urlpatterns = router.urls
