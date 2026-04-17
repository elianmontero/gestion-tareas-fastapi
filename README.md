![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

📝 Task Manager API
Esta es una API RESTful desarrollada con FastAPI para la gestión de tareas (CRUD). El proyecto utiliza SQLModel para la interacción con la base de datos SQLite, permitiendo una persistencia de datos eficiente y una validación de tipos robusta.

🚀 Características
CRUD Completo: Crear, leer, actualizar y eliminar tareas.

Persistencia: Uso de SQLite para almacenar datos de forma local.

Documentación Automática: Interfaz interactiva con Swagger UI (/docs).

Arquitectura Limpia: Separación de modelos, base de datos y lógica de rutas.

🛠️ Tecnologías utilizadas
Python 3.x

FastAPI: Framework web de alto rendimiento.

SQLModel: Biblioteca para interactuar con bases de datos SQL usando objetos Python.

Uvicorn: Servidor ASGI para la ejecución de la API.

Pydantic: Validación de datos.

📦 Instalación y Configuración
1. Clonar el repositorio:

git clone https://github.com/tu-usuario/fastapi-task-manager.git
cd fastapi-task-manager

2. Crear y activar el entorno virtual:

python -m venv venv
# En Windows:
.\venv\Scripts\activate

3. Instalar dependencias:

pip install -r requirements.txt

💻 Ejecución
Para iniciar el servidor de desarrollo, ejecuta:

python -m uvicorn main:app --reload

Una vez encendido, puedes acceder a:
API: http://127.0.0.1:8000
