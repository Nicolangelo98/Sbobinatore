import os
import time
import whisper
from pydub import AudioSegment

# 📂 Percorsi
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"
os.makedirs(output_dir, exist_ok=True)

# 🛠️ Caricamento del modello Whisper migliorato
model = whisper.load_model("large")  # Oppure "large"

# 📕 Otteniamo tutti i file audio
files = [f for f in os.listdir(audio_dir) if f.endswith(".m4a")]

# 🔄 Processa tutti i file audio
for filename in files:
    file_path = os.path.join(audio_dir, filename)
    text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
    
    print(f"⏳ Inizio elaborazione: {filename}")
    
    try:
        # 📌 Conversione in WAV 16kHz mono
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        wav_path = file_path.replace(".m4a", ".wav")
        audio.export(wav_path, format="wav")
        print(f"🔄 Conversione completata: {filename}")
    except Exception as e:
        continue

    # ⏳ Avvio timer
    start_time = time.time()
    start_hour = time.strftime("%H:%M:%S")
    print(f"📝 Trascrizione iniziata: {filename} alle {start_hour}")

    try:
        # 🔄 Trascrizione con salvataggio in tempo reale
        with open(text_file_path, "a", encoding="utf-8") as f:
            for segment in model.transcribe(wav_path, language="it", temperature=0, beam_size=5, word_timestamps=True, fp16=False)["segments"]:
                f.write(f"{segment['text']}\n")
    except Exception as e:
        continue
    
    elapsed_time = time.time() - start_time
    hours, rem = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(rem, 60)
    end_hour = time.strftime("%H:%M:%S")
    print(f"✅ Trascrizione completata: {filename} alle {end_hour} (Tempo impiegato: {hours}h {minutes}min {seconds}sec)")
    
    # 🗑️ Rimuove il file WAV temporaneo
    os.remove(wav_path)

print("🎉 Operazione completata!")