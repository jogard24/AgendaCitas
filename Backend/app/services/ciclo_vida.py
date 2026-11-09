import json
from datetime import datetime

def clasificar_paciente(fecha_nacimiento_str: str) -> dict:
    """Calcula la edad y busca el grupo etario correspondiente en el JSON."""
    fecha_nac = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
    hoy = datetime.now()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    
    with open("config/grupos_etarios.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        
    for grupo in config["grupos_etarios"]:
        
        rango = grupo.get("rango_edad_anual") or grupo.get("rango_edad_anos")
        if rango ["min"] <= edad <= rango["max"]:
            
            return {
                "edad": edad,
                "grupo": grupo["nombre"],
                "requiere_acudiente": grupo["requiere_acudiente"],
                "duracion_minutos": grupo["duracion_cita_minutos"]
            }
            
    return {"edad": edad, "grupo": "No determinado", "requiere_acudiente": False, "duracion_minutos": 30}

if __name__ == "__main__":
    # Prueba con fecha de nacimiento ficticia (ej. 10 de mayo de 2018)
    resultado = clasificar_paciente("2018-05-10")
    print("Resultado de prueba:", resultado)