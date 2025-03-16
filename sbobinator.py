import os
import whisper

# 📂 Definizione dei percorsi per i file audio e le trascrizioni
audio_dir = r"C:\Users\Utente\Desktop\Sbobinetor\audio"
output_dir = r"C:\Users\Utente\Desktop\Sbobinetor\trascrizioni"

# 🛠️ Creazione della cartella output se non esiste
os.makedirs(output_dir, exist_ok=True)

# 🔍 Controlla se la cartella audio esiste, altrimenti esce con un errore
if not os.path.exists(audio_dir):
    print(f"❌ Errore: La cartella audio non esiste -> {audio_dir}")
    exit()

# 🧠 Caricamento del modello Whisper
print("📥 Caricamento del modello Whisper... (potrebbe richiedere alcuni secondi)")
model = whisper.load_model("small")
print("✅ Modello Whisper caricato con successo!")

# 🔄 Processa tutti i file audio nella cartella
for filename in os.listdir(audio_dir):
    if filename.endswith(".m4a"):
        file_path = os.path.join(audio_dir, filename)
        print(f"🎙️ Trascrizione in corso: {filename}")

        # ⏳ Esegui la trascrizione con Whisper
        result = model.transcribe(file_path, language="it")

        # 💾 Salvataggio della trascrizione in un file di testo
        text_file_path = os.path.join(output_dir, filename.replace(".m4a", ".txt"))
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"✅ Trascrizione completata e salvata in: {text_file_path}")

print("🎉 Operazione completata con successo!")
