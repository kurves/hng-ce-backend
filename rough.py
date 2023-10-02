from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseNotFound, HttpResponse
from .models import Video
import tempfile
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import whisper
import tempfile
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import whisper
from celery import shared_task
from .tasks import transcribe_video

# Create your views here.




#views.py
@api_view(['POST'])
def create_video(request):
    video = Video.objects.create()
    return Response({'video_id': video.id}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def append_video(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return HttpResponseNotFound("Video not found")

    # Check if the request contains a body with data
    if not request.body:
        return Response({'error': 'No video data provided'}, status=status.HTTP_400_BAD_REQUEST)

    new_video_data = request.body

    if video.upload:
        # Read the existing video data
        existing_video_data = video.upload.read()

        # Create temporary files to save the video data
        with tempfile.NamedTemporaryFile(delete=False) as existing_tempfile:
            existing_tempfile.write(existing_video_data)
            existing_tempfile_path = existing_tempfile.name

        with tempfile.NamedTemporaryFile(delete=False) as new_tempfile:
            new_tempfile.write(new_video_data)
            new_tempfile_path = new_tempfile.name

        # Create VideoFileClip objects from the temporary files
        existing_clip = VideoFileClip(existing_tempfile_path)
        new_clip = VideoFileClip(new_tempfile_path)

        # Concatenate the video clips
        final_clip = concatenate_videoclips([existing_clip, new_clip])

        # Save the concatenated video data to the video model
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as final_tempfile:
            final_clip.write_videofile(final_tempfile.name, codec='libx264')
            final_tempfile_path = final_tempfile.name

        video.upload.save(f'video_{video.id}.mp4', ContentFile(open(final_tempfile_path, 'rb').read()))

        # Clean up temporary files
        os.remove(existing_tempfile_path)
        os.remove(new_tempfile_path)
        os.remove(final_tempfile_path)

        return Response({'message': 'Video appended and joined successfully'}, status=status.HTTP_200_OK)
    else:
        # If there's no existing video, use the new video data directly
        video.upload.save(f'video_{video.id}.mp4', ContentFile(new_video_data))
        return Response({'message': 'Video added successfully'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_video(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return HttpResponseNotFound("Video not found")

    if not video.upload:
        return Response({'error': 'No video data associated with this video ID'}, status=status.HTTP_400_BAD_REQUEST)

    video_data = video.upload.read()
    response = HttpResponse(video_data, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="video_{video.id}.mp4"'
    return response


   return Response({'video_id': video.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

