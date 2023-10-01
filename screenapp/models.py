from django.db import models

# Create your models here.



class ScreenVideo(models.Model):
    title=models.CharField(max_length=100)
    video_file=models.FileField(upload_to="recorded_videos/")
    timestamp=models.DateTimeField(auto_now_add=True)
    transcription=models.TextField(blank=True,)

    def __str__(self):
        return self.title
