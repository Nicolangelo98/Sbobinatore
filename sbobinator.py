import os
import whisper

def trascrivi_audio(cartella):
    """
    Cerca file audio nella cartella e li trascrive in un file di testo.
    """
    model = whisper.load_model("base")
    print("Modello Whisper caricato.")

    # Trova tutti i file audio nella cartella
    audio_files = [f for f in os.listdir(cartella) if f.endswith((".mp3", ".m4a", ".wav"))]

    if not audio_files:
        print("❌ Nessun file audio trovato.")
        return

    with open("trascrizione.txt", "w", encoding="utf-8") as f:
        for audio in audio_files:
            audio_path = os.path.join(cartella, audio)
            print(f"🎙️ Trascrizione di {audio} in corso...")

            result = model.transcribe(audio_path, fp16=False)
            transcript = result.get("text", "").strip()

            if transcript:
                f.write(f"--- Trascrizione di {audio} ---\n{transcript}\n\n")
                print(f"✅ Trascritto: {audio}")
            else:
                print(f"⚠️ Nessuna trascrizione per {audio}")

    print("📄 Trascrizione completata! Controlla 'trascrizione.txt'.")

if __name__ == "__main__":
    cartella_audio = "./audio"  # Modifica con il percorso della cartella
    trascrivi_audio(cartella_audio)
