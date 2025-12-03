# 🎮 PUBG API ETL - Versión Inicial

Este proyecto forma parte de mi proceso continuo de mejora como **Data Engineer Junior**, con el objetivo de reforzar habilidades clave como el consumo de APIs, estructuración de pipelines ETL y manejo de datos reales.

Proyecto personal para practicar y mostrar habilidades de **Data Engineering** usando datos reales de la API oficial de PUBG.

Incluye:
- Consumo de API REST
- Pipeline ETL en Python
- Almacenamiento en PostgreSQL
- Análisis exploratorio en notebooks
---

### 🛠️ Tecnologías usadas

- Python 3.x
- Requests
- Pandas
- SQLAlchemy
- psycopg2-binary
- python-dotenv
- PostgreSQL
- Jupyter Notebook
- VS Code

---

### ⚙️ ¿Qué hace este proyecto?

- Se conecta con la API oficial de PUBG
- Extrae datos de partidas y telemetría de un jugador
- Procesa la información en scripts modulares (ETL)
- Guarda los resultados en archivos `.csv` y en una base de datos relacional

---

### 🧱 Estructura actual del proyecto

```bash
pubg-api-etl/
├── .venv/                  # Entorno virtual (no se versiona)
├── data/                   # Datos descargados (.csv, .json)
│   └── telemetry/
├── notebooks/              # Notebooks de análisis/EDA
│   └── pubg_api_analysis.ipynb
├── src/
│   ├── Extract/
│   │   └── extract.py      # Lógica de extracción desde la API
│   ├── Transform/
│   │   └── transform.py    # Limpieza y transformación de datos
│   ├── Load/
│   │   └── load.py         # Carga a CSV / PostgreSQL
│   └── config/
│       ├── .env.example    # Ejemplo de variables de entorno
│       ├── db_config.py    # Configuración de conexión a Postgres
│       └── pubg_api_config.py  # Configuración de la API de PUBG
├── run_pipeline.py         # Script principal del pipeline ETL
├── requirements.txt        # Dependencias del proyecto
└── README.md
---

### 🚀 Puesta en marcha

1. Clonar el repositorio
git clone https://github.com/juanjosegr/pubg-api-etl.git
cd pubg-api-etl

2. Crear y activar entorno virtual
python -m venv .venv
# PowerShell
.\.venv\Scripts\Activate.ps1
# CMD
.\.venv\Scripts\activate.bat

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar variables de entorno

Copiar el archivo de ejemplo y rellenar con tus credenciales:

cp src/config/.env.example src/config/.env

Editar src/config/.env:

DB_USER=postgres
DB_PASS=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pubg_db

PUBG_API_KEY=tu_api_key_real

5. Crear base de datos en PostgreSQL
CREATE DATABASE pubg_db;

6. Ejecutar el pipeline
python run_pipeline.py


Los datos se guardarán en:

Archivos CSV dentro de data/

Tablas de PostgreSQL en la base de datos pubg_db

### 🚀 Próximos pasos

Este repositorio irá evolucionando. Próximas tareas que ya estoy trabajando:
- Mejorar modularización del código ETL
- Añadir creación automática de tablas en PostgreSQL
- Incorporar validación de calidad de datos
- Orquestar el pipeline con Airflow o Prefect
- Dockerizar el entorno (app + Postgres)
- Añadir tests unitarios (pytest)
- Crear dashboard (Streamlit / Power BI) con estadísticas del jugador

---

### 📚 Objetivo del proyecto

Este no es un proyecto de iniciación, sino una forma de **practicar, consolidar y mostrar habilidades reales** de ingeniería de datos trabajando con una fuente de datos externa real, compleja y dinámica.

Busco seguir ampliando mi experiencia profesional y, al mismo tiempo, tener un espacio donde experimentar ideas, probar tecnologías y demostrar cómo pienso y estructuro mis soluciones.

Mi meta es convertir este repositorio en un proyecto demostrativo robusto y escalable, útil como portfolio y también como base para otros proyectos ETL con APIs públicas.

---

### 📬 Feedback bienvenido

Todo comentario, consejo o sugerencia técnica es más que bienvenido. ¡Gracias por pasar!

---