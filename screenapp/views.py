from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets,generics
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer
import tempfile
import os
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.decorators import api_view
from moviepy.editor import VideoFileClip, concatenate_videoclips
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
import pika

class ScreenVideoView(generics.ListCreateAPIView):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer


@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt, name='dispatch')  # Add this decorator if needed
def create_video(request):
    video = ScreenVideo.objects.create()
    response = Response({'video_id': video.id}, status=status.HTTP_201_CREATED)
    response["Access-Control-Allow-Origin"] = "*"  # Replace * with the allowed origin
    return response


class ScreenVideoUploadView(APIView):  
    def post(self, request):
        try:
            # Get the video data from the request body.
            video_chunk = request.GET['recordingchunk']
            temp_file= tempfile.NamedTemporaryFile(delete=False,suffix='.mp4') 
            for chunk in video_data.chunks():
                temp_file.write(chunk)  
            temp_file.close
            
            video = Video(title=request.data('title'))
            video.video_file.save(os.path.basename(temp_file.name), temp_file)

            os.remove(temp_file.name)  # Remove the temporary file


            # Start the Celery task to continuously store the video data in the database in chunks.
            upload_video.delay(os.path.join(settings.MEDIA_ROOT, 'temp', 'video.mp4'))

            # Return a response to the frontend.
            return Response({'status': 'success'},{'path':f.name})

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_video(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    if not video.upload:
        return Response({'error': 'No video data associated with this video ID'}, status=status.HTTP_400_BAD_REQUEST)

    video_data = video.upload.read()
    response = HttpResponse(video_data, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="video_{video.id}.mp4"'
    return response





class TranscribeVideoView(APIView):
 

    def post(self, request):


        video_id = request.data['video_id']

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        
        channel = connection.channel()

        # Declare a RabbitMQ queue.
        channel.queue_declare(queue='video_transcriptions')

        # Publish the video ID to the RabbitMQ queue.
        channel.basic_publish(exchange='', routing_key='video_transcriptions', body=video_id)

        # Close the RabbitMQ connection.
        connection.close()

        
        return Response({'status': 'success'})
        