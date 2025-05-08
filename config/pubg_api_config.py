import os
from dotenv import load_dotenv

current_dir = os.path.dirname(__file__) 
env_path = os.path.abspath(os.path.join(current_dir, "..", "config", "credenciales.env"))

load_dotenv(env_path)

api_key = os.getenv("PUBG_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json"
}

BASE_URL = "https://api.pubg.com/shards/steam"