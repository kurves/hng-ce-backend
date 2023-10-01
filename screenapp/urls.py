from rest_framework.routers import DefaultRouter
from . import views

from django.urls import path
router = DefaultRouter()
router.register(r'screen-videos', views.ScreenVideoViewSet)



urlpatterns=[
    #home page
    #path('', views.index, name='index'),
    #path('api',views.PersonListView.as_view(),name='Person-list'),
    path('api/upload',views.StartVideoUploadView.as_view(),name='create-video'),
   # path('api/<str:name>', views.PersonRetrieveByName.as_view(),name="Retrieve-Person-by-name")
   
]