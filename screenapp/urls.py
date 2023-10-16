from rest_framework.routers import DefaultRouter
from .views import ScreenVideoView
from . import views
from django.urls import path
router = DefaultRouter()
#router.register(r'screen-videos', ScreenVideoViewSet)

#urlpatterns = router.urls

urlpatterns=[
    path("api/",ScreenVideoView.as_view(),name="video-list"),
    path("api/upload",views.create_video,name="create-video"),
    path('api/get_video/<video_id>/', views.get_video, name='get_video'),
    path('api/extract_audio/<video_id>', views.extract_audio, name="extract audio"),
    path('api/transcribe/<video_id>/', views.transcribe_video, name='_video'),
]