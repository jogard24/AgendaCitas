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
    return {"mensaje": "API de Citas funcionando correctamente"}

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