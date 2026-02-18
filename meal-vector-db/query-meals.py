import chromadb
from sentence_transformers import SentenceTransformer

# ✅ Same persistent path
client = chromadb.PersistentClient(path="./meal_db")

collection = client.get_collection(name="meals")

model = SentenceTransformer("all-MiniLM-L6-v2")


def query_meals(user_query):
    query_embedding = model.encode([user_query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return results["documents"]


if __name__ == "__main__":
    query = input("Enter your meal search: ")
    results = query_meals(query)

    print("\nTop Matching Meals:\n")
    for r in results[0]:
        print(r)
        print("=" * 60)
