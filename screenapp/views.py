from django.shortcuts import render
import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets,generics
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer

import pika
class ScreenVideoView(generics.ListCreateAPIView):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer


class ScreenVideoUploadView(APIView):


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
from rest_framework.views import APIView
from rest_framework.response import Response
import pika

class TranscribeVideoView(APIView):
    Transcribes a video using Whisper.

    def post(self, request):
        Accepts the video ID from the frontend and sends it to RabbitMQ.

        # Get the video ID from the request body.
        video_id = request.data['video_id']

        # Create a RabbitMQ connection.
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        # Create a RabbitMQ channel.
        channel = connection.channel()

        # Declare a RabbitMQ queue.
        channel.queue_declare(queue='video_transcriptions')

        # Publish the video ID to the RabbitMQ queue.
        channel.basic_publish(exchange='', routing_key='video_transcriptions', body=video_id)

        # Close the RabbitMQ connection.
        connection.close()

        # Return a response to the frontend.
        return Response({'status': 'success'})
        """