import os
import whisper
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 🔐 Carica variabili da .env
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

audio_dir = os.getenv("AUDIO_DIR")
output_dir = os.getenv("OUTPUT_DIR")


# 📁 Crea cartella output se non esiste
os.makedirs(output_dir, exist_ok=True)

# 🎙 Carica modello Whisper
model = whisper.load_model("large")

# 🎧 Trova tutti i file .m4a nella cartella
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".m4a")]

# 📬 Funzione invio email con allegato
def invia_email_con_allegato(file_path):
    msg = EmailMessage()
    msg["Subject"] = "Pokkia, Sbobinassione Completata!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("POKKIA OKKIA OKKIA")

    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email inviata con successo a {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"❌ Errore nell'invio dell'email: {e}")

# 🔁 Loop di trascrizione e invio
for file in audio_files:
    file_path = os.path.join(audio_dir, file)
    output_file = os.path.join(output_dir, file.replace(".m4a", ".txt"))
    
    start_time = time.time()
    start_timestamp = time.strftime("%H:%M:%S", time.localtime(start_time))
    print(f"[{start_timestamp}] Inizio trascrizione: {file}")
    
    result = model.transcribe(file_path, language="it",fp16=False)
                                #temperature=0, beam_size=5  -> temperatura per non dare creatività, beam_size fa 5 prove
    
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

    # 📧 Invia email con allegato
    invia_email_con_allegato(output_file)
