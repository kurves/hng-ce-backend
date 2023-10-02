from rest_framework.routers import DefaultRouter
from .views import ScreenVideoView
from . import views
from django.urls import path
router = DefaultRouter()
#router.register(r'screen-videos', ScreenVideoViewSet)

#urlpatterns = router.urls

urlpatterns=[
    path("api/",ScreenVideoView.as_view(),name="video-list"),
    path("api/upload", views.append_video,name="upload"),
    path("api/upload",views.create_video,name="create-video")
   # path("api/transcribe",views.TranscribeVideoView.as_view(), name="tran")
]