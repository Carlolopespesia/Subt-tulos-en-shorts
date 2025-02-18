# 🎬 Proyecto de Transcripción y Subtitulación de Videos

Este proyecto automatiza la transcripción de audio, la generación de subtítulos y la integración de los mismos en un video con estilos personalizados. Se basa en `MoviePy`, `Whisper` de OpenAI y `FFmpeg`.

---

## 📌 Características

- Convierte archivos de audio (MP3) a formato WAV.
- Transcribe automáticamente el audio a texto utilizando `Whisper`.
- Genera un archivo de subtítulos en formato `.ass`.
- Aplica estilos personalizados a los subtítulos.
- Inserta los subtítulos en el video con `MoviePy`.
- Ajusta la longitud de los subtítulos sin romper palabras.

---

## ⚙️ Requisitos

### 🔹 Dependencias necesarias

Asegúrate de instalar los siguientes paquetes antes de ejecutar el script:

```sh
pip install moviepy openai-whisper ffmpeg-python numpy
```

### 🔹 Instalación de `ffmpeg`

Para que `MoviePy` y `ffmpeg-python` funcionen correctamente, asegúrate de tener `FFmpeg` instalado:

- **Windows:** Descarga e instala [FFmpeg](https://ffmpeg.org/download.html) y agrégalo al `PATH`.
- **MacOS/Linux:** Instálalo con:
  ```sh
  sudo apt install ffmpeg  # Debian/Ubuntu
  brew install ffmpeg  # macOS (Homebrew)
  ```

---

## 🚀 Uso del Proyecto

### 🔹 1. Convertir audio MP3 a WAV

El script convierte automáticamente el archivo de audio MP3 a WAV utilizando `ffmpeg`.

### 🔹 2. Transcribir el audio a texto

Se usa `Whisper` para transcribir el audio y generar subtítulos.

### 🔹 3. Generar subtítulos en formato `.ass`

Los segmentos de audio transcritos se convierten en subtítulos formateados en `.ass`.

### 🔹 4. Aplicar subtítulos al video

El script procesa los subtítulos, aplica estilos definidos y los inserta en el video final.

---

## 📄 Ejecución

Coloca los archivos del video y audio en la carpeta del proyecto y ejecuta el script principal:

```sh
python script.py
```

El video subtitulado se guardará como `LOKURAAAxd.mp4`.

---

## 🎨 Personalización de estilos

Puedes modificar los estilos en el diccionario `styles` dentro del script:

```python
styles = {
    "Default": {
        "fontname": "Arial",
        "fontsize": 80,
        "color": "yellow",
        "outline_color": "orange",
        "shadow_color": "White",
        "bold": True,
        "italic": False
    }
}
```

---

## 📢 Contribución

Si quieres mejorar este proyecto, siéntete libre de hacer un **fork** y enviar un **pull request**. ¡Las mejoras siempre son bienvenidas! 😊

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Puedes usarlo y modificarlo libremente.

---

✨ **¡Gracias por usar este proyecto!** 🚀

