import csv
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="icd10_codes"
)

with open("app/data/icd10.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        collection.add(
            ids=[row["code"]],
            documents=[row["description"]],
            metadatas=[
                {
                    "code": row["code"]
                }
            ]
        )

print("ICD-10 data stored successfully!")