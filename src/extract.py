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


import pandas as pd
import time

def find_seasons():
    url = f"{BASE_URL}/seasons"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def listar_temporadas():
    data = find_seasons()
    seasons = []
    for season in data['data']:
        seasons.append({
            "ID:" : season['id'],
            "is_current" : season['attributes']['isCurrentSeason'],
            "is_offseason" : season['attributes']['isOffseason']
        })
    return pd.DataFrame(seasons)

def ranked_stats(player_id,seasonID):
    url = f"{BASE_URL}/players/{player_id}/seasons/{seasonID}/ranked"
    response = requests.get(url, headers = HEADERS)
    response.raise_for_status()
    return response.json()

def normal_stats(player_id,seasonID):
    url = f"{BASE_URL}/players/{player_id}/seasons/{seasonID}"
    response = requests.get(url, headers = HEADERS)
    response.raise_for_status()
    return response.json()

import time

def comprobar_stats_en_todas_las_seasons(player_id, delay=6.2):
    df_seasons = listar_temporadas()

    for index, row in df_seasons.iterrows():
        season_id = row["ID:"]
        
        # Filtrar temporadas de consola
        if any(x in season_id.lower() for x in ["console", "psn", "xbox"]):
            print(f"⏩ Saltando temporada de consola: {season_id}")
            continue

        print(f"\n🔎 Comprobando season: {season_id}")

        # Comprobar stats normales
        try:
            normal_data = normal_stats(player_id, season_id)
            normal_stats_data = normal_data.get("data", {}).get("attributes", {}).get("gameModeStats", {})

            if normal_stats_data:
                print("✅ Normales: Stats encontradas.")
            else:
                print("⚠️ Normales: Sin stats.")
        except requests.exceptions.HTTPError as e:
            print(f"❌ Normales: Error HTTP - {e}")
        
        time.sleep(delay)  # Espera entre peticiones

        # Comprobar stats ranked
        try:
            ranked_data = ranked_stats(player_id, season_id)
            ranked_stats_data = ranked_data.get("data", {}).get("attributes", {}).get("rankedGameModeStats", {})

            if ranked_stats_data:
                print("✅ Ranked: Stats encontradas.")
            else:
                print("⚠️ Ranked: Sin stats.")
        except requests.exceptions.HTTPError as e:
            print(f"❌ Ranked: Error HTTP - {e}")
        
        time.sleep(delay)  # Espera entre peticiones

player_id = "account.4f2c09f2b4d447379dbace96bc582a96"
comprobar_stats_en_todas_las_seasons(player_id)
