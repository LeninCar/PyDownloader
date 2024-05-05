import subprocess
import os
import re
import json
import csv
from datetime import datetime
import threading

NH = 4  # Número de hilos
NV = str(5)  # Número de vídeos

def descargar_video(url, directorio_destino, nombre_personalizado):
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

def obtener_nombres_urls(url_canal):
    comando = ['yt-dlp', '--no-warnings', '--flat-playlist', '-e', '-g', '--playlist-end', '5', url_canal]
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

def procesar_videos(ih, nh, nombres_videos, urls_videos, directorio_destino):
    for i in range(ih, len(nombres_videos), nh):
        nombre_video = nombres_videos[i]
        nombre_video = limpiar_caracteres_especiales(nombre_video)
        url_video = urls_videos[i]

        extension = subprocess.check_output(['yt-dlp', '--no-warnings', '--flat-playlist', '--get-filename', '-o', '%(ext)s', url_video], text=True).strip()

        # Descargar el vídeo
        descargar_video(url_video, directorio_destino, nombre_video)

        # Obtener la ruta del vídeo descargado
        video_path = f'{directorio_destino}/{nombre_video}.{extension}'

        fecha_publicacion = obtener_fecha_publicacion(url_video)
        fecha_descarga = datetime.now().date()
        
        # Extraer el audio del vídeo
        extraer_audio(nombre_video, video_path, directorio_destino)

        with open(registro_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nombre_video, fecha_publicacion, str(fecha_descarga)])

nombres_videos = []
urls_videos = []
threads = []

if __name__ == '__main__':
    # URL del nuevo vídeo de YouTube a descargar
    # url_canal = "https://www.youtube.com/@TEDEdEspanol"

    with open('../canales.json', 'r') as file:
        data = json.load(file)

    directorio_destino = os.path.expanduser('~/Audios')
    registro_csv = os.path.join(directorio_destino, 'registro_audios.csv')

    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Verificar si el archivo CSV existe
    if not os.path.exists(registro_csv):
        # Crear el archivo CSV con los encabezados
        with open(registro_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Título del Video', 'Fecha de Publicación', 'Fecha de Descarga'])

    for canal in data:
        nombre_canal = canal['nombre']
        url_canal = canal['url']

        obtener_nombres_urls(url_canal)

    start_time = datetime.now()

    for i in range(NH):
        # Crear un hilo con la función 'procesar_videos'
        thread = threading.Thread(target=procesar_videos, args=(i, NH, nombres_videos, urls_videos, directorio_destino))
        # Comenzar el hilo
        thread.start()
        # Adicionar el hilo a la lista de hilos
        threads.append(thread)

    for thread in threads:
        # Esperar a que todos los hilos terminen
        thread.join()

    end_time = datetime.now()

    total_time = end_time - start_time
    
    print("###################### El tiempo total fue de: " + str(total_time.total_seconds()))


    