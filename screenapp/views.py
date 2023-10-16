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
from django.http import HttpResponse
#from drf_yasg.views import extend_schema



class ScreenVideoView(generics.ListCreateAPIView):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer

#@extend_schema(request=XSerializer, responses=XSerializer)
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
            video = ScreenVideo.objects.get(pk=serializer.instance.id)
            transcript=transcribe_video(video.video_file.path)
            video.trancription=transcript
            video.save()
            os.remove(temp_file.name)  # Remove the temporary file


            # Start the Celery task to continuously store the video data in the database in chunks.
            upload_video.delay(os.path.join(settings.MEDIA_ROOT, 'temp', 'video.mp4'))

            # Return a response to the frontend.
            return Response({'status': 'success'},{'path':f.name})

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(request=XSerializer, responses=XSerializer)
@api_view(['GET'])
def get_video(request, video_id):
    try:
        video = ScreenVideo.objects.get(pk=video_id)
    except ScreenVideo.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    if not video.video_file:
        return Response({'error': 'No video data associated with this video ID'}, status=status.HTTP_400_BAD_REQUEST)

    video_data = video.video_file.read()
    response = HttpResponse(video_data, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="video_{video.id}.mp4"'
    return response


 # Extracting audio from video

def extract_audio(request,video_id):
    video_path=request.data['video_file']
    video= VideoFileClip(video_path)

    audio=video.audio
    temp_file= tempfile.NamedTemporaryFile(delete=False,suffix='.mp3') 
    audio.write_audiofile(temp_file)
    video.close()
    audio.close()

@api_view(['GET'])
def transcribe_video(request, video_id):
  
    video = ScreenVideo.objects.get(pk=video_id)

    

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    
    channel = connection.channel()

    # Declare a RabbitMQ queue.
    channel.queue_declare(queue='video_transcriptions')

    # Publish the video ID to the RabbitMQ queue.
    channel.basic_publish(exchange='', routing_key='video_transcriptions', body=video_id)

    # Close the RabbitMQ connection.
    connection.close()

    
    return Response(data,{'status': 'success'})
    

       
       