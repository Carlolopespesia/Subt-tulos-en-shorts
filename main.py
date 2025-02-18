import moviepy.editor as mp
import re
import whisper
import os
import subprocess
import datetime

# Define las rutas de los archivos
video_path = "Mi_video_poxo.mp4"
subtitles_path = "subtitulos_poxo.ass"
final_output_path = "LOKURAAAxd.mp4"
mp3_file = "Mi_video.mp3"
wav_file = "lel.wav"
text_file = "subtitulos.txt"
working_dir = "."

# Estilos definidos directamente en el script
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
    # Puedes agregar más estilos aquí si es necesario
}

# Función para parsear el archivo .ass y extraer los subtítulos
def parse_ass(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    events = []
    for line in lines:
        if line.strip().startswith("Dialogue:"):
            parts = line.split(",", 9)
            start_time = parts[1].strip()
            end_time = parts[2].strip()
            style = parts[3].strip()
            text = parts[9].strip().replace("\\N", "\n")
            text = split_text(text, 25)  # Ajustar el texto
            events.append(((start_time, end_time), text, style))

    return events

# Función para dividir el texto en líneas de máximo n caracteres sin romper palabras
def split_text(text, n):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_line) > n:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)

# Convertir el tiempo en formato "h:mm:ss.cs" a segundos
def time_to_seconds(time_str):
    h, m, s = re.split("[:.]", time_str)[:3]
    ms = re.split("[:.]", time_str)[-1]
    return int(h) * 3600 + int(m) * 60 + int(s) + float('0.' + ms)

# Función para generar un clip de texto con los estilos aplicados
def create_text_clip(txt, style, start, end):
    return (mp.TextClip(txt,
                       font=style.get("fontname", "Arial"),
                       fontsize=style.get("fontsize", 24),
                       color=style.get("color", "yellow"),
                       stroke_color=style.get("outline_color", "black"),
                       stroke_width=2,
                       method='caption',
                       size=(1280 - 40, None),  # Reduce el ancho del texto para que no se salga del video
                       align='center')
            .set_start(start)
            .set_end(end)
            .set_position(('center', 'bottom'), relative=False)
            .margin(bottom=20, opacity=0))  # Ajusta el margen inferior

# Función para convertir MP3 a WAV
def convert_mp3_to_wav(mp3_file, wav_file):
    try:
        subprocess.run(['ffmpeg', '-i', mp3_file, wav_file], check=True)
        print(f"Conversión exitosa de {mp3_file} a {wav_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error en la conversión: {e}")

# Función para transcribir audio a texto
def transcribe_audio_to_text(audio_file, text_file):
    if not os.path.exists(audio_file):
        print(f"El archivo de audio {audio_file} no existe.")
        return

    model = whisper.load_model("medium")
    result = model.transcribe(audio_file)

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    return result["segments"]

# Función para crear archivo ASS
def create_ass(segments, ass_file):
    def format_time(seconds):
        td = datetime.timedelta(seconds=seconds)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{int(td.total_seconds() // 3600):01d}:{int((td.total_seconds() % 3600) // 60):02d}:{int(td.total_seconds() % 60):02d}.{ms:03d}"

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(
             """
                [Script Info]
                Title: Generated Subtitles
                ScriptType: v4.00+
                WrapStyle: 0
                ScaledBorderAndShadow: yes
                YCbCr Matrix: None

                [Aegisub Project Garbage]
                Last Style Storage: Default
                Active Line: 0

                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
                Style: Default,Arial,11,&H00FFFF,&H000000FF,&H00000000,&H00FFFFFF,1,0,0,0,100,100,0,0,1,1,2,2,10,10,10,1

                [Events]
                Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                """
        )
        for i, segment in enumerate(segments):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"].strip().replace('\n', ' ')
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n\t\t\t\t")

# Función para agregar subtítulos al video
def add_subtitles_to_video(video_file, ass_file, output_file, working_dir):
    try:
        os.chdir(working_dir)
        video_file = os.path.basename(video_file)
        ass_file = os.path.basename(ass_file)
        output_file = os.path.basename(output_file)

        command = ['ffmpeg', '-i', video_file, '-vf', f"ass={ass_file}", output_file]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"Subtítulos agregados a {video_file} y guardados en {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error al agregar subtítulos: {e}")

# Main script execution
if __name__ == "__main__":
    # Convertir el archivo MP3 a WAV
    convert_mp3_to_wav(mp3_file, wav_file)

    # Transcribir el audio a texto
    segments = transcribe_audio_to_text(wav_file, text_file)

    if segments:
        # Crear archivo ASS a partir de los segmentos transcritos
        create_ass(segments, subtitles_path)

        # Procesar los subtítulos y añadirlos al video
        subs = parse_ass(subtitles_path)
        default_style = styles["Default"]
        video = mp.VideoFileClip(video_path)
        subtitle_clips = [create_text_clip(text, styles.get(style, default_style), time_to_seconds(start), time_to_seconds(end))
                          for (start, end), text, style in subs]
        video_with_subtitles = mp.CompositeVideoClip([video, *subtitle_clips])
        edited_video = video_with_subtitles
        edited_video.write_videofile(final_output_path, codec="libx264", audio_codec="aac")
    else:
        print("No se generaron segmentos para crear el archivo ASS.")
