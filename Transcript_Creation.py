import os
import json
import torchaudio
import torch
from vosk import Model, KaldiRecognizer
import numpy as np

# Load Vosk model
model_path = r"C:\Users\nandh\Downloads\vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Vosk model not found at {model_path}. Please download and extract the model.")
    exit()
model = Model(model_path)

# Load audio file
audio_path = r"D:\navya\mini project\audios\audio2.wav"
if not os.path.exists(audio_path):
    print(f"Audio file not found at {audio_path}.")
    exit()
waveform, sample_rate = torchaudio.load(audio_path)

# Check if the audio file has multiple channels and convert to mono if necessary
if waveform.shape[0] > 1:
    waveform = torch.mean(waveform, dim=0, keepdim=True)

# Convert audio data to a NumPy array and rescale to 16-bit PCM
audio_data = waveform.numpy()
audio_data = (audio_data * 32767).astype(np.int16)

# Initialize the KaldiRecognizer
rec = KaldiRecognizer(model, sample_rate)

# Process the audio file in chunks
transcript = ""
chunk_size = 4000  # Adjust chunk size as needed
for i in range(0, len(audio_data), chunk_size):
    data = audio_data[i:i + chunk_size].tobytes()
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        transcript += result["text"]

# Finalize the transcription
result = json.loads(rec.FinalResult())
transcript += result["text"]

# Save the transcript to a text file
transcript_file_path = r"D:\navya\mini project\transcripts\transcript2.txt"
with open(transcript_file_path, "w") as f:
    f.write(transcript)

print("Transcript saved successfully.")
