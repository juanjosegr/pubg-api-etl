from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import quote
import os
from dotenv import load_dotenv
import sys
env_path = sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "credenciales.env")))

load_dotenv(env_path)

def get_engine():
    user = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    password = quote(raw_password)
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    print("Conectando a la base de datos...")
    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            print("✅ Conexión a PostgreSQL exitosa.")
        return engine
    except OperationalError as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)
        return None


