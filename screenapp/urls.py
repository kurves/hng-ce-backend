from rest_framework.routers import DefaultRouter
from .views import ScreenVideoView,ScreenVideoUploadView
from . import views
from django.urls import path
router = DefaultRouter()
#router.register(r'screen-videos', ScreenVideoViewSet)

#urlpatterns = router.urls

urlpatterns=[
    path("api/",ScreenVideoView.as_view(),name="video-list"),
    path("api/upload", ScreenVideoUploadView.as_view(),name="upload")
   # path("api/transcribe",views.TranscribeVideoView.as_view(), name="tran")
]