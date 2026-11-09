import json
from datetime import datetime
from pathlib import Path

def clasificar_paciente(fecha_nacimiento_str: str) -> dict:
    fecha_nac = datetime.strptime(str(fecha_nacimiento_str), "%Y-%m-%d").date()
    hoy = datetime.now().date()
    
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    
    # Buscamos la carpeta config/ de forma dinámica
    base_dir = Path(__file__).resolve().parent.parent.parent
    json_path = base_dir / "config" / "grupos_etarios.json"
    
    if not json_path.exists():
        json_path = base_dir.parent / "config" / "grupos_etarios.json"
        
    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    for grupo in config["grupos_etarios"]:
        rango = (
            grupo.get("rango_edad_anual") or 
            grupo.get("rango_edad_anos") or 
            grupo.get("rango_edad_años")
        )
        
        if rango and (rango["min"] <= edad <= rango["max"]):
            return {
                "edad": edad,
                "grupo": grupo["nombre"],
                "requiere_acudiente": grupo.get("requiere_acudiente", False),
                "duracion_minutos": grupo.get("duracion_cita_minutos", 30)
            }
            
    return {"edad": edad, "grupo": "No determinado", "requiere_acudiente": False, "duracion_minutos": 30}