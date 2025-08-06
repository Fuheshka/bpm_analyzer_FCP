import librosa

# Загружаем аудиофайл
audio_path = 'song.mp3'  # замени на свой файл
y, sr = librosa.load(audio_path)

# Определяем темп и такты
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Переводим кадры в секунды
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Выводим информацию
print(f"Определённый темп: {float(tempo):.2f} BPM")
print("Список времён (в секундах) для маркеров:")
for i, t in enumerate(beat_times, 1):
    print(f"{i}: {float(t):.2f} сек")
