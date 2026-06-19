from app.services.icd_rag import recommend_icd_codes

result = recommend_icd_codes(
    "Patient has fever and headache"
)

print(result)