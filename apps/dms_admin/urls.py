from rest_framework.routers import DefaultRouter

from apps.dms_admin.views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
