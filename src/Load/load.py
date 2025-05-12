import os
from datetime import datetime
from time import sleep
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Extract.extract import searchPlayer, find_match_players, extract_match_details
from Transform.transform import rooster_info, match_info, player_match_info
from config.db_config import get_engine

def save_to_csv(df, filename="data/match_data.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)

def run_etl(player_name, max_matches=3):
    print(f"Obteniendo ID para jugador: {player_name}")
    player_id = searchPlayer(player_name)
    
    print("Obteniendo lista de partidas...")
    matches = find_match_players(player_id)[:max_matches]
    sleep(1)

    # Inicializamos los tres dataframes
    all_data_match = pd.DataFrame()
    all_data_rooster = pd.DataFrame()
    all_data_player = pd.DataFrame()
    
    for match in matches:
        match_id = match['id']
        print(f"Procesando partida: {match_id}")
        match_data = extract_match_details(match_id)
        sleep(1)

        # Match info
        df_match = match_info(match_data)
        df_match['match_id'] = match_id
        all_data_match = pd.concat([all_data_match, df_match], ignore_index=True)
        sleep(1)
        
        # Rooster info
        df_rooster = rooster_info(match_data)
        df_rooster['match_id'] = match_id
        all_data_rooster = pd.concat([all_data_rooster, df_rooster], ignore_index=True)
        sleep(1)
        
        # Player info
        df_player = player_match_info(match_data)
        df_player['match_id'] = match_id
        all_data_player = pd.concat([all_data_player, df_player], ignore_index=True)

        sleep(1)

    # Timestamp y nombres de archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = "data"

    player_file = f"{base_path}/{player_name}_players_{timestamp}.csv"
    rooster_file = f"{base_path}/{player_name}_roosters_{timestamp}.csv"
    match_file = f"{base_path}/{player_name}_matches_{timestamp}.csv"

    print("Guardando archivos CSV...")
    save_to_csv(all_data_player, filename=player_file)
    save_to_csv(all_data_rooster, filename=rooster_file)
    save_to_csv(all_data_match, filename=match_file)

    print("✅ ETL completado. Archivos generados:")
    print(f" - {player_file}")
    print(f" - {rooster_file}")
    print(f" - {match_file}")

    return {
        "player_csv": player_file,
        "rooster_csv": rooster_file,
        "match_csv": match_file
    }

def load_postgres(csv_file_path, table_name):
    print(f"archivo: '{csv_file_path}'")
    print(f"tabla: '{table_name}'")
    
    upload_csv_to_postgres(csv_file_path, table_name, key_column="match_id")
    print("✅ Upload completo.")   

def upload_csv_to_postgres(csv_file_path, table_name, key_column="match_id"):
    engine_start = get_engine()
    try:
        # Leer el archivo CSV
        df = pd.read_csv(csv_file_path)

        # Obtener los match_id ya existentes en la tabla
        existing_ids_query = f"""
            SELECT {key_column} FROM pubg_games.{table_name}
        """
        existing_ids = pd.read_sql(existing_ids_query, engine_start)
        existing_ids_set = set(existing_ids[key_column].astype(str))

        # Convertimos el match_id a string (por seguridad) y filtramos duplicados
        df[key_column] = df[key_column].astype(str)
        df_filtered = df[~df[key_column].isin(existing_ids_set)]

        if df_filtered.empty:
            print(f"⚠️ Todos los registros del archivo ya existen en la tabla '{table_name}'. No se insertó nada.")
        else:
            df_filtered.to_sql(table_name, engine_start, if_exists="append", index=False, schema="pubg_games")
            print(f"✅ Insertados {len(df_filtered)} registros nuevos en '{table_name}'.")

    except Exception as e:
        print(f"❌ Error al subir a PostgreSQL: {e}")

