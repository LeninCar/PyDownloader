import subprocess
import os

###################### Opción en la que no se usa la herrameinta ffmpeg ########################s

def descargar_video(url, directorio_destino, nombre_personalizado):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    comando_descarga = ['yt-dlp', '-x', '-o', f'{directorio_destino}/{nombre_personalizado}', '--audio-format', 'mp3', url] # sólo audio, formato mp3
    subprocess.run(comando_descarga)

# URL del nuevo vídeo de YouTube a descargar
url_video = "https://www.youtube.com/watch?v=tdwWhVCrQhU"

# Directorio donde se guardarán los archivos descargados
directorio_destino = "/home/lecm/Videos"

comando_info_video = ['yt-dlp', '-e', url_video]

titulo_video = subprocess.check_output(comando_info_video, text=True).strip()
titulo_video = titulo_video.replace("-", "")


# Descargar el vídeo
descargar_video(url_video, directorio_destino,titulo_video)
