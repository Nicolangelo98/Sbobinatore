import os
import time
import whisper
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

        # ⏳ Avvio timer
        start_time = time.time()
        start_hour = time.strftime("%H:%M:%S")  # ⏱️ Salva l'orario di inizio
        print(f"📝 Avvio della trascrizione alle {start_hour}...")
         
        # 🔄 Trascrizione
        result = model.transcribe(wav_path, language="it", temperature=0, beam_size=5, fp16=False)
         
        # ⏱️ Tempo totale impiegato
        elapsed_time = time.time() - start_time
        formatted_time = format_time(int(elapsed_time))
        end_hour = time.strftime("%H:%M:%S")  # ⏱️ Salva l'orario di fine
        print(f"✅ Trascrizione completata alle {end_hour}! Tempo impiegato: {formatted_time}")
 
        # 💾 Salvataggio
        text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"✅ Trascrizione salvata: {text_file_path}")
        
        # 🗑️ Rimuove il file WAV temporaneo
        os.remove(wav_path)
        print(f"🗑️ File temporaneo eliminato: {wav_path}")
         
print("🎉 Operazione completata!")
