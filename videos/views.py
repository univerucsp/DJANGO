# views.py
import os
import json
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Video
from .forms import VideoUploadForm

def video_list(request):
    # Cargar el archivo JSON con todos los metadatos de los videos
    metadata_path = os.path.join(settings.MEDIA_ROOT, 'metadata', 'videos_metadata.json')
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        videos = metadata.get("videos", [])
    else:
        videos = []

    # Filtrar videos por búsqueda (por ejemplo, por label, color o confidence)
    query = request.GET.get('search', '')
    filtered_videos = []

    if query:
        # Dividir la búsqueda en términos individuales
        query_terms = [term.strip().lower() for term in query.split(',')]
        
        for video in videos:
            # Filtrar si todas las condiciones de búsqueda se cumplen
            video_matches = True
            for term in query_terms:
                term_found = False  # Flag para saber si encontramos el término

                # Buscar si el término está en el label, colors o confidence
                for frame in video["frames"]:
                    for detection in frame["detections"]:
                        if (term in detection["label"].lower() or 
                            any(term in color.lower() for color in detection.get("colors", []))):
                            term_found = True
                            break
                    if term_found:
                        break
                
                if not term_found:
                    video_matches = False
                    break

            if video_matches:
                filtered_videos.append(video)
    else:
        # Si no hay búsqueda, mostramos todos los videos
        filtered_videos = videos

    # Manejar la subida de nuevos videos
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()  # Guarda el video en la base de datos

            # Actualizar el archivo JSON con los metadatos del nuevo video
            new_video_metadata = {
                "video_name": video.file.name,
                "video_path": video.file.url,
                "frames": []  # Podrías agregar frames aquí si lo necesitas
            }

            # Cargar el archivo JSON existente, agregar el nuevo video y guardar
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {"videos": []}

            metadata['videos'].append(new_video_metadata)

            # Guardar el archivo JSON con los metadatos actualizados
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)

            return redirect('video_list')  # Redirige a la lista de videos después de la carga
    else:
        form = VideoUploadForm()

    return render(request, 'videos/video_list.html', {'videos': videos, 'form': form, 'query': query, 'filtered_videos': filtered_videos})

