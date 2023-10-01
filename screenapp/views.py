from django.shortcuts import render
import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer

class ScreenVideoViewSet(viewsets.ModelViewSet):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer


"""class StartVideoUploadView(APIView):


    def post(self, request):


        # Get the video data from the request body.
        video_data = request.data
        redis.set('video_data', video_data)
        
        # Save the video data to a temporary location.
        with open(os.path.join(settings.MEDIA_ROOT, 'temp', 'video.mp4'), 'wb') as f:
            f.write(video_data.read())

        # Start the Celery task to continuously store the video data in the database in chunks.
        upload_video.delay(os.path.join(settings.MEDIA_ROOT, 'temp', 'video.mp4'))

        # Return a response to the frontend.
        return Response({'status': 'success'})

"""
