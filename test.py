from app.services.transcription import transcribe_audio

test = transcribe_audio("data/upload/hindi.mp3")

print(test)