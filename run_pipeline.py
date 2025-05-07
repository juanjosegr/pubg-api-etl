import os
import sys

current_dir = os.path.dirname(__file__)    
config_path = os.path.abspath(os.path.join(current_dir,"src"))
sys.path.append(config_path)

from src.load import run_etl, load_postgres

csv_paths = run_etl("KaDiz-", max_matches=10)


load_postgres(csv_paths["player_csv"], table_name="players", )
load_postgres(csv_paths["rooster_csv"], table_name="roosters")
load_postgres(csv_paths["match_csv"], table_name="matches")