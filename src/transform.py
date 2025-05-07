import pandas as pd

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