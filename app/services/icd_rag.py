import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("icd10_codes")


def recommend_icd_codes(assessment: str, n_results: int = 3):

    results = collection.query(
        query_texts=[assessment],
        n_results=n_results
    )

    recommendations = []

    for i in range(len(results["ids"][0])):
        recommendations.append({
            "code": results["metadatas"][0][i]["code"],
            "description": results["documents"][0][i]
        })

    return recommendations