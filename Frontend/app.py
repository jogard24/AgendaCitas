import streamlit as st
import requests
from datetime import date

# Configuración de la página (Título e icono en la pestaña del navegador)
st.set_page_config(page_title="Agenda de Citas & Semaforización", layout="wide", page_icon="")

st.title(" Sistema de Gestión de Citas")
st.caption("Módulo de Clasificación de Pacientes y Semaforización")

st.divider()

# Sección 1: Formulario interactivo
st.subheader(" Clasificación de Paciente por Ciclo de Vida")

col1, col2 = st.columns([1, 2])

with col1:
    fecha_nacimiento = st.date_input(
        "Selecciona la Fecha de Nacimiento:",
        value=date(2018, 5, 15),
        max_value=date.today()
    )
    
    botan_consultar = st.button(" Clasificar Paciente", use_container_width=True)
    print(f"Botón presionado: {botan_consultar}, Fecha seleccionada: {fecha_nacimiento}")

# Sección 2: Respuesta y visualización
with col2:
    if botan_consultar:
        # Preparamos la petición HTTP para enviarla a nuestra "cocina" (FastAPI)
        url_api = "http://127.0.0.1:8000/api/v1/pacientes/clasificar"
        payload = {"fecha_nacimiento": fecha_nacimiento.strftime("%Y-%m-%d")}
        respuesta = requests.post(url_api, json=payload)
        
        try:
            respuesta = requests.post(url_api, json=payload)
            
            if respuesta.status_code == 200:
                datos = respuesta.json()["data"]
                
                # Pintamos el resultado en pantalla de forma bonita
                st.success(f"¡Pacientes clasificado con éxito!")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Edad Calculada", f"{datos['edad']} años")
                c2.metric("Grupo Etario", datos['grupo'])
                c3.metric("Duración Cita", f"{datos['duracion_minutos']} min")
                
                if datos['requiere_acudiente']:
                    st.warning(" **Atención:** Este paciente requiere la presencia de un acudiente obligatorio.")
                else:
                    st.info("ℹ El paciente puede asistir sin acudiente.")
            else:
                st.error("Ocurrió un error al procesar en la API.")
                
        except Exception as e:
            st.error(f"No se pudo conectar con el Backend (FastAPI). ¿Está encendido uvicorn? Error: {e}")
            
            st.divider()

st.subheader(" Agenda de Citas y Control de Asistencia (Semaforización)")

if st.button(" Cargar Citas Agendadas", use_container_width=False):
    try:
        res = requests.get("http://127.0.0.1:8000/api/v1/citas/agenda")
        if res.status_code == 200:
            citas = res.json()["citas"]
            
            # Dibujar cada cita como una tarjeta coloreada con HTML/CSS
            cols = st.columns(len(citas))
            for idx, cita in enumerate(citas):
                with cols[idx]:
                    html_card = f"""
                    <div style="
                        background-color: {cita['color_hex']};
                        padding: 15px;
                        border-radius: 10px;
                        color: white;
                        font-family: sans-serif;
                        margin-bottom: 10px;">
                        <h4 style="margin:0; color: white;">{cita['paciente']}</h4>
                        <p style="margin:5px 0 0 0; font-size: 0.9em;"><b>Grupo:</b> {cita['grupo_etario']}</p>
                        <p style="margin:2px 0 0 0; font-size: 0.85em;"><b>Hora:</b> {cita['fecha_hora']}</p>
                        <hr style="border: 0.5px solid rgba(255,255,255,0.3);">
                        <span style="background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8em;">
                            {cita['estado_nombre']}
                        </span>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.error("No se pudo obtener la agenda de citas.")
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")