from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from app.services.transcription import transcribe_audio
from app.services.diarization import diarize_transcript

app=FastAPI()

upload_dir = Path("app/data/upload")
upload_dir.mkdir(parents=True, exist_ok=True)

@app.get("/")
def root():
    return{
        "message" : "Healthcare AI Scribe API Running"
    }
    
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    file_path = upload_dir / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    print(f"File saved at: {file_path}")
        
    transcript = transcribe_audio(str(file_path))
    
    transcription_result = transcribe_audio(str(file_path))
    conversation = diarize_transcript(transcription_result["transcript"])
    
    print("Transcript Result:", transcript)
        
    return{
        "filename": file.filename,
        "saved_to": str(file_path),
        "transcript": transcription_result["transcript"],
        "language": transcription_result["language"],
        "conversation": conversation,
        "status": "uploaded successfully"
    }