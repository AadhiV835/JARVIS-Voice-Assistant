import voice_auth
print("Recording and checking voice...")
embed = voice_auth.get_embedding(voice_auth.record_voice())
known = voice_auth.load_known_embeddings()
match = voice_auth.identify_speaker(embed, known)
if match:
    print(f"Identified as: {match}")
else:
    print("Could not recognize you.")
