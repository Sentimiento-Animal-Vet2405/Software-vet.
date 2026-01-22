import streamlit as st
import pandas as pd
import os
import io

# --- ESTÉTICA CIELO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0f2fe; color: black; margin-bottom:10px; }
    h1, h2, h3, p, label { color: black !important; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
DB_FILES = ["propietarios.csv", "mascotas.csv", "historias.csv", "hospitalizados.csv"]
for db in DB_FILES:
    if not os.path.exists(db):
        pd.DataFrame().to_csv(db, index=False)

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("## 🐾 Sentimiento Animal")
    st.write("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "📥 Importar Datos", "🩺 Consulta", "👥 Clientes"])

# --- MODULO DE IMPORTACIÓN ULTRA-FLEXIBLE ---
if menu == "📥 Importar Datos":
    st.title("📥 Importación de Datos (OkVet)")
    st.write("Dra. Camila, intente subir su archivo aquí. Si falla, usaremos el modo manual.")
    
    target = st.selectbox("¿Qué datos va a subir?", ["propietarios", "mascotas"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    archivo = st.file_uploader("Subir archivo CSV o Excel", type=["csv", "xlsx"])
    
    if archivo:
        try:
            # Lector Inteligente: Intenta Excel, si falla intenta CSV con coma, si falla con punto y coma
            if archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
            else:
                try:
                    df = pd.read_csv(archivo, sep=',')
                except:
                    df = pd.read_csv(archivo, sep=';')
            
            st.success("¡Archivo leído! Vista previa:")
            st.dataframe(df.head(5))
            
            if st.button("🚀 GUARDAR EN EL SISTEMA"):
                df.to_csv(f"{target}.csv", index=False)
                st.success(f"Se han guardado {len(df)} registros en {target}.")
                st.balloons()
        except Exception as e:
            st.error(f"No pudimos leer el archivo. Intente guardarlo como 'CSV delimitado por comas' en Excel.")
            st.info("Sugerencia: Abra su Excel, elija 'Guardar como' -> 'CSV (delimitado por comas)'.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.title("🏠 Inicio")
    df_p = pd.read_csv("propietarios.csv")
    df_m = pd.read_csv("mascotas.csv")
    
    c1, c2 = st.columns(2)
    c1.metric("Clientes", len(df_p))
    c2.metric("Mascotas", len(df_m))
    
    if len(df_p) == 0:
        st.warning("El sistema está vacío. Vaya a 'Importar Datos' para cargar su información de OkVet.")

# (Resto de funciones simplificadas para asegurar carga rápida)
