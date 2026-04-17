from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db_and_tables, get_session
from models import Tarea

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mi API de Tareas</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #f4f4f9; color: #333; padding: 50px; }
            .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; }
            h1 { color: #005571; }
            p { font-size: 1.1em; }
            .btn { background-color: #005571; color: white; padding: 10px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: background 0.3s; }
            .btn:hover { background-color: #0082ad; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 API de Gestión de Tareas</h1>
            <p>Bienvenido a mi primera API profesional desarrollada con <strong>FastAPI</strong> y <strong>SQLModel</strong>.</p>
            <p>Esta aplicación permite crear, editar y organizar tareas de forma eficiente.</p>
            <br>
            <a href="/docs" class="btn">Explorar Documentación (Swagger)</a>
        </div>
    </body>
    </html>
    """

# Esto crea las tablas en el archivo .db al arrancar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 1. Obtener todas las tareas
@app.get("/tareas")
def obtener_tareas(session: Session = Depends(get_session)):
    # Usamos select(Tarea) para pedirle a SQLModel que busque en la tabla
    tareas = session.exec(select(Tarea)).all()
    return tareas

# 2. Crear una tarea nueva
@app.post("/tareas")
def crear_tarea(nueva_tarea: Tarea, session: Session = Depends(get_session)):
    session.add(nueva_tarea) # Añade la instancia a la sesión
    session.commit()         # Guarda los cambios en el archivo .db
    session.refresh(nueva_tarea) # Actualiza el objeto (por ejemplo, para traer el ID)
    return {"mensaje": "Tarea creada con éxito", "tarea": nueva_tarea}

# 3. Eliminar tarea por ID
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea_por_id(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id) # Busca directamente por ID
    if not tarea:
        raise HTTPException(status_code=404, detail="No encontré esa tarea")
    
    session.delete(tarea) # Marca la tarea para borrar
    session.commit()      # Aplica el borrado en la base de datos
    return {"mensaje": f"Tarea {tarea_id} eliminada"}

# 4. Marcar como completada
@app.put("/tareas/{tarea_id}/completar")
def marcar_tarea_completada(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")
    
    tarea.completada = True
    session.add(tarea) # Notificamos el cambio
    session.commit()   # Guardamos
    session.refresh(tarea)
    return {"mensaje": f"Tarea {tarea_id} marcada como completada", "tarea": tarea}

# 5. Modificar título y descripción
@app.put("/tareas/{tarea_id}/tarea_modificada")
def cambiar_titulo_de_tarea(tarea_id: int, tarea_titulo: str, tarea_descripcion: str, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")
    
    tarea.titulo = tarea_titulo
    tarea.descripcion = tarea_descripcion
    
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return {"mensaje": f"Tarea {tarea_id} fue modificada con éxito", "tarea": tarea}

# Nota sobre "eliminar-ultima": 
# En bases de datos reales, no suele existir el concepto de "última" de forma automática 
# como en las listas, ya que el orden puede variar. 
# Es más seguro y profesional borrar siempre por ID.