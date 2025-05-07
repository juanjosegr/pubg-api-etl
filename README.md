# 🎮 PUBG API ETL - Versión Inicial

Este proyecto forma parte de mi proceso continuo de mejora como **Data Engineer Junior**, con el objetivo de reforzar habilidades clave como el consumo de APIs, estructuración de pipelines ETL y manejo de datos reales.

---

### 🛠️ Tecnologías usadas

- Python
- Jupyter Notebook (exploración)
- VS Code (desarrollo modular)
- API REST (PUBG)
- Requests
- Pandas
- SQLAlchemy
- PostgreSQL
- dotenv

---

### ⚙️ ¿Qué hace este proyecto?

- Se conecta con la API oficial de PUBG
- Extrae datos de partidas y telemetría de un jugador
- Procesa la información en scripts modulares (ETL)
- Guarda los resultados en archivos `.csv` y en una base de datos relacional

---

### 🧱 Estructura actual del proyecto

pubg_pipeline/

├── data/ # Archivos descargados (.csv, .json)

│ └── telemetry/

├── src/ # Scripts de ETL (extract, transform, load)

├── config/ # API keys y conexión a base de datos

│   ├── db_config.py

│   └── pubg_api_config.py

├── notebooks/ # Notebooks para exploración

├── run_pipeline.py # Script principal de ejecución

├── requirements.txt # Dependencias del proyecto

└── README.md # Esta documentación

---

### 🚀 Próximos pasos

Este repositorio irá evolucionando. Próximas tareas que ya estoy trabajando:
- Modularizar el código en formato `script.py` con funciones claras
- Crear visualizaciones exploratorias
- Explorar una interfaz sencilla para consultas dinámicas
- Agregar validación de calidad de datos
- Automatizar con Airflow o Prefect
- Dockerizar el entorno para facilitar despliegue
- Incluir tests unitarios con `pytest`

---

### 📚 Objetivo del proyecto

Este no es un proyecto de iniciación, sino una forma de **practicar, consolidar y mostrar habilidades reales** de ingeniería de datos trabajando con una fuente de datos externa real, compleja y dinámica.

Busco seguir ampliando mi experiencia profesional y, al mismo tiempo, tener un espacio donde experimentar ideas, probar tecnologías y demostrar cómo pienso y estructuro mis soluciones.

Mi meta es convertir este repositorio en un proyecto demostrativo robusto y escalable, útil como portfolio y también como base para otros proyectos ETL con APIs públicas.

---

### 📬 Feedback bienvenido

Todo comentario, consejo o sugerencia técnica es más que bienvenido. ¡Gracias por pasar!

---
