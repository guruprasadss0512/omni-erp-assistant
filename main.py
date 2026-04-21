from fastapi import FastAPI, Request, Query, BackgroundTasks
from fastapi.responses import PlainTextResponse
import os
import requests
import whisper
import tempfile
from dotenv import load_dotenv

# --- IMPORT YOUR AI BRAIN ---
from agent import process_chat

load_dotenv()

app = FastAPI(title="Omni-Channel ERP Assistant")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_super_secret_token_123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

print("Loading Whisper Model into memory...")
whisper_model = whisper.load_model("base")
print("Model loaded successfully!")

def send_whatsapp_message(to_number: str, message_text: str):
    """Sends a text message via WhatsApp API."""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text},
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Message sent to WhatsApp status: {response.status_code}")

def download_whatsapp_media(media_id: str) -> str:
    """Downloads media from Meta and saves it to a temp file."""
    url_req = requests.get(
        f"https://graph.facebook.com/v18.0/{media_id}",
        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    )
    media_url = url_req.json().get("url")

    media_req = requests.get(
        media_url,
        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg")
    temp_file.write(media_req.content)
    temp_file.close()
    return temp_file.name

# --- NEW: THE AI PROCESSING FUNCTION ---
def process_and_reply(sender_phone: str, user_text: str):
    """Passes text to the AI and sends the result back to WhatsApp."""
    print(f"\n🧠 AI is thinking about: '{user_text}'...")
    try:
        # Let LangGraph, Groq, and Zoho do their magic
        ai_response = process_chat(user_text)
        print(f"🗣️ AI Decision: {ai_response}\n")
        
        # Send the AI's response back to the user's phone
        send_whatsapp_message(sender_phone, ai_response)
    except Exception as e:
        print(f"❌ Error in AI processing: {e}")
        send_whatsapp_message(sender_phone, "System Error: Could not connect to the ERP database.")

def process_audio_message(media_id: str, sender_phone: str):
    """Downloads, transcribes, and passes audio text to the AI."""
    try:
        print("Downloading audio from Meta...")
        file_path = download_whatsapp_media(media_id)
        
        print("Transcribing audio...")
        result = whisper_model.transcribe(file_path)
        transcription = result["text"]
        print(f"Transcription complete: {transcription}")
        
        # Send the user a quick note so they know the audio was heard
        send_whatsapp_message(sender_phone, f"*(Transcribed: {transcription})*")
        
        # Pass the transcribed text directly into the AI Brain!
        process_and_reply(sender_phone, transcription)
        
        os.remove(file_path)
    except Exception as e:
        print(f"Error processing audio: {e}")

@app.get("/")
def read_root():
    return {"status": "ERP Assistant Server is running!"}

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    return PlainTextResponse(content="Verification failed", status_code=403)

@app.post("/webhook")
async def receive_message(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    if body.get("object") == "whatsapp_business_account":
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    message = value["messages"][0]
                    sender_phone = message["from"]
                    
                    if message["type"] == "text":
                        incoming_text = message["text"]["body"]
                        print(f"📱 Received text from {sender_phone}: {incoming_text}")
                        # Route to AI in the background
                        background_tasks.add_task(process_and_reply, sender_phone, incoming_text)
                        
                    elif message["type"] == "audio":
                        media_id = message["audio"]["id"]
                        print(f"🎤 Received audio note from {sender_phone}. Processing...")
                        # Route to Audio Processor -> then to AI
                        background_tasks.add_task(process_audio_message, media_id, sender_phone)
                        
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)