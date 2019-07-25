from django.db import models

class UserVideoMapping(models.Model):
    user_id = models.IntegerField()
    video_name = models.CharField(max_length=200)
    video_size = models.IntegerField()