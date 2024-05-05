import subprocess
import os
import re
import json
import csv
from datetime import datetime

NV = str(5)  # Número de vídeos

def descargar_video(url, directorio_destino, nombre_personalizado):
    comando_descarga = ['yt-dlp','--no-warnings', '-S', 'res:360','-o', f'{directorio_destino}/{nombre_personalizado}', url]
    subprocess.run(comando_descarga)

def extraer_audio(titulo_video, video_path, directorio_destino):
    audio_path = f'{directorio_destino}\\{titulo_video}.mp3'
    comando_extraccion = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', audio_path]
    subprocess.run(comando_extraccion)
    os.remove(video_path)

def obtener_fecha_publicacion(url_video):
    comando_fecha = subprocess.check_output(['yt-dlp','--no-warnings', '--no-warnings','--get-filename', '-o' ,'%(upload_date)s', url_video], text=True)
    fecha_str = comando_fecha.strip()
    fecha_publicacion = datetime.strptime(fecha_str, '%Y%m%d').date()  # Formato de fecha en YT: AAAAMMDD
    return fecha_publicacion

def obtener_nombres_urls(url_canal):
    comando = ['yt-dlp', '--no-warnings', '--flat-playlist', '-e', '-g', '--playlist-end', NV , url_canal]
    salida = subprocess.check_output(comando, text=True).strip().split('\n')

    for i in range(0, len(salida), 2):
        nombres_videos.append(salida[i])
        urls_videos.append(salida[i + 1])
        
def limpiar_caracteres_especiales(texto):
    # Definir un patrón de expresión regular para buscar caracteres especiales
    patron = re.compile(r'[^\w\s]')
    # Reemplazar los caracteres especiales con una cadena vacía
    texto_limpio = patron.sub('', texto)
    return texto_limpio

nombres_videos = []
urls_videos = []

if __name__ == '__main__':
    # URL del nuevo vídeo de YouTube a descargar
    # url_canal = "https://www.youtube.com/@TEDEdEspanol"

    with open('../canales.json', 'r') as file:
        data = json.load(file)

    directorio_destino = os.path.expanduser('~\\Audios')
    registro_csv = os.path.join(directorio_destino, 'registro_audios.csv')

    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Verificar si el archivo CSV existe
    if not os.path.exists(registro_csv):
        # Crear el archivo CSV con los encabezados
        with open(registro_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título del Video', 'Fecha de Publicación', 'Fecha de Descarga'])
            
    for canal in data:
        nombre_canal = canal['nombre']
        url_canal = canal['url']

        obtener_nombres_urls(url_canal)

    start_time = datetime.now()


    for titulo_video, url_video in zip(nombres_videos, urls_videos):

        extension = subprocess.check_output(['yt-dlp', '--no-warnings', '--flat-playlist', '--get-filename', '-o', '%(ext)s', url_video], text=True).strip()

        titulo_video = limpiar_caracteres_especiales(titulo_video)
        # Descargar el vídeo
        descargar_video(url_video, directorio_destino, titulo_video)

        # Obtener la ruta del vídeo descargado
        video_path = f'{directorio_destino}\\{titulo_video}.{extension}'

        fecha_publicacion = obtener_fecha_publicacion(url_video)
        fecha_descarga = datetime.now().date()

        # Extraer el audio del vídeo
        extraer_audio(titulo_video, video_path, directorio_destino)

        with open(registro_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([titulo_video, fecha_publicacion, str(fecha_descarga)])

    end_time = datetime.now()

    total_time = end_time - start_time

    print("###################### El tiempo total fue de: " + str(total_time.total_seconds()))
