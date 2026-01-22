import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- CONFIGURACIÓN CIELO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], p, h1, h2, h3, label, span { color: #02456e !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; border: none; height: 3em; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
def leer(n):
    if os.path.exists(n):
        try:
            df = pd.read_csv(n)
            return df
        except: return pd.DataFrame()
    return pd.DataFrame()

def guardar(df, n):
    df.to_csv(n, index=False)

# --- MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("MÓDULOS", [
        "🏠 Dashboard", 
        "👥 Propietarios y Mascotas", 
        "🩺 Consulta + IA", 
        "💊 Fórmulas/Remisiones", 
        "🏥 Hospitalización", 
        "📄 Certificados", 
        "📥 Importar OkVet"
    ])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p = leer("propietarios.csv")
    df_m = leer("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Propietarios", len(df_p))
    c2.metric("Pacientes", len(df_m))
    st.write("### Base de Datos de Pacientes")
    st.dataframe(df_m, use_container_width=True)

# --- 2. PROPIETARIOS Y MASCOTAS (CORREGIDO) ---
elif menu == "👥 Propietarios y Mascotas":
    st.title("👥 Gestión de Clientes y Pacientes")
    tab1, tab2 = st.tabs(["👤 Registrar Propietario", "🐕 Anexar Mascota"])
    
    with tab1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        with st.form("nuevo_p"):
            n = st.text_input("Nombre Completo")
            d = st.text_input("Documento/Cédula")
            t = st.text_input("Teléfono")
            if st.form_submit_button("💾 Guardar"):
                df = leer("propietarios.csv")
                nueva_p = pd.DataFrame([[n, d, t]], columns=["Nombre", "Documento", "Telefono"])
                guardar(pd.concat([df, nueva_p]), "propietarios.csv")
                st.success("¡Guardado!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        df_p = leer("propietarios.csv")
        if df_p.empty or len(df_p.columns) < 2:
            st.warning("⚠️ No hay propietarios. Cargue datos en 'Importar OkVet' o registre uno manual.")
        else:
            # Seleccionamos la columna de nombre y documento sin importar cómo se llamen en el Excel
            df_p['Busqueda'] = df_p.iloc[:, 0].astype(str) + " (" + df_p.iloc[:, 1].astype(str) + ")"
            seleccion = st.selectbox("🔍 Buscar Propietario:", df_p['Busqueda'].tolist())
            doc_dueño = seleccion.split("(")[-1].replace(")", "")
            
            with st.form("nueva_m"):
                m_n = st.text_input("Nombre de la Mascota")
                m_e = st.selectbox("Especie", ["Canino", "Felino", "Otro"])
                if st.form_submit_button("🐾 Anexar Mascota"):
                    df_m = leer("mascotas.csv")
                    nueva_m = pd.DataFrame([[m_n, m_e, doc_dueño]], columns=["Mascota", "Especie", "Dueño"])
                    guardar(pd.concat([df_m, nueva_m]), "mascotas.csv")
                    st.success(f"{m_n} anexado a su dueño.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. IMPORTAR OKVET (EL TRADUCTOR) ---
elif menu == "📥 Importar OkVet":
    st.title("📥 Sincronización de Datos")
    target = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    st.info("Copie los datos de su Excel y péguelos aquí abajo.")
    datos = st.text_area("Cuadro de pegado (Ctrl+V):", height=200)
    
    if st.button("🚀 Procesar y Limpiar Datos"):
        if datos:
            try:
                df_up = pd.read_csv(io.StringIO(datos), sep='\t')
                # Forzamos que los nombres de las columnas sean los que el sistema necesita
                if target == "propietarios.csv":
                    df_up.columns = ["Nombre", "Documento", "Telefono"][:len(df_up.columns)]
                else:
                    df_up.columns = ["Mascota", "Especie", "Dueño"][:len(df_up.columns)]
                
                guardar(df_up, target)
                st.success("¡Información cargada correctamente!")
                st.rerun()
            except:
                st.error("Error al procesar. Intente copiar solo las filas con datos y sus títulos.")

# --- OTROS MÓDULOS ---
elif menu == "🩺 Consulta + IA":
    st.title("🩺 Consulta Médica")
    st.write("Módulo activo para diagnósticos.")

elif menu == "🏥 Hospitalización":
    st.title("🏥 Hospitalización")
    st.write("Control de internos.")

elif menu == "💊 Fórmulas/Remisiones":
    st.title("💊 Fórmulas")
    st.write("Generador de recetas.")
            
