import chromadb
from sentence_transformers import SentenceTransformer
from fetch_meals import fetch_all_meals

# ✅ Use PersistentClient (VERY IMPORTANT)
client = chromadb.PersistentClient(path="./meal_db")

# Create or get collection
collection = client.get_or_create_collection(name="meals")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def prepare_meal_text(meal):
    ingredients = []

    for i in range(1, 21):
        ing = meal.get(f"strIngredient{i}")
        if ing and ing.strip():
            ingredients.append(ing.strip())

    text = f"""
    Name: {meal.get('strMeal')}
    Category: {meal.get('strCategory')}
    Area: {meal.get('strArea')}
    Ingredients: {', '.join(ingredients)}
    Instructions: {meal.get('strInstructions')}
    """

    return text.strip()


def store_all_meals():
    meals = fetch_all_meals()

    documents = []
    ids = []
    metadatas = []

    for meal in meals:
        documents.append(prepare_meal_text(meal))
        ids.append(meal["idMeal"])
        metadatas.append({
            "category": meal.get("strCategory"),
            "area": meal.get("strArea")
        })

    print("Generating embeddings...")
    embeddings = model.encode(documents).tolist()

    print("Storing in ChromaDB...")
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print("Total stored:", collection.count())
    print("✅ All meals stored successfully!")


if __name__ == "__main__":
    store_all_meals()
