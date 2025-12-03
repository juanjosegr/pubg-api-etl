import os
from dotenv import load_dotenv
import requests
current_dir = os.path.dirname(__file__) 
env_path = os.path.abspath(os.path.join(current_dir, "..", "config", ".env"))

load_dotenv(env_path)

api_key = os.getenv("PUBG_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json"
}

BASE_URL = "https://api.pubg.com/shards/steam"

def get_api_response(endPoint: str) -> dict:
    """
    Sends a GET request to the PUBG API and returns the JSON response.

    Args:
        endPoint (str): The API endpoint to query (appended to BASE_URL).

    Returns:
        dict: The parsed JSON response from the API.

    Raises:
        HTTPError: If the API response contains an HTTP error status.
    """

    # Build the full URL with the given endpoint
    url = f"{BASE_URL}/{endPoint}"
    # Send a GET request with authorization headers
    response = requests.get(url, headers=HEADERS)
    # Raise an exception if the request fails (e.g., 404 or 500)
    response.raise_for_status()
    # Return the response parsed as JSON
    return response.json()