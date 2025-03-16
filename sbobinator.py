import os
import whisper
from pydub import AudioSegment
import time  # Per monitorare il tempo di esecuzione

# 📂 Percorsi delle cartelle (modifica se necessario)
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"
os.makedirs(output_dir, exist_ok=True)

# 🛠️ Caricamento del modello Whisper (Medium per maggiore accuratezza)
print("📥 Caricamento del modello Whisper... (potrebbe richiedere alcuni secondi)")
model = whisper.load_model("small")  # Puoi usare "large" per ancora più precisione
print("✅ Modello Whisper caricato con successo!")

# Funzione per dividere l'audio in segmenti di 5 minuti
def split_audio(input_audio_path, segment_duration_ms=3*60*1000):
    audio = AudioSegment.from_file(input_audio_path)
    segments = []
    
    # Calcola il numero di segmenti necessari
    num_segments = len(audio) // segment_duration_ms + (1 if len(audio) % segment_duration_ms != 0 else 0)
    
    for i in range(num_segments):
        start_ms = i * segment_duration_ms
        end_ms = (i + 1) * segment_duration_ms
        segment = audio[start_ms:end_ms]
        segment_path = f"{input_audio_path.replace('.m4a', '')}_part_{i+1}.wav"
        segment.export(segment_path, format="wav")
        segments.append(segment_path)
    
    return segments

# 🔄 Processa tutti i file audio nella cartella
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".m4a")]
print(f"🔍 Trovati {len(audio_files)} file audio da elaborare.")

for filename in audio_files:
    file_path = os.path.join(audio_dir, filename)
    print(f"🎙️ Inizio elaborazione: {filename}")
    
    # 📌 Conversione in formato WAV 16kHz mono (per migliorare la qualità della trascrizione)
    print("🔄 Convertendo l'audio in formato WAV 16kHz mono...")
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    wav_path = file_path.replace(".m4a", ".wav")
    audio.export(wav_path, format="wav")
    print("✅ Conversione completata!")

    # ⏳ Spezzare l'audio in segmenti da 5 minuti
    segments = split_audio(wav_path)
    num_segments = len(segments)
    print(f"📂 {filename} è stato diviso in {num_segments} segmenti.")

    # 📑 Trascrizione dei segmenti e concatenazione in un unico file
    full_transcription = ""
    for i, segment in enumerate(segments):
        print(f"🔄 Inizio trascrizione del segmento {i+1} su {num_segments}...")
        start_time = time.time()  # Monitoriamo quanto tempo impiega ogni segmento
        result = model.transcribe(segment, language="it", temperature=0, beam_size=5)
        elapsed_time = time.time() - start_time
        print(f"✅ Trascrizione completata per il segmento {i+1} in {elapsed_time:.2f} secondi!")

        # Concatenazione della trascrizione nel file unico
        full_transcription += result["text"] + "\n"  # Aggiungi una nuova riga tra i segmenti

    # 💾 Salvataggio della trascrizione completa in un unico file di testo
    text_file_path = os.path.join(output_dir, f"{filename.replace('.m4a', '')}_complete_transcription.txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(full_transcription)
    print(f"📄 Trascrizione completa salvata in: {text_file_path}")

    print(f"🎉 Elaborazione di {filename} completata!")

print("🎉 Tutti i file sono stati elaborati con successo!")
