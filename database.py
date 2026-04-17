from sqlmodel import create_engine, SQLModel, Session
import models  # Importamos tus modelos para que SQLModel los conozca

# Nombre del archivo de la base de datos
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# El "Engine" es el motor que permite a Python hablar con SQLite
engine = create_engine(sqlite_url, echo=True) # echo=True muestra los comandos SQL en la terminal

def create_db_and_tables():
    # Esta función crea el archivo .db y las tablas basadas en tus modelos
    SQLModel.metadata.create_all(engine)

def get_session():
    # Esto nos da una "sesión" para trabajar (abrir/cerrar conexión)
    with Session(engine) as session:
        yield session