import requests

def fetch_all_meals():
    all_meals = []

    for letter in "abcdefghijklmnopqrstuvwxyz":
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
        response = requests.get(url)
        data = response.json()

        if data.get("meals"):
            all_meals.extend(data["meals"])

    return all_meals
