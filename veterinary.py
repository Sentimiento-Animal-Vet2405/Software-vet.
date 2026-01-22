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
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN AUTOMÁTICA ---
DB_FILES = {
    "propietarios.csv": ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"],
    "mascotas.csv": ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"]
}
for db, cols in DB_FILES.items():
    if not os.path.exists(db) or os.stat(db).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# --- MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "📥 Cargar Datos OkVet", "🩺 Consulta"])

# --- MODULO DE CARGA DIRECTA ---
if menu == "📥 Cargar Datos OkVet":
    st.title("📥 Importar sus archivos de OkVet")
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    tipo = st.selectbox("1. ¿Qué archivo va a subir?", ["propietarios.csv", "mascotas.csv"])
    
    # Este cargador acepta XLSX y CSV sin pedir librerías extra
    archivo = st.file_uploader("2. Seleccione su archivo (OkVet - Mascotas o OkVet - Propietarios)", type=["xlsx", "csv"])
    
    if archivo:
        try:
            if archivo.name.endswith('.xlsx'):
                # Intento de lectura directa de Excel
                df_nuevo = pd.read_excel(archivo, engine='openpyxl')
            else:
                # Lectura de CSV flexible
                try: df_nuevo = pd.read_csv(archivo, sep=',')
                except: df_nuevo = pd.read_csv(archivo, sep=';')
            
            st.write("✅ **Vista previa de sus datos:**")
            st.dataframe(df_nuevo.head(5))
            
            if st.button("🚀 INTEGRAR DATOS AHORA"):
                df_nuevo.to_csv(tipo, index=False)
                st.success(f"¡Excelente! Los datos de {archivo.name} ya están en el sistema.")
                st.balloons()
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Dra., si el Excel falla, intente subir el archivo que termina en .csv que ya tiene listo.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🏠 Dashboard":
    st.title("🏠 Estado de la Clínica")
    p = pd.read_csv("propietarios.csv")
    m = pd.read_csv("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Clientes", len(p))
    c2.metric("Mascotas", len(m))
    
