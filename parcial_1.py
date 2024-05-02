import subprocess
import os
import json
from datetime import datetime
import threading

def descargar_video(url, directorio_destino, nombre_personalizado):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    comando_descarga = ['yt-dlp','--no-warnings', '-S', 'res:360','-o', f'{directorio_destino}/{nombre_personalizado}', url]
    subprocess.run(comando_descarga)

def extraer_audio(titulo_video, video_path, directorio_destino):
    audio_path = f'{directorio_destino}/{titulo_video}.mp3'
    comando_extraccion = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', audio_path]
    subprocess.run(comando_extraccion)
    os.remove(video_path)

def obtener_fecha_publicacion(url_video):
    comando_fecha = subprocess.check_output(['yt-dlp','--no-warnings', '--no-warnings','--get-filename', '-o' ,'%(upload_date)s', url_video], text=True)
    fecha_str = comando_fecha.strip()
    fecha_publicacion = datetime.strptime(fecha_str, '%Y%m%d').date()  # Formato de fecha en YT: AAAAMMDD
    return fecha_publicacion

if __name__ == '__main__':
    # URL del nuevo vídeo de YouTube a descargar
    # url_canal = "https://www.youtube.com/@TEDEdEspanol"

    with open('canales.json', 'r') as file:
        data = json.load(file)

    # Directorio donde se guardarán los archivos descargados
    directorio_destino = "/home/lecm/Videos"

    for canal in data:

        nombre_canal = canal['nombre']
        url_canal = canal['url']
        
        print("##" * 25)
        print("##" + " " * 5 + f'Descargando vídeos de {nombre_canal}...')
        print("##" * 25)

        comando_nombre = subprocess.check_output(['yt-dlp','--no-warnings', '--flat-playlist', '-e', '--playlist-end', '2', url_canal], text=True)

        array_titulos = comando_nombre.strip().split('\n')

        comando_urls = subprocess.check_output(['yt-dlp', '--no-warnings', '--flat-playlist', '-g', '--playlist-end', '2', url_canal], text=True)

        array_urls = comando_urls.strip().split('\n')

        for titulo_video, url_video in zip(array_titulos, array_urls):

            extension = subprocess.check_output(['yt-dlp', '--no-warnings', '--flat-playlist', '--get-filename', '-o', '%(ext)s', url_video], text=True).strip()

            titulo_video = titulo_video.replace("-", "").replace(",", "").replace("!", "")
            # Descargar el vídeo
            # descargar_video(url_video, directorio_destino, titulo_video)

            # Obtener la ruta del vídeo descargado
            video_path = f'{directorio_destino}/{titulo_video}.{extension}'

            fecha_publicacion = obtener_fecha_publicacion(url_video)
            fecha_descarga = datetime.now().date()
            print(f'Video: {titulo_video} - Fecha de publicación en YouTube: {fecha_publicacion} - Fecha de descarga: {fecha_descarga}')

            # Extraer el audio del vídeo
            # extraer_audio(titulo_video, video_path, directorio_destino)

        
        print(f'Vídeos de {nombre_canal} descargados correctamente.\n')
