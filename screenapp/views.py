from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer

class ScreenVideoViewSet(viewsets.ModelViewSet):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer