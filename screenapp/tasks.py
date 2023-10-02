from celery import Celery, shared_tasks
from django.db import models
from .models import ScreenVideo
import os
import subprocess
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage

#import openai


@shared_task
def process_video(video_id, new_video_data):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return

    if video.upload:
        existing_video_data = video.upload.read()

        # Process and concatenate videos here using MoviePy

        # Save the concatenated video data to the video model
        video.upload.save(f'video_{video.id}.mp4', ContentFile(concatenated_video_data))

        # Clean up temporary files
        os.remove(temp_file.name) 
    else:
        # If there's no existing video, use the new video data directly
        video.upload.save(f'video_{video.id}.mp4', ContentFile(new_video_data))


























app=Celery('screenrecords')
@app.task
def store_video_chunks():
    """Continuously stores video chunks from Redis in the database."""

    # Get the blob metadata chunk from Redis.
    blob_metadata_chunk = redis.get('video_metadata_data')

    # Create a new model instance with the given blob metadata chunk.
    model_instance = ScreenVideo(video_metadata_data=video_metadata_data)

    # Save the model instance to the database.
    model_instance.save()
    
def merge_video_chunks(video_chunks_path):

  # Merge the video chunks using the ffmpeg command-line tool.
  merged_video_path = os.path.join(video_chunks_path, 'merged.mp4')
  subprocess.run([
      'ffmpeg',
      '-i', os.path.join(video_chunks_path, '%d.mp4'),
      '-c:v', 'copy',
      '-c:a', 'copy',
      merged_video_path
  ])

  return merged_video_path

@app.task
def merge_and_upload_video(video_chunks_path):
  
  # Merge the video chunks.
  merged_video_path = merge_video_chunks(video_chunks_path)

  # Upload the merged video file to Django.
  with open(merged_video_path, 'rb') as f:
    default_storage.save('videos/merged.mp4', f)
"""
@app.task

def transcribe_video(video_id):
 

    # Get the video path.
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_id + '.mp4')

    # Transcribe the video using OpenAI Whisper.
    transcription = openai.whisper(video_path)

    # Save the transcription to the database.
    model_instance = ScreenVideo(transcription=transcription)
    model_instance.save()
"""

