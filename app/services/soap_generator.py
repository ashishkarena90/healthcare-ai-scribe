from langchain_groq import ChatGroq
from app.prompts.soap_prompt import soap_prompt
from app.scheme.soap_schema import SOAPNote
from dotenv import load_dotenv
import os
import json
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_soap(conversation: str):
    
    final_prompt = soap_prompt.format(
        conversation = conversation
    )
    
    response = llm.invoke(final_prompt)
    
    soap_dict = json.loads(response.content)
    
    
    validation_soap = SOAPNote(**soap_dict)
    
    
    
    return validation_soap.model_dump()