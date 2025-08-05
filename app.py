import streamlit as st
import json
import datetime
import os
import webbrowser
from urllib.parse import quote

# --- Funciones de la aplicación (la lógica es casi la misma) ---

ARCHIVO = "citas.json"

def cargar_citas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_citas(citas):
    with open(ARCHIVO, "w") as file:
        json.dump(citas, file, indent=4)

def agregar_cita(fecha, hora, cliente, servicio, telefono):
    if not hora or not cliente or not servicio or not telefono:
        st.error("Completa todos los campos para guardar la cita.")
        return False

    citas = cargar_citas()
    
    if fecha not in citas:
        citas[fecha] = []

    for cita_existente in citas[fecha]:
        if cita_existente['hora'] == hora:
            st.error(f"La hora {hora} ya está reservada para el {fecha}.")
            return False

    nueva_cita = {
        "hora": hora,
        "cliente": cliente,
        "servicio": servicio,
        "telefono": telefono
    }
    
    citas[fecha].append(nueva_cita)
    guardar_citas(citas)
    st.success(f"Cita para {cliente} guardada con éxito.")
    return True

def hacer_llamada(numero_telefono):
    webbrowser.open(f"tel:{numero_telefono}")

def enviar_whatsapp(numero_telefono, nombre_cliente):
    mensaje = f"Hola {nombre_cliente}, te recuerdo que tienes una cita en la barbería."
    mensaje_codificado = quote(mensaje)
    url_whatsapp = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
    webbrowser.open(url_whatsapp)

# --- Interfaz de usuario (UI) de Streamlit ---

# Título de la aplicación
st.title("RonalsBarberShop")
st.write("---")

# Creación de pestañas para organizar la interfaz
tab1, tab2 = st.tabs(["Agendar Cita", "Ver Citas del Día"])

with tab1:
    st.header("Agendar nueva cita")
    
    # Widgets para agendar citas
    fecha_cita = st.date_input("Fecha de la cita", datetime.date.today())
    hora_cita = st.text_input("Hora (Ej: 10:30 AM)")
    nombre_cliente = st.text_input("Nombre del Cliente")
    telefono_cliente = st.text_input("Número de Teléfono")
    servicio_cita = st.text_input("Servicio (Ej: Corte, Barba)")

    if st.button("Guardar Cita"):
        fecha_str = fecha_cita.strftime("%Y-%m-%d")
        telefono_limpio = telefono_cliente.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        agregar_cita(fecha_str, hora_cita, nombre_cliente, servicio_cita, telefono_limpio)

with tab2:
    st.header("Citas para hoy")
    
    citas_existentes = cargar_citas()
    hoy_str = datetime.date.today().strftime("%Y-%m-%d")
    
    if citas_existentes and hoy_str in citas_existentes:
        for cita in citas_existentes[hoy_str]:
            st.markdown(f"*Hora:* {cita['hora']} | *Cliente:* {cita['cliente']} | *Servicio:* {cita['servicio']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Llamar", key=f"call_{cita['telefono']}", on_click=lambda t=cita['telefono']: hacer_llamada(t))
            with col2:
                st.button("WhatsApp", key=f"whatsapp_{cita['telefono']}", on_click=lambda t=cita['telefono'], m=cita['cliente']: enviar_whatsapp(t, m))
            st.write("---")
    else:
        st.write("No hay citas programadas para hoy.")
