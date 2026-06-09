from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path

app=FastAPI()

upload_dir = Path("data/upload")
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
        
    return{
        "filename": file.filename,
        "saved_to": str(file_path),
        "status": "uploaded successfully"
    }