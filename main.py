from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import engine, create_db_and_tables, get_session
from models import Tarea

# Configuración de plantillas (asegúrate de tener la carpeta 'templates')
templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de Tareas</title>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2092/2092175.png" type="image/png">
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


# Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 1. Mostrar tareas
@app.get("/tareas")
def obtener_tareas(session: Session = Depends(get_session)):
    return session.exec(select(Tarea)).all()


@app.get("/tareas-web", response_class=HTMLResponse)
def visualizar_tareas(request: Request, session: Session = Depends(get_session)):
    tareas = session.exec(select(Tarea)).all()
    return templates.TemplateResponse(
        request=request, 
        name="tareas.html", 
        context={"tareas": tareas}
    )


# 2. Crear tarea
@app.post("/tareas")
def crear_tarea(nueva_tarea: Tarea, session: Session = Depends(get_session)):
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    return {"mensaje": "Tarea creada con éxito", "tarea": nueva_tarea}


# 3. Eliminar tarea
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No encontré esa tarea")
    session.delete(tarea)
    session.commit()
    return {"mensaje": f"Tarea {tarea_id} eliminada"}


# 4. Marcar como completada
@app.put("/tareas/{tarea_id}/completar")
def marcar_tarea_completada(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    
    if not tarea:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")
    
    tarea.completada = True
    
    session.add(tarea)
    session.commit()
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