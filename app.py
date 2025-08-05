import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox
import os
import json
import datetime
import webbrowser
from urllib.parse import quote

# Configuración de customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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

def agregar_cita():
    """Función para agregar una nueva cita."""
    fecha = calendario.get_date()
    hora = entrada_hora.get()
    cliente = entrada_cliente.get()
    servicio = entrada_servicio.get()
    telefono = entrada_telefono.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

    if not hora or not cliente or not servicio or not telefono:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
        return

    citas = cargar_citas()
    
    # Asegúrate de que la fecha sea una clave válida en el diccionario
    if fecha not in citas:
        citas[fecha] = []

    # Verificar si la hora ya está ocupada
    for cita_existente in citas[fecha]:
        if cita_existente['hora'] == hora:
            messagebox.showerror("Hora ocupada", f"La hora {hora} ya está reservada para el {fecha}.")
            return

    nueva_cita = {
        "hora": hora,
        "cliente": cliente,
        "servicio": servicio,
        "telefono": telefono
    }
    
    citas[fecha].append(nueva_cita)
    guardar_citas(citas)
    messagebox.showinfo("Cita agregada", f"Cita para {cliente} guardada con éxito.")

    # Limpiar los campos después de guardar
    entrada_hora.delete(0, 'end')
    entrada_cliente.delete(0, 'end')
    entrada_servicio.delete(0, 'end')
    entrada_telefono.delete(0, 'end')

def hacer_llamada(numero_telefono):
    """Abre la aplicación de llamadas del sistema."""
    webbrowser.open(f"tel:{numero_telefono}")

def enviar_whatsapp(numero_telefono, nombre_cliente):
    """Crea y abre un enlace de WhatsApp con un mensaje predefinido."""
    mensaje = f"Hola {nombre_cliente}, te recuerdo que tienes una cita en la barbería."
    mensaje_codificado = quote(mensaje)
    url_whatsapp = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
    webbrowser.open(url_whatsapp)

def ver_citas():
    """Muestra las citas guardadas en una nueva ventana."""
    citas_existentes = cargar_citas()
    
    ventana_citas = ctk.CTkToplevel(app)
    ventana_citas.title("Citas del Día")
    ventana_citas.geometry("600x400")
    
    frame_citas = ctk.CTkScrollableFrame(ventana_citas)
    frame_citas.pack(padx=10, pady=10, fill="both", expand=True)

    hoy = datetime.date.today().strftime("%Y-%m-%d")
    
    if citas_existentes and hoy in citas_existentes:
        ctk.CTkLabel(frame_citas, text=f"--- Citas para hoy, {hoy} ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        
        for cita in citas_existentes[hoy]:
            cita_frame = ctk.CTkFrame(frame_citas)
            cita_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(cita_frame, text=f"Hora: {cita['hora']} | Cliente: {cita['cliente']} | Servicio: {cita['servicio']}").pack(side="left", padx=5)
            
            ctk.CTkButton(cita_frame, text="Llamar", command=lambda t=cita['telefono']: hacer_llamada(t)).pack(side="right", padx=5)
            
            ctk.CTkButton(cita_frame, text="WhatsApp", command=lambda t=cita['telefono'], m=cita['cliente']: enviar_whatsapp(t, m)).pack(side="right", padx=5)
    else:
        ctk.CTkLabel(frame_citas, text="No hay citas disponibles para hoy.").pack(pady=20)


# --- Interfaz de usuario (UI) ---
app = ctk.CTk()
app.title("Agenda Barberia")
app.geometry("480x540")

# Título de la aplicación con animación
titulo_label = ctk.CTkLabel(
    app,
    text="RonalsBarberShop",
    font=("Arial", 30, "bold")
)
titulo_label.pack(pady=10)

colores = ["blue", "purple", "green", "red", "orange"]
indice_color = 0

def animar_titulo():
    global indice_color
    titulo_label.configure(text_color=colores[indice_color])
    indice_color = (indice_color + 1) % len(colores)
    app.after(500, animar_titulo)

animar_titulo()

# Resto de los widgets de la interfaz
calendario = Calendar(app, selectmode='day', date_pattern="yyyy-mm-dd")
calendario.pack(pady=10)

ctk.CTkLabel(app, text="Hora (Ej: 10:30 AM):").pack(pady=5)
entrada_hora = ctk.CTkEntry(app)
entrada_hora.pack(pady=5)

ctk.CTkLabel(app, text="Nombre del Cliente:").pack(pady=5)
entrada_cliente = ctk.CTkEntry(app)
entrada_cliente.pack(pady=5)

ctk.CTkLabel(app, text="Número de Teléfono:").pack(pady=5)
entrada_telefono = ctk.CTkEntry(app)
entrada_telefono.pack(pady=5)

ctk.CTkLabel(app, text="Servicio (Ej: Corte, Barba):").pack(pady=5)
entrada_servicio = ctk.CTkEntry(app)
entrada_servicio.pack(pady=5)

ctk.CTkButton(app, text="Guardar Cita", command=agregar_cita).pack(pady=10)
ctk.CTkButton(app, text="Ver Citas del Día", command=ver_citas).pack(pady=10)

app.mainloop()
