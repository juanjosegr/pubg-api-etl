from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import quote
import os
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv("credenciales.env")

def get_engine():
    # Lee las variables de entorno
    user = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    # Codificar la contraseña para evitar problemas con caracteres especiales
    password = quote(raw_password)

    # Construye la cadena de conexión
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    print("Conectando a la base de datos...")

    try:
        engine = create_engine(connection_string)
        # Intenta abrir una conexión para probar
        with engine.connect() as conn:
            print("✅ Conexión a PostgreSQL exitosa.")
        return engine
    except OperationalError as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)
        return None
