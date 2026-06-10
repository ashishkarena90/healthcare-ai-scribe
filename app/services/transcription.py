import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path : str) -> str:
    """
    Transcribe audio file using Whisper
    """
    
    result = model.transcribe(audio_path, task="translate")
    
    print(result["text"])
    print(result["language"])