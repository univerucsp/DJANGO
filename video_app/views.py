# video_app/views.py

import os
from django.conf import settings
from django.shortcuts import render
from .models import Video  # Asegúrate de que el modelo Video esté importado

def video_list(request):
    # Obtener todos los videos almacenados en la base de datos
    videos = Video.objects.all()  # Asumiendo que has creado el modelo Video
    return render(request, 'videos/video_list.html', {'videos': videos})

