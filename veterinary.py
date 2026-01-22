import streamlit as st
import pandas as pd
import os

# --- ESTÉTICA CIELO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("<style>html, body, [class*='css'] { background-color: #f0f9ff; color: black !important; }</style>", unsafe_allow_html=True)

# --- FUNCIÓN DE LECTURA BLINDADA ---
def leer_archivo_seguro(nombre_archivo, columnas):
    # Si el archivo no existe o está vacío, creamos uno nuevo en memoria
    if not os.path.exists(nombre_archivo) or os.stat(nombre_archivo).st_size == 0:
        df_vacio = pd.DataFrame(columns=columnas)
        df_vacio.to_csv(nombre_archivo, index=False)
        return df_vacio
    try:
        # Intentamos leer, si falla (EmptyDataError), devolvemos tabla limpia
        df = pd.read_csv(nombre_archivo)
        if df.empty:
            return pd.DataFrame(columns=columnas)
        return df
    except Exception:
        return pd.DataFrame(columns=columnas)

# --- INICIALIZACIÓN ---
cols_p = ["Nombre", "Documento", "Telefono"]
cols_m = ["Dueño", "Mascota", "Especie"]

# --- INTERFAZ ---
st.title("🐾 Sentimiento Animal - Dra. Camila")

menu = st.sidebar.radio("MENÚ", ["🏠 Inicio", "📥 Cargar OkVet", "🩺 Consulta"])

if menu == "🏠 Inicio":
    # Aquí es donde fallaba antes, ahora está protegido
    df_p = leer_archivo_seguro("propietarios.csv", cols_p)
    df_m = leer_archivo_seguro("mascotas.csv", cols_m)
    
    st.metric("Clientes", len(df_p))
    st.metric("Mascotas", len(df_m))
    
    if len(df_p) == 0:
        st.info("El sistema está listo. Por favor cargue sus datos en el menú de la izquierda.")

elif menu == "📥 Cargar OkVet":
    st.header("📥 Cargar Datos")
    target = st.selectbox("Seleccione destino", ["propietarios.csv", "mascotas.csv"])
    archivo = st.file_uploader("Suba su archivo CSV", type=["csv"])
    
    if archivo:
        df_subido = pd.read_csv(archivo, sep=None, engine='python')
        st.write("Vista previa:")
        st.dataframe(df_subido.head())
        if st.button("Guardar Datos"):
            df_subido.to_csv(target, index=False)
            st.success("Guardado. Reinicie la página.")
            st.balloons()
            
