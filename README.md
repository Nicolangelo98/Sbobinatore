# Sbobinatore
#pip install openai-whisper ffmpeg-python
funziona 
import os
import whisper


import os
import whisper
import librosa
import soundfile as sf
import noisereduce as nr
from pydub import AudioSegment

# 📂 Percorsi
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"
os.makedirs(output_dir, exist_ok=True)

# 🛠️ Caricamento del modello Whisper migliorato
print("📥 Caricamento del modello Whisper...")
model = whisper.load_model("large")  # Oppure "large"
print("✅ Modello caricato!")

# 🔄 Processa tutti i file audio
for filename in os.listdir(audio_dir):
    if filename.endswith(".m4a"):
        file_path = os.path.join(audio_dir, filename)
        print(f"🎙️ Preprocessing e trascrizione: {filename}")

        # 📌 Conversione in WAV 16kHz mono
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        wav_path = file_path.replace(".m4a", ".wav")
        audio.export(wav_path, format="wav")

        # 🎛 Riduzione del rumore
        y, sr = librosa.load(wav_path, sr=16000)
        y_denoised = nr.reduce_noise(y=y, sr=sr)
        denoised_path = wav_path.replace(".wav", "_denoised.wav")
        sf.write(denoised_path, y_denoised, sr)

        # ⏳ Trascrizione migliorata
        result = model.transcribe(denoised_path, language="it", temperature=0, beam_size=5)

        # 💾 Salvataggio
        text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"✅ Trascrizione salvata: {text_file_path}")

print("🎉 Operazione completata!")

