import streamlit as st
import pandas as pd
import os

# --- ESTÉTICA PROFESIONAL ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0f2fe; color: black; }
    .stButton>button { background: #0284c7; color: white !important; font-weight: bold; width: 100%; border-radius: 10px; }
    p, h1, h2, h3, label { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ARCHIVOS ROBUSTO ---
def inicializar_y_leer(nombre_archivo, columnas):
    if not os.path.exists(nombre_archivo) or os.stat(nombre_archivo).st_size == 0:
        pd.DataFrame(columns=columnas).to_csv(nombre_archivo, index=False)
    try:
        return pd.read_csv(nombre_archivo)
    except:
        return pd.DataFrame(columns=columnas)

# Columnas necesarias
cols_p = ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo"]
cols_m = ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo"]

# --- MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write(f"**Dra. Camila Mejía**")
    st.write("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "📥 Cargar de OkVet", "🩺 Consulta"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Estado de la Clínica")
    df_p = inicializar_y_leer("propietarios.csv", cols_p)
    df_m = inicializar_y_leer("mascotas.csv", cols_m)
    
    c1, c2 = st.columns(2)
    c1.metric("Clientes", len(df_p))
    c2.metric("Mascotas", len(df_m))
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if len(df_p) == 0:
        st.info("👋 El sistema está listo. Vaya a 'Cargar de OkVet' para subir sus archivos.")
    else:
        st.success("✅ Base de datos activa y cargada.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. CARGADOR ULTRA-FLEXIBLE ---
elif menu == "📥 Cargar de OkVet":
    st.title("📥 Importar Archivos")
    st.write("Suba aquí sus archivos descargados de OkVet.")
    
    target = st.selectbox("¿Qué datos va a subir?", ["propietarios.csv", "mascotas.csv"])
    archivo = st.file_uploader("Seleccione el archivo (Excel o CSV)", type=["xlsx", "csv"])
    
    if archivo:
        try:
            # Lector universal
            if archivo.name.endswith('.xlsx'):
                df_nuevo = pd.read_excel(archivo)
            else:
                try: df_nuevo = pd.read_csv(archivo, sep=',')
                except: df_nuevo = pd.read_csv(archivo, sep=';')
            
            st.write("✅ **Vista previa de los datos:**")
            st.dataframe(df_nuevo.head(5))
            
            if st.button("🚀 GUARDAR DATOS EN EL SISTEMA"):
                df_nuevo.to_csv(target, index=False)
                st.success(f"¡Éxito! {len(df_nuevo)} registros cargados.")
                st.balloons()
        except Exception as e:
            st.error("Error al leer el archivo. Intente subir la versión .csv que ya tiene lista.")

# --- 3. CONSULTA (BÁSICA) ---
elif menu == "🩺 Consulta":
    st.title("🩺 Estación Médica")
    st.write("Módulo listo para recibir sus datos.")
                
