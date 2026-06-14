import re

def diarize_transcript(transcript: str):

    pattern = r"(Doctor|Patient)[,:]?\s*(.*?)(?=(Doctor|Patient|$))"

    matches = re.findall(pattern, transcript, re.DOTALL)

    conversation = []

    for match in matches:
        conversation.append({
            "speaker": match[0],
            "text": match[1].strip()
        })

    return conversation