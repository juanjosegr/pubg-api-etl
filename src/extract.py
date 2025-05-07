import sys
import os
import requests

current_dir = os.path.dirname(__file__)                      
config_path = os.path.abspath(os.path.join(current_dir, "..", "config"))
sys.path.append(config_path)

from pubg_api_config import BASE_URL, HEADERS



def searchPlayer (player_name):
    # Endpoint to find player for name
    url = f"{BASE_URL}/players?filter[playerNames]={player_name}"
    
    # Send the GET request to the API with authorization headers
    response = requests.get(url, headers=HEADERS)

    # Raise an exception if the request failed (e.g., 404 or 500)
    response.raise_for_status()    

    #Save the information and transform with Json library and return the player id
    data = response.json()
    return data["data"][0]["id"]

searchPlayer('KaDiz-')

def find_match_players(player_id):
    # Endpoint to obtain data of the player from id
    url = f"{BASE_URL}/players/{player_id}"

    # Send the GET request to the API with authorization headers
    response = requests.get(url, headers=HEADERS)
    
    # Raise an exception if the request failed (e.g., 404 or 500)
    response.raise_for_status()  

    # Returns all of matches from the player
    return response.json()["data"]["relationships"]["matches"]["data"]


def extract_match_details(match_id):
    # Construct the API endpoint URL using the match ID
    url = f"{BASE_URL}/matches/{match_id}"
    
    # Send the GET request to the API with authorization headers
    response = requests.get(url, headers=HEADERS)
    
    # Raise an exception if the request failed (e.g., 404 or 500)
    response.raise_for_status()
    
    # Return the JSON response containing match details
    return response.json()

def download_telemetry(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    match_data = response.json()

    # Obtener asset ID de telemetría
    asset_id = match_data['data']['relationships']['assets']['data'][0]['id']

    # Buscar el asset en el array 'included'
    asset = next((item for item in match_data['included'] if item['type'] == 'asset' and item['id'] == asset_id), None)
    if asset is None:
        print("❌ Telemetry asset not found.")
        return match_data

    telemetry_url = asset['attributes']['URL']
    
    tele_response = requests.get(telemetry_url, headers={"Accept-Encoding": "gzip"})
    tele_response.raise_for_status()

    os.makedirs("telemetry", exist_ok=True)
    filepath = f"telemetry/{match_id}_telemetry.json"
    with open(filepath, "wb") as f:
        f.write(tele_response.content)

    print(f"✅ Telemetría guardada en {filepath}")
