# Automatizador de Descarga y Extracción de Audios de YouTube
Este proyecto consiste en una aplicación que automatiza la descarga de vídeos de cinco canales de YouTube y extrae los audios correspondientes. En total, se descargan 25 vídeos y se obtienen 25 audios.
# Lógica de la Aplicación
El funcionamiento de la aplicación sigue estos pasos:
1. Obtención de URLs de los Vídeos: La aplicación recopila las URLs de los vídeos de los cinco canales de YouTube especificados.
2. Descarga de Vídeos: Utilizando la herramienta yt-dlp, la aplicación descarga los vídeos correspondientes a las URLs recopiladas.
3. Extracción de Audios: Una vez descargados los vídeos, la aplicación utiliza ffmpeg para extraer el audio de cada uno de ellos.
4. Guardado de Audios: Los audios extraídos se guardan en el sistema de archivos local, listos para su posterior uso.
# Requisitos
para ejecutar esta aplicación, necesitarás tener instalado los siguientes programas:
- python3: lenguaje de programación
- yt-dlp: Herramienta de línea de comandos para descargar vídeos de YouTube 
- ffmpeg: Utilizado para extraer el audio de los vídeos descargados
Ambas herramientas están disponibles para sistemas operativos Linux y Windows
# Instalacion en Linux
## yt-dlp
Puedes instalar yt-dlp en Linux utilizando pip:
```pip install yt-dlp```
## ffmpeg
Puedes instalar ffmpeg en Linux utilizando el gestor de paquetes de tu distribución. Por ejemplo, en Ubuntu y otras distribuciones basadas en Debian, puedes usar apt:
```sudo apt install ffmpeg```
# Instalación en Windows
## yt-dlp
Para instalar yt-dlp en Windows, puedes utilizar pip desde la línea de comandos:
```pip install yt-dlp```
## ffmpeg
Para instalar ffmpeg en Windows, puedes descargar el paquete binario desde el sitio web oficial de ffmpeg (https://ffmpeg.org/download.html) y seguir las instrucciones de instalación proporcionadas.
No olvides agregar ffmpeg en el PATH.
# Uso
1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener instalados yt-dlp y ffmpeg en tu sistema.
3. Abre una terminal y navega hasta el directorio del proyecto.
4. Ejecuta el script que desees ejeucutar ya sea la version para Linux o Windows.
# Funcionamiento
Los scripts utilizan yt-dlp para descargar los vídeos de los cinco canales de YouTube especificados. Luego, utiliza ffmpeg para extraer el audio de los vídeos descargados.
# Notas
- Si el script tiene 'L' es para la version de Linux.
- Si el script tiene 'W' es para la version de Windows.
- Existe 3 scripts: secuencial, multithreading, multiprocessing.
- En el script de multithreading y multiprocessing puedes cambiar el numero de hilos de uso en la variable nh
# Integrantes:
- Lenin Esteban Carabali Moreno 2310025-3743 lenin.carabali@correounivalle.edu.co
- Wilson Camilo Garces Zuñiga 2310105-3743 garces.wilson@correounivalle.edu.co
