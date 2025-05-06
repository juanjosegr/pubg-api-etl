import os
from dotenv import load_dotenv

load_dotenv("credenciales.env")

api_key = os.getenv("PUBG_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json"
}

BASE_URL = "https://api.pubg.com/shards/steam"
