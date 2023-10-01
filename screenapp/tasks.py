from celery import Celery
from django.db import models

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
            model_instance = MyModel(video_data=chunk)
            model_instance.save()

    # Delete the video file from the temporary location.
    os.remove(video_path)