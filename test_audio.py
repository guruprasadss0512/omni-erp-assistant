import whisper
import time

print("Loading Whisper model (this may take a minute the first time as it downloads)...")
# We use the "base" model for a good balance of speed and accuracy on local machines.
# Options: tiny, base, small, medium, large
model = whisper.load_model("base") 

def transcribe_local_audio(file_path):
    print(f"Transcribing {file_path}...")
    start_time = time.time()
    
    # The transcribe function handles everything
    result = model.transcribe(file_path)
    
    end_time = time.time()
    print(f"\n--- Transcription Complete in {round(end_time - start_time, 2)} seconds ---")
    print(f"TEXT: {result['text']}")

# To run this, you will need a sample audio file in your directory.
if __name__ == "__main__":
    # Replace 'sample.mp3' with whatever audio file you have in the folder
    # Or record a quick 5-second voice note on your phone, email it to yourself, and save it here.
    try:
         transcribe_local_audio("sample.mp3") # or sample.ogg, sample.wav
    except Exception as e:
         print(f"Error: {e}")
         print("Make sure you have an audio file named 'sample.mp3' in this directory!")