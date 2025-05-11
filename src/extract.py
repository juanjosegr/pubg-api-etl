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
    url = f"{BASE_URL}/players/{player_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  
    return response.json()["data"]["relationships"]["matches"]["data"]

def extract_match_details(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def find_telemetry(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def find_seasons():
    url = f"{BASE_URL}/seasons"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

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

def stats_lifetime(player_id):
    url = f"{BASE_URL}/players/{player_id}/seasons/lifetime"
    response = requests.get(url, headers = HEADERS)
    response.raise_for_status()
    return response.json()

def weapon_mastery(player_id):
    url = f"{BASE_URL}/players/{player_id}/weapon_mastery"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def survival_mastery(player_id):
    url = f"{BASE_URL}/players/{player_id}/survival_mastery"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def find_clan(clan_id):
    url = f"{BASE_URL}/clans/{clan_id}"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def obtain_leaderboards(platform_region, seasonId, gameMode):
    url = f"https://api.pubg.com/shards/{platform_region}/leaderboards/{seasonId}/{gameMode}"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def obtain_samples():
    url = f"{BASE_URL}/samples"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def obtain_status():
    url = "https://api.pubg.com/status"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def obtain_tournament_stats():
    url = "https://api.pubg.com/tournaments"
    response = requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()
