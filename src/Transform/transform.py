import pandas as pd
import os
import requests
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Extract.extract import find_telemetry, find_seasons, normal_stats, ranked_stats

def match_info(match_data):
    data = match_data['data']['attributes']
    rows = []
    rows.append({
            "gameMode":data['gameMode'],
            "mapName": data["mapName"],
            "createdAt": data['createdAt'],
            "isCustomMatch": data["isCustomMatch"],
            "matchType": data["matchType"],
            "seasonState": data["seasonState"]
    })
        
    return pd.DataFrame(rows)

def rooster_info(match_data):
    rosters = match_data['data']['relationships']['rosters']['data']
    rows = []
    for r in rosters:
        rows.append({
            "id": r['id']
        })
        
    return pd.DataFrame(rows)

def player_match_info(match_data):
    participants = [x for x in match_data['included'] if x['type'] == 'participant']
    rows = []
    for p in participants:
        stats = p['attributes']['stats']
        rows.append({
            "name": stats['name'],
            "playerId": stats["playerId"],
            "winPlace": stats["winPlace"],
            "kills": stats['kills'],
            "headshotKills": stats["headshotKills"],
            "longestKill": stats["longestKill"],
            "killPlace": stats["killPlace"],
            "DBNOs": stats["DBNOs"],
            "assists": stats["assists"],
            "damageDealt": stats['damageDealt'],
            "winPlace": stats['winPlace'],
            "timeSurvived": str(pd.to_timedelta(stats['timeSurvived'], unit='s')).split()[-1],
            "heals": stats["heals"],
            "boosts": stats["boosts"],
            "deathType": stats["deathType"],
            "walkDistance": stats["walkDistance"],
            "rideDistance": stats["rideDistance"],
            "swimDistance": stats["swimDistance"],
            "vehicleDestroys": stats["vehicleDestroys"]
        })
    pd.set_option('display.max_rows', None)
    return pd.DataFrame(rows).sort_values(by=['winPlace', 'kills'], ascending=[True, False]).reset_index(drop=True)

def transform_telemetry(match_id):
    match_data  = find_telemetry(match_id)

    # Obtener asset ID de telemetría
    try:
        asset_id = match_data['data']['relationships']['assets']['data'][0]['id']
    except (KeyError, IndexError):
        print("❌ No se encontró asset_id en los datos.")
        return match_data
    
    # Buscar el asset en el array 'included'
    asset = next(
        (item for item in match_data.get('included',[])
         if item['type'] == 'asset' and item['id'] == asset_id), 
        None)

    if asset is None:
        print("❌ Telemetry asset not found.")
        return match_data

    telemetry_url = asset['attributes'].get('URL')
    if not telemetry_url:
        print("❌ URL Telemetry not found.")
        return match_data
    
    tele_response = requests.get(telemetry_url, headers={"Accept-Encoding": "gzip"})
    tele_response.raise_for_status()

    os.makedirs("data/telemetry", exist_ok=True)
    filepath = f"data/telemetry/{match_id}_telemetry.json"
    with open(filepath, "wb") as f:
        f.write(tele_response.content)

    print(f"✅ Telemetría guardada en {filepath}")
    return filepath

def list_seasons():
    data = find_seasons()
    seasons = []
    for season in data['data']:
        seasons.append({
            "ID:" : season['id'],
            "is_current" : season['attributes']['isCurrentSeason'],
            "is_offseason" : season['attributes']['isOffseason']
        })
    return pd.DataFrame(seasons)

def found_all_season_stats(player_id, delay=6.2):
    df_seasons = list_seasons()

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
