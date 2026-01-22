import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, date

# --- CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: ESTÉTICA CIELO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f9ff; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; border-right: 1px solid #7dd3fc; }
    [data-testid="stSidebar"] [data-testid="stImage"] img { border-radius: 50%; border: 3px solid white; }
    p, span, label, h1, h2, h3, .stMarkdown { color: #000000 !important; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0f2fe; margin-bottom: 20px; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 12px; font-weight: 700; height: 3rem; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE BASES DE DATOS (Vital para que no salga en blanco) ---
DB_FILES = {
    "propietarios": ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"],
    "mascotas": ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"],
    "historias": ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab", "Hosp"]
}

for db, cols in DB_FILES.items():
    if not os.path.exists(f"{db}.csv"):
        pd.DataFrame(columns=cols).to_csv(f"{db}.csv", index=False)

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENÚ PRINCIPAL", ["🏠 Dashboard", "👥 Clientes", "🐾 Pacientes", "🩺 Consulta IA", "📥 Importar de OkVet", "💾 Reportes"])

# --- MODULOS ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    st.info("Bienvenida Dra. Camila. Si acaba de migrar datos de OkVet, aparecerán aquí.")
    try:
        df_m = pd.read_csv("mascotas.csv")
        st.metric("Total Pacientes", len(df_m))
    except:
        st.write("Iniciando sistema...")

elif menu == "📥 Importar de OkVet":
    st.title("📥 Importar Datos")
    st.write("Use esta sección para cargar sus Excels.")
    # (Aquí iría el código de importación que ya tenemos)
    st.warning("Asegúrese de que el archivo 'requirements.txt' esté creado en GitHub para descargar plantillas.")

elif menu == "🩺 Consulta IA":
    st.title("🩺 Estación Médica")
    st.write("Seleccione un paciente para comenzar la consulta.")
    # Si las bases de datos están vacías, mostramos este mensaje amigable
    df_p = pd.read_csv("propietarios.csv")
    if df_p.empty:
        st.warning("Aún no hay clientes. Registre uno en el menú 'Clientes' o impórtelos de OkVet.")
    else:
        st.success("Lista de clientes cargada correctamente.")

# (Añada los demás bloques de código aquí)
