from django.db import models


class Entry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Audio(models.Model):
    file = models.FileField(upload_to="audio/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
