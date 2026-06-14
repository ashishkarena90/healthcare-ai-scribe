from pydantic import BaseModel
from typing import List

class SOAPNote(BaseModel):
    subjective: List[str]
    objective: List[str]
    assessment: List[str]
    plan: List[str]
    
    