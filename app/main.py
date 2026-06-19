from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from app.services.transcription import transcribe_audio
from app.services.diarization import diarize_transcript
from app.services.soap_generator import generate_soap
from app.services.icd_rag import recommend_icd_codes

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
        
    
    transcription_result = transcribe_audio(str(file_path))
    
    conversation = diarize_transcript(transcription_result["transcript"])
    
    conversation_text = ""
    
    for item in conversation:
        conversation_text += (
            f"{item['speaker']}: {item['text']}\n"
        )
        
    soap_note = generate_soap(conversation_text)
    assessment = soap_note['assessment']
    if isinstance(assessment, list):
      assessment = " ".join(assessment)
      
      
    icd_codes = recommend_icd_codes(
        assessment
    )
    
    print("Transcript Result:", transcription_result)
        
    return{
        "filename": file.filename,
        "saved_to": str(file_path),
        "transcript": transcription_result["transcript"],
        "language": transcription_result["language"],
        "conversation": conversation,
        "soap_note": soap_note,
        "icd_codes": icd_codes,
        "status": "uploaded successfully"
    }