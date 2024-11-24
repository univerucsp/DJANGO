# models.py
from django.db import models
import json

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='videos/')
    metadata = models.JSONField(default=dict)  # Campo para almacenar el JSON de metadatos

    def __str__(self):
        return self.title

