from langchain_core.prompts import PromptTemplate

soap_prompt = PromptTemplate(
    input_variables=["conversation"],
    template="""
You are an expert medical documentation assistant.

Analyze the doctor-patient conversation and generate a SOAP note.

Instructions:
1. Extract patient complaints and symptoms into subjective.
2. Extract vital signs and measurable observations into objective.
3. Extract doctor's diagnosis into assessment.
4. Extract medications, tests, treatments, and follow-up instructions into plan.
5. If information is missing, return an empty list.
6. Return ONLY valid JSON.
7. Do NOT use markdown.
8. Do NOT wrap the response in ```json.
9. Do NOT create nested objects.
10. Do NOT create a SOAP parent key.

Return EXACTLY in this format:

{{
    "subjective": [],
    "objective": [],
    "assessment": [],
    "plan": []
}}

Example:

{{
    "subjective": [
        "Fever for three days",
        "Headache"
    ],
    "objective": [],
    "assessment": [
        "Viral infection"
    ],
    "plan": [
        "Paracetamol",
        "CBC test"
    ]
}}

Conversation:
{conversation}
"""
)