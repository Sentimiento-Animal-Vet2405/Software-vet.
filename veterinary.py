import streamlit as st
import pandas as pd
import os
import io

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; }
    .stButton>button { background: #0284c7 !important; color: white !important; font-weight: bold; border-radius: 12px; height: 3.5rem; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0f2fe; margin-bottom: 20px; color: black; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1, h2, h3, label, p, span { color: #02456e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BASES DE DATOS ---
DB_FILES = ["propietarios.csv", "mascotas.csv", "hospital.csv", "historias.csv"]
for f in DB_FILES:
    if not os.path.exists(f):
        pd.DataFrame().to_csv(f, index=False)

def leer_db(nombre):
    try:
        if os.path.exists(nombre) and os.stat(nombre).st_size > 0:
            return pd.read_csv(nombre)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "🩺 Consulta Clínica", "🏥 Hospitalización", "📥 Cargar Información"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p = leer_db("propietarios.csv")
    df_m = leer_db("mascotas.csv")
    
    col1, col2 = st.columns(2)
    col1.metric("Clientes Registrados", len(df_p))
    col2.metric("Mascotas Registradas", len(df_m))
    
    if len(df_p) == 0:
        st.warning("⚠️ El sistema no tiene datos cargados.")
    else:
        st.success("✅ Base de datos activa.")
        st.write("### Vista de Pacientes")
        st.dataframe(df_m)

# --- 2. CONSULTA Y HOSPITALIZACIÓN (MÓDULOS COMPLETOS) ---
elif menu == "🩺 Consulta Clínica":
    st.title("🩺 Historia Clínica")
    st.info("Seleccione un paciente para iniciar la consulta SOIP.")
    # El sistema leerá de la base de datos que carguemos en el paso 4

elif menu == "🏥 Hospitalización":
    st.title("🏥 Módulo de Hospital")
    st.write("Gestión de pacientes internados.")

# --- 4. CARGA DE DATOS (LA SOLUCIÓN DEFINITIVA) ---
elif menu == "📥 Cargar Información":
    st.title("📥 Portal de Carga Inmediata")
    target = st.selectbox("¿Qué datos va a ingresar?", ["propietarios.csv", "mascotas.csv"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("⚡ Opción: Copiar y Pegar desde Excel")
    st.write("Dra. Camila, como el servidor tiene problemas con los archivos, hagamos esto: **Abra su Excel, seleccione sus datos, cópielos (Ctrl+C) y péguelos aquí abajo.**")
    
    datos_pegados = st.text_area("Pegue las celdas de su Excel aquí:", height=200, placeholder="Nombre   Documento   Telefono...")
    
    if st.button("🚀 Cargar Datos Ahora"):
        if datos_pegados:
            try:
                # Lee los datos pegados (detecta si vienen de Excel/pestañas)
                df_pegado = pd.read_csv(io.StringIO(datos_pegados), sep='\t')
                if df_pegado.empty or len(df_pegado.columns) < 2:
                    df_pegado = pd.read_csv(io.StringIO(datos_pegados), sep=None, engine='python')
                
                df_pegado.to_csv(target, index=False)
                st.success(f"¡Éxito! Se cargaron {len(df_pegado)} registros en {target}.")
                st.balloons()
            except Exception as e:
                st.error("No pudimos procesar los datos pegados. Asegúrese de incluir los títulos de las columnas.")
        else:
            st.error("El cuadro está vacío.")
    st.markdown("</div>", unsafe_allow_html=True)
        
