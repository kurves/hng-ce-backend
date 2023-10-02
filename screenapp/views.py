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
class ScreenVideoView(generics.ListCreateAPIView):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer

"""
class ScreenVideoUploadView(APIView):
    parser_classes = (MultiPartParser,)

"""   



@api_view(['GET','POST'])
def create_video(request):
    video = ScreenVideo.objects.create()
    return Response({'video_id': video.id}, status=status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def append_video(request,video_id):
     
    try:
        video = ScreenVideo.objects.get(pk=video_id)
    except ScreenVideo.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    if not request.data:
        return Response({'error': 'No video data provided'}, status=status.HTTP_400_BAD_REQUEST)
    new_video_data = request.data.get('upload')

    process_video.delay(video_id, request.data)


    if video.upload:
        recording = ScreenVideo.objects.create()
        recording.recordingChunk.save(recording_chunk.name,recording_chunk)
        existing_video_data = video.upload.read()

        with tempfile.NamedTemporaryFile(delete=False) as existing_tempfile:
            existing_tempfile.write(existing_video_data)
            existing_tempfile_path = existing_tempfile.name

        with tempfile.NamedTemporaryFile(delete=False) as new_tempfile:
            new_tempfile.write(new_video_data.read())
            new_tempfile_path = new_tempfile.name

        existing_clip = VideoFileClip(existing_tempfile_path)
        new_clip = VideoFileClip(new_tempfile_path)
        final_clip = concatenate_videoclips([existing_clip, new_clip])

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as final_tempfile:
            final_clip.write_videofile(final_tempfile.name, codec='libx264')
            final_tempfile_path = final_tempfile.name

        video.upload.save(f'video_{video.id}.mp4', ContentFile(open(final_tempfile_path, 'rb').read()))

        os.remove(existing_tempfile_path)
        os.remove(new_tempfile_path)
        os.remove(final_tempfile_path)

        return Response({'message': 'Video appended and joined successfully'}, status=status.HTTP_200_OK)
    else:
        video.upload.save(f'video_{video.id}.mp4', ContentFile(new_video_data.read()))
        return Response({'message': 'Video added successfully'}, status=status.HTTP_200_OK)

    """ 

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
"""


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