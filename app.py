import streamlit as st
import json
import datetime
import os
import webbrowser
from urllib.parse import quote

# --- Funciones de la aplicación ---

# Ruta del archivo de citas
ARCHIVO = "citas.json"

def cargar_citas():
    """Carga las citas desde el archivo JSON si existe, de lo contrario devuelve un diccionario vacío."""
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_citas(citas):
    """Guarda las citas en el archivo JSON."""
    with open(ARCHIVO, "w") as file:
        json.dump(citas, file, indent=4)

def agregar_cita(fecha, hora, cliente, servicio, telefono):
    """Función para agregar una nueva cita."""
    if not hora or not cliente or not servicio or not telefono:
        st.error("Completa todos los campos para guardar la cita.")
        return False

    citas = cargar_citas()
    
    # Asegúrate de que la fecha sea una clave válida en el diccionario
    if fecha not in citas:
        citas[fecha] = []

    # Verificar si la hora ya está ocupada
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
    """Abre la aplicación de llamadas del sistema."""
    webbrowser.open(f"tel:{numero_telefono}")

def enviar_whatsapp(numero_telefono, nombre_cliente):
    """Crea y abre un enlace de WhatsApp con un mensaje predefinido."""
    mensaje = f"Hola {nombre_cliente}, te recuerdo que tienes una cita en la barbería."
    mensaje_codificado = quote(mensaje)
    url_whatsapp = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
    webbrowser.open(url_whatsapp)

# --- Interfaz de usuario (UI) de Streamlit ---

# Configuración de la página
st.set_page_config(page_title="Agenda de Barbería", layout="wide")

# Título de la aplicación con un subtítulo
st.title("RonalsBarberShop")
st.markdown("### Gestión de Citas")
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
        # Título de la sección de citas
        st.subheader(f"Citas del día {hoy_str}")
        
        for cita in citas_existentes[hoy_str]:
            st.markdown(f"*Hora:* {cita['hora']} | *Cliente:* {cita['cliente']} | *Servicio:* {cita['servicio']}")
            
            # Crea columnas para alinear los botones
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                # Botón de llamada
                if st.button("Llamar", key=f"call_{cita['telefono']}_{cita['hora']}"):
                    hacer_llamada(cita['telefono'])
            with col2:
                # Botón de WhatsApp
                if st.button("WhatsApp", key=f"whatsapp_{cita['telefono']}_{cita['hora']}"):
                    enviar_whatsapp(cita['telefono'], cita['cliente'])

            st.markdown("---")
    else:
        st.write("No hay citas programadas para hoy.")
