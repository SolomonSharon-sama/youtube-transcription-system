import whisper
import os
from pyannote.audio import Pipeline
from huggingface_hub import login

# Log in to Hugging Face
login("your_huggingface_token")  # Replace with your token

# Folder setup
base_dir = "/Users/mac/Desktop/transcriptions/lenny/strategy"
os.makedirs(base_dir, exist_ok=True)

# List MP3 files
mp3_files = [f for f in os.listdir(base_dir) if f.endswith(".mp3")]

# Load models
whisper_model = whisper.load_model("tiny.en")
diarization = Pipeline.from_pretrained("pyannote/speaker-diarization")

# Track processed files
processed_files = []

for mp3 in mp3_files:
    path = f"{base_dir}/{mp3}"
    output_file = f"{base_dir}/{mp3.replace('.mp3', '_diarized.txt')}"
    
    # Skip if transcript already exists
    if os.path.exists(output_file):
        print(f"Skipped (already transcribed): {output_file}")
        processed_files.append(mp3)
        continue
    
    # Transcribe and diarize
    try:
        result = whisper_model.transcribe(path, word_timestamps=True)
        diarization_result = diarization(path)
        with open(output_file, "w") as f:
            for turn, _, speaker in diarization_result.itertracks(yield_label=True):
                f.write(f"Speaker {speaker}: {result['text'][int(turn.start*16000):int(turn.end*16000)]}\n")
        print(f"Transcribed: {output_file}")
        processed_files.append(mp3)
    except Exception as e:
        print(f"Error transcribing {mp3}: {e}")
        continue

# Print summary
print("\n=== Transcription Summary ===")
print(f"Processed Files ({len(processed_files)}):")
for mp3 in processed_files:
    print(f"  - {mp3}")
print(f"Skipped or Failed Files ({len(mp3_files) - len(processed_files)}):")
for mp3 in mp3_files:
    if mp3 not in processed_files:
        print(f"  - {mp3}")