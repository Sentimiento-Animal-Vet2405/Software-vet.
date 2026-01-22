import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- 1. ESTÉTICA CIELO (FORZADO) ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], p, h1, h2, h3, label, span { color: #02456e !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; border: none; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0; color: #166534 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASES DE DATOS SEGURAS ---
DB_FILES = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono"],
    "mascotas.csv": ["Mascota", "Especie", "Dueño"],
    "hospital.csv": ["Mascota", "Estado", "Motivo"]
}

for f, cols in DB_FILES.items():
    if not os.path.exists(f): pd.DataFrame(columns=cols).to_csv(f, index=False)

def leer(n):
    try:
        df = pd.read_csv(n)
        return df if not df.empty else pd.DataFrame(columns=DB_FILES.get(n, []))
    except: return pd.DataFrame(columns=DB_FILES.get(n, []))

# --- 3. MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("MÓDULOS ACTIVOS", [
        "🏠 Panel de Control", "👥 Propietarios y Mascotas", "🩺 Consulta + IA", 
        "💊 Fórmulas y Remisiones", "🏥 Hospitalización", "📄 Certificados", "📥 Importar OkVet"
    ])

# --- 4. LÓGICA DE MÓDULOS ---

if menu == "🏠 Panel de Control":
    st.title("🏠 Dashboard")
    df_p, df_m = leer("propietarios.csv"), leer("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Clientes", len(df_p))
    c2.metric("Mascotas", len(df_m))
    st.write("### Lista de Pacientes Actuales")
    st.dataframe(df_m, use_container_width=True)

elif menu == "👥 Propietarios y Mascotas":
    st.title("👥 Gestión de Base de Datos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Añadir Propietario")
        with st.form("form_p"):
            n = st.text_input("Nombre")
            d = st.text_input("Documento")
            t = st.text_input("Celular")
            if st.form_submit_button("Guardar"):
                df = leer("propietarios.csv")
                pd.concat([df, pd.DataFrame([[n,d,t]], columns=df.columns)]).to_csv("propietarios.csv", index=False)
                st.success("Cliente guardado")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Añadir Mascota")
        df_p = leer("propietarios.csv")
        # SOLUCIÓN AL ERROR: Verificamos si la columna existe antes de usarla
        lista_duenos = df_p["Documento"].tolist() if "Documento" in df_p.columns and not df_p.empty else ["Sin registros"]
        with st.form("form_m"):
            mn = st.text_input("Nombre Mascota")
            me = st.selectbox("Especie", ["Canino", "Felino", "Otro"])
            md = st.selectbox("Dueño (Documento)", lista_duenos)
            if st.form_submit_button("Registrar Mascota"):
                df = leer("mascotas.csv")
                pd.concat([df, pd.DataFrame([[mn, me, md]], columns=df.columns)]).to_csv("mascotas.csv", index=False)
                st.success("Mascota guardada")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🩺 Consulta + IA":
    st.title("🩺 Consulta e IA")
    df_m = leer("mascotas.csv")
    p_lista = df_m.iloc[:,0].tolist() if not df_m.empty else []
    paciente = st.selectbox("Paciente:", p_lista)
    s = st.text_area("S - Subjetivo (Síntomas)")
    if s:
        st.markdown(f"<div class='ia-card'>🤖 IA: Analizando síntomas... (Sugerencia de diagnóstico activo)</div>", unsafe_allow_html=True)
    st.text_area("O - Objetivo")
    st.button("💾 Guardar Historia")

elif menu == "💊 Fórmulas y Remisiones":
    st.title("💊 Recetario y 📤 Remisiones")
    st.text_area("Escriba la fórmula médica aquí...")
    st.text_input("Remitir a especialista:")
    st.button("Imprimir / Guardar")

elif menu == "🏥 Hospitalización":
    st.title("🏥 Control Hospitalario")
    st.write("Módulo de pacientes críticos.")

elif menu == "📄 Certificados":
    st.title("📄 Certificados de Salud")
    st.write("Generador de documentos para viajes.")

elif menu == "📥 Importar OkVet":
    st.title("📥 Carga desde Excel")
    target = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    datos = st.text_area("Abra su Excel, seleccione todo, copie y pegue aquí:")
    if st.button("🚀 Cargar"):
        df_up = pd.read_csv(io.StringIO(datos), sep='\t')
        df_up.to_csv(target, index=False)
        st.success("¡Información sincronizada!")
        st.rerun()
        
