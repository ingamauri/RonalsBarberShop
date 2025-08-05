import streamlit as st
import json
from datetime import datetime

# Ruta del archivo donde se guardarán las citas
ARCHIVO_CITAS = "citas.json"

# Cargar citas existentes
def cargar_citas():
    try:
        with open(ARCHIVO_CITAS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar cita
def guardar_cita(cita):
    citas = cargar_citas()
    citas.append(cita)
    with open(ARCHIVO_CITAS, "w") as f:
        json.dump(citas, f, indent=4)

# Interfaz de Streamlit
st.set_page_config(page_title="Agenda tu cita", page_icon="💈")
st.title("💈 Agenda tu cita en la barbería")

st.markdown("Completa el formulario para reservar tu cita.")

# Formulario
with st.form("form_cita"):
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Número de WhatsApp (ej: 18099846863)")
    servicio = st.selectbox("Servicio", ["Corte", "Barba", "Corte + Barba", "Coloración", "Otro"])
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")

    submit = st.form_submit_button("Reservar cita")

# Procesar cita
if submit:
    if not nombre or not telefono:
        st.warning("Por favor completa todos los campos.")
    else:
        cita = {
            "nombre": nombre,
            "telefono": telefono,
            "servicio": servicio,
            "fecha": str(fecha),
            "hora": str(hora),
            "confirmada": False
        }
        guardar_cita(cita)
        st.success("✅ ¡Cita reservada con éxito!")

        # Enlace de confirmación por WhatsApp
        mensaje = f"Hola {nombre}, tu cita está reservada para el {fecha} a las {hora} para {servicio}. ¡Gracias!"
        mensaje_codificado = mensaje.replace(" ", "%20")
        enlace = f"https://wa.me/{telefono}?text={mensaje_codificado}"

        st.markdown(f"[📩 Confirmar por WhatsApp]({enlace})")

# Mostrar citas (opcional)
if st.checkbox("Ver todas las citas agendadas"):
    citas = cargar_citas()
    if citas:
        for c in citas:
            st.write(f"📅 {c['fecha']} {c['hora']} - {c['nombre']} ({c['telefono']}) - {c['servicio']}")
    else:
        st.info("No hay citas agendadas todavía.")