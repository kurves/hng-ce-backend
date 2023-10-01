from rest_framework import serializers
from .models import ScreenVideo

class ScreenVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenVideo
        fields = "__all__"