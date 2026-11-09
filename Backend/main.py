from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.ciclo_vida import clasificar_paciente
from app.core.database import get_db_connection

app = FastAPI(
    title="API Agenda de Citas & Semaforización",
    version="1.0.0"
)

# Permitir que el Frontend (Streamlit) se comunique con el Backend sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema para recibir la solicitud de clasificación
class SolicitudClasificacion(BaseModel):
    fecha_nacimiento: str  # Formato YYYY-MM-DD

@app.get("/")
def home():
    return {"mensaje": "API de Citas funcionando correctamente "}

@app.post("/api/v1/pacientes/clasificar")
def endpoint_clasificar(datos: SolicitudClasificacion):
    """Endpoint para obtener la clasificación por grupo etario según el JSON."""
    try:
        resultado = clasificar_paciente(datos.fecha_nacimiento)
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/health-db")
def probar_base_datos():
    """Endpoint para verificar el estado de la conexión a Firebird."""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "ok", "base_datos": "Conectada a Firebird SALUSDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en BD: {str(e)}")
    
    # Cargar estados desde el JSON de semaforización
import json

def obtener_estados_config():
    with open("config/estados_asistencia.json", "r", encoding="utf-8") as f:
        return json.load(f)["estados"]

@app.get("/api/v1/citas/agenda")
def obtener_agenda_semaforizada():
    """Retorna la lista de citas con el color y estado de asistencia cargados desde el JSON."""
    estados = {e["id"]: e for e in obtener_estados_config()}
    
    # Datos de prueba estructurados (listos para mapear con la BD Firebird)
    citas_ejemplo = [
        {
            "id": 1,
            "paciente": "Carlos Mendoza",
            "grupo_etario": "Vejez",
            "fecha_hora": "2026-11-06 08:00 AM",
            "estado_id": "asistio"
        },
        {
            "id": 2,
            "paciente": "Lucía Gómez",
            "grupo_etario": "Primera Infancia",
            "fecha_hora": "2026-11-06 09:00 AM",
            "estado_id": "no_asistio"
        },
        {
            "id": 3,
            "paciente": "Andrés Pérez",
            "grupo_etario": "Juventud",
            "fecha_hora": "2026-11-06 10:30 AM",
            "estado_id": "pendiente"
        }
    ]
    
    # Inyectar los colores del JSON según el estado
    for cita in citas_ejemplo:
        info_estado = estados.get(cita["estado_id"], {})
        cita["estado_nombre"] = info_estado.get("nombre", "Desconocido")
        cita["color_hex"] = info_estado.get("color_hex", "#cccccc")
        
    return {"status": "success", "citas": citas_ejemplo}