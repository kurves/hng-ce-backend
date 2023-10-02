from rest_framework import serializers
from .models import ScreenVideo

class ScreenVideoSerializer(serializers.Serializer):
    recordingChunk=serializers.FileField()