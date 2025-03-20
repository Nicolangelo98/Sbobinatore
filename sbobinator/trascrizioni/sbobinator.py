import os
import time
import whisper
import librosa
import soundfile as sf
from pydub import AudioSegment

# 📂 Percorsi
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"
os.makedirs(output_dir, exist_ok=True)

# 🛠️ Caricamento del modello Whisper migliorato
print("\U0001f4e5 Caricamento del modello Whisper...")
try:
    model = whisper.load_model("large")  # Oppure "large"
    print("✅ Modello caricato!")
except Exception as e:
    print(f"❌ Errore durante il caricamento del modello: {e}")
    exit(1)

# ⏺ Funzione per formattare il tempo in modo leggibile
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_str = ""
    if hours > 0:
        time_str += f"{hours} h "
    if minutes > 0:
        time_str += f"{minutes} minuti "
    if seconds > 0 or time_str == "":
        time_str += f"{seconds} secondi"
    return time_str.strip()

# 🔄 Processa tutti i file audio
for filename in os.listdir(audio_dir):
    if filename.endswith(".m4a"):
        file_path = os.path.join(audio_dir, filename)
        print(f"\U0001f3a7 Preprocessing e trascrizione: {filename}")

        try:
            # 📌 Conversione in WAV 16kHz mono
            print("🔄 Conversione in formato WAV 16kHz mono...")
            audio = AudioSegment.from_file(file_path)
            audio = audio.set_channels(1).set_frame_rate(16000)
            wav_path = file_path.replace(".m4a", ".wav")
            audio.export(wav_path, format="wav")
            print(f"✅ Conversione completata: {wav_path}")
        except Exception as e:
            print(f"❌ Errore durante la conversione di {filename}: {e}")
            continue

        # ⏳ Avvio timer
        start_time = time.time()
        start_timestamp = time.strftime("%H:%M:%S", time.localtime(start_time))
        print(f"📝 Trascrizione iniziata alle ore: {start_timestamp}")

        try:
            # 🔄 Trascrizione con rilevamento parti silenziate
            result = model.transcribe(wav_path, language="it", temperature=0, beam_size=5, word_timestamps=True,fp16=False)
        except Exception as e:
            print(f"❌ Errore durante la trascrizione di {filename}: {e}")
            continue
        
        # ⏱️ Tempo totale impiegato
        end_time = time.time()
        end_timestamp = time.strftime("%H:%M:%S", time.localtime(end_time))
        elapsed_time = format_time(int(end_time - start_time))
        print(f"✅ Trascrizione completata in {elapsed_time}!")
        print(f"📝 Trascrizione terminata alle ore: {end_timestamp}")

        try:
            # 💾 Salvataggio
            text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
            with open(text_file_path, "w", encoding="utf-8") as f:
                for segment in result["segments"]:
                    start = format_time(int(segment["start"]))
                    end = format_time(int(segment["end"]))
                    text = segment["text"]
                    f.write(f"[{start} - {end}] {text}\n")
            print(f"✅ Trascrizione salvata con intervalli di silenzio: {text_file_path}")
        except Exception as e:
            print(f"❌ Errore durante il salvataggio della trascrizione di {filename}: {e}")

print("🎉 Operazione completata!")
