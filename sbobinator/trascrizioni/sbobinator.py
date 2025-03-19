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
model = whisper.load_model("large")  # Oppure "large"
print("✅ Modello caricato!")

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

        # 📌 Conversione in WAV 16kHz mono
        print("🔄 Conversione in formato WAV 16kHz mono...")
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        wav_path = file_path.replace(".m4a", ".wav")
        audio.export(wav_path, format="wav")
        print(f"✅ Conversione completata: {wav_path}")

        # 🎛 Riduzione del rumore (commentata)
        # print("🎛 Riduzione del rumore in corso...")
        # y, sr = librosa.load(wav_path, sr=16000)
        # y_denoised = nr.reduce_noise(y=y, sr=sr)
        # denoised_path = wav_path.replace(".wav", "_denoised.wav")
        # sf.write(denoised_path, y_denoised, sr)
        # print(f"✅ Riduzione del rumore completata: {denoised_path}")

        # ⏳ Avvio timer
        start_time = time.time()
        print("📝 Avvio della trascrizione...")
        
        # 🔄 Trascrizione
        result = model.transcribe(wav_path, language="it", temperature=0, beam_size=5)
        
        # ⏱️ Tempo totale impiegato
        elapsed_time = time.time() - start_time
        formatted_time = format_time(int(elapsed_time))
        print(f"✅ Trascrizione completata in {formatted_time}!")

        # 💾 Salvataggio
        text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"✅ Trascrizione salvata: {text_file_path}")

print("🎉 Operazione completata!")
