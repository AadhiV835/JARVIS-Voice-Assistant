import voice_auth
embed = voice_auth.get_embedding(voice_auth.record_voice())
voice_auth.save_new_user("aadhi", embed)
