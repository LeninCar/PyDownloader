import subprocess
import os

def descargar_video(url, directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    comando_descarga = ['yt-dlp', '-o', f'{directorio_destino}/%(title)s.%(ext)s', url]
    subprocess.run(comando_descarga)

def extraer_audio(titulo_video, video_path, directorio_destino):
    audio_path = f'{directorio_destino}/{titulo_video}.mp3'
    # print(f'Extrayendo audio de {video_path} aaaaaaaaa {audio_path}')
    comando_extraccion = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', audio_path]
    subprocess.run(comando_extraccion)
    os.remove(video_path)

# URL del nuevo vídeo de YouTube a descargar
url_video = "https://www.youtube.com/watch?v=sOS9aOIXPEk"

# Directorio donde se guardarán los archivos descargados
directorio_destino = "/home/lecm/Videos"

# Descargar el vídeo
descargar_video(url_video, directorio_destino)

comando_info_video = ['yt-dlp', '-e', url_video]
titulo_video = subprocess.check_output(comando_info_video, text=True).strip()

# Obtener la ruta del vídeo descargado
ruta_video = f'{directorio_destino}/{titulo_video}.webm'

# Extraer el audio del vídeo descargado
extraer_audio(titulo_video, ruta_video, directorio_destino)
