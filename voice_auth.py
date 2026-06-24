from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
import os
import soundfile as sf
import speech_module as sm
import sounddevice as sd

encoder = VoiceEncoder()

def record_voice(duration=4, filename="temp.wav"):
    sm.SpeakText("Please speak now.")
    print("Recording voice...")
    
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
    sd.wait()
    sf.write(filename, audio, 16000)
    return filename

def get_embedding(wav_path):
    wav = preprocess_wav(wav_path)
    return encoder.embed_utterance(wav)

def load_known_embeddings(folder="known_voices"):
    embeddings = {}
    for file in os.listdir(folder):
        if file.endswith(".npy"):
            name = file[:-4]
            embeddings[name] = np.load(os.path.join(folder, file))
    return embeddings

def identify_speaker(voice_embed, known_embeds, threshold=0.65):
    from numpy.linalg import norm
    for name, emb in known_embeds.items():
        similarity = np.dot(voice_embed, emb) / (norm(voice_embed) * norm(emb))
        if similarity > threshold:
            return name
    return None

def save_new_user(name, embedding, folder="known_voices"):
    if not os.path.exists(folder):
        os.mkdir(folder)
    np.save(os.path.join(folder, f"{name.lower()}.npy"), embedding)
