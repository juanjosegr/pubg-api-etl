import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.pubg_api_config import BASE_URL, HEADERS, get_api_response

def searchPlayer (player_name):
    return get_api_response(f"players?filter[playerNames]={player_name}")["data"][0]["id"]

def find_match_players(player_id):
    return get_api_response(f"players/{player_id}")["data"]["relationships"]["matches"]["data"]

def extract_match_details(match_id):
    return get_api_response(f"matches/{match_id}")

def find_telemetry(match_id):
    return get_api_response(f"matches/{match_id}")

def find_seasons():
    return get_api_response("seasons")

def ranked_stats(player_id,seasonID):
    return get_api_response(f"players/{player_id}/seasons/{seasonID}/ranked")

def normal_stats(player_id,seasonID):
    return get_api_response(f"players/{player_id}/seasons/{seasonID}")

def stats_lifetime(player_id):
    return get_api_response(f"players/{player_id}/seasons/lifetime")

def weapon_mastery(player_id):
    return get_api_response(f"players/{player_id}/weapon_mastery")

def survival_mastery(player_id):
    return get_api_response(f"players/{player_id}/survival_mastery")

def find_clan(clan_id):
   return get_api_response(f"clans/{clan_id}")

def obtain_samples():
    return get_api_response("samples")

def obtain_leaderboards(platform_region, seasonId, gameMode):
    url = f"https://api.pubg.com/shards/{platform_region}/leaderboards/{seasonId}/{gameMode}"
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
