import random
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cookpad.com"


def get_recipes(targets):
    """
    This function fetches recipes from the cookpad website.
    It takes a list of targets as input and returns a random sample of 3 recipes.
    """
    # Send a GET request to the cookpad website with the targets as search parameters
    response = requests.get(f"{BASE_URL}/search/{targets}")
    # Parse the response text with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all recipe previews in the parsed HTML
    tags = soup.find_all("li", class_="ranked-list__item")
    recipes = []
    for tag in tags:
        # Append each recipe's name, image, and link to the recipes list
        recipes.append(
            {
                "name": tag.find_all("a")[0].text.strip(),
                "image": tag.find_all("img")[1]["src"],
                "link": f'{BASE_URL}/{tag.find_all("a")[0].get("href")}',
            }
        )
    # Return a random sample of 3 recipes
    return random.sample(recipes, 3)
