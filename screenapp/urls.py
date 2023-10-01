from rest_framework.routers import DefaultRouter
from .views import ScreenVideoViewSet

router = DefaultRouter()
router.register(r'screen-videos', ScreenVideoViewSet)

urlpatterns = router.urls