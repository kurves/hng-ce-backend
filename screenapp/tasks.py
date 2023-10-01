from celery import Celery
from django.db import models
from .models import 

import openai

app=Celery('screenrecords')
@app.task
def upload_video(video_path):
    """Uploads the video to the database in chunks."""

    # Open the video file.
    with open(video_path, 'rb') as f:
        # Read the video data in chunks.
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break

            # Save the chunk to the database.
            model_instance = ScreenVideo(video_data=chunk)
            model_instance.save()

    # Delete the video file from the temporary location.
    os.remove(video_path)


@app.task
def transcribe_video(video_id):
    """Transcribes a video using OpenAI Whisper."""

    # Get the video path.
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_id + '.mp4')

    # Transcribe the video using OpenAI Whisper.
    transcription = openai.whisper(video_path)

    # Save the transcription to the database.
    model_instance = ScreenVideo(transcription=transcription)
    model_instance.save()

