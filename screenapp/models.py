from django.db import models
import uuid

# Create your models here.
class ScreenVideo(models.Model):
    #video_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file=models.FileField(upload_to="recorded_videos/")
    timestamp=models.DateTimeField(auto_now_add=True)
    transcription=models.TextField(blank=True,)

    def __str__(self):
        return str(self.id)
