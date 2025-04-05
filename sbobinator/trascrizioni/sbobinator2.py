import os
import whisper
import time

# Percorsi cartelle
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"


# Crea la cartella di output se non esiste
os.makedirs(output_dir, exist_ok=True)

# Carica il modello di Whisper (usa "base" o "small" per più velocità, "large" per più precisione)
model = whisper.load_model("large")

# Trova tutti i file .m4a nella cartella sorgente
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".m4a")]

for file in audio_files:
    file_path = os.path.join(audio_dir, file)
    output_file = os.path.join(output_dir, file.replace(".m4a", ".txt"))
    
    start_time = time.time()
    start_timestamp = time.strftime("%H:%M:%S", time.localtime(start_time))
    print(f"[{start_timestamp}] Inizio trascrizione: {file}")
    
    result = model.transcribe(file_path, language="it")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    end_time = time.time()
    end_timestamp = time.strftime("%H:%M:%S", time.localtime(end_time))
    elapsed_time = end_time - start_time
    elapsed_h = int(elapsed_time // 3600)
    elapsed_m = int((elapsed_time % 3600) // 60)
    elapsed_s = int(elapsed_time % 60)
    
    print(f"[{end_timestamp}] Fine trascrizione: {file}")
    print(f"Tempo impiegato: {elapsed_h} ore, {elapsed_m} minuti, {elapsed_s} secondi")
    print(f"Trascrizione salvata in: {output_file}")
    