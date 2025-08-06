import xml.etree.ElementTree as ET
import librosa
import os


# Загрузка аудио и анализ ударов
audio_path = "song.mp3"
y, sr = librosa.load(audio_path)
_, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Настройки
audio_name = "MySong"
fcpxml_path = "output.fcpxml"

# Создание XML-структуры
fcpxml = ET.Element("fcpxml", version="1.10")
resources = ET.SubElement(fcpxml, "resources")

# Формат ресурса
format_id = "r1"
ET.SubElement(resources, "format", id=format_id, frameDuration="1/25s", width="1920", height="1080", colorSpace="1-1-1 (Rec. 709)")

# Аудио как ресурс
audio_id = "r2"
asset = ET.SubElement(resources, "asset", id=audio_id, name=audio_name, start="0s", duration="600s", hasAudio="1", hasVideo="0")

# Вложенный media-rep с путём к файлу
ET.SubElement(asset, "media-rep", kind="original-media", src=f"file://{os.path.abspath(audio_path)}")

# Проект
library = ET.SubElement(fcpxml, "library")
event = ET.SubElement(library, "event", name="BeatMarkers")
project = ET.SubElement(event, "project", name="Beat Markers Project")

sequence = ET.SubElement(project, "sequence", duration="600s", format=format_id, tcStart="0s", tcFormat="NDF")
spine = ET.SubElement(sequence, "spine")

# Аудиоклип с маркерами
clip = ET.SubElement(spine, "asset-clip", name=audio_name, ref=audio_id, start="0s", duration="600s", offset="0s")

# Добавление маркеров
for i, t in enumerate(beat_times, 1):
    ET.SubElement(clip, "marker", start=f"{t:.2f}s", duration="1/100s", value=f"Beat {i}")

# Сохранение в файл
tree = ET.ElementTree(fcpxml)
tree.write(fcpxml_path, encoding="utf-8", xml_declaration=True)

print(f"✅ FCPXML успешно создан: {fcpxml_path}")
