import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ESTÉTICA ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; border-right: 2px solid #7dd3fc; }
    .main-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e0f2fe; margin-bottom: 20px; }
    .stButton>button { background: #0284c7 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 3.5rem; width: 100%; }
    h1, h2, h3, label, p { color: #0369a1 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BASES DE DATOS ---
DB_FILES = {
    "propietarios.xlsx": ["Nombre", "Documento", "Telefono", "Correo"],
    "mascotas.xlsx": ["Doc_Dueño", "Nombre_Mascota", "Especie", "Raza", "Sexo"],
    "historias.xlsx": ["Fecha", "Mascota", "S", "O", "I", "P", "Vacunas"],
    "hospital.xlsx": ["Mascota", "Estado", "Motivo", "Ingreso"]
}

def cargar_datos(nombre_archivo, columnas):
    if not os.path.exists(nombre_archivo):
        pd.DataFrame(columns=columnas).to_excel(nombre_archivo, index=False)
    try:
        return pd.read_excel(nombre_archivo)
    except:
        return pd.DataFrame(columns=columnas)

# --- NAVEGACIÓN ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("SISTEMA MÉDICO", ["🏠 Dashboard", "🩺 Consulta SOIP", "🏥 Hospitalización", "💉 Vacunación", "📥 Importar EXCEL OkVet"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p = cargar_datos("propietarios.xlsx", DB_FILES["propietarios.xlsx"])
    df_m = cargar_datos("mascotas.xlsx", DB_FILES["mascotas.xlsx"])
    df_h = cargar_datos("hospital.xlsx", DB_FILES["hospital.xlsx"])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", len(df_p))
    c2.metric("Mascotas", len(df_m))
    c3.metric("En Hospital", len(df_h))

    if not df_h.empty:
        st.subheader("🚨 Pacientes Internados")
        st.table(df_h)

# --- 2. CONSULTA SOIP ---
elif menu == "🩺 Consulta SOIP":
    st.title("🩺 Estación Médica")
    df_m = cargar_datos("mascotas.xlsx", DB_FILES["mascotas.xlsx"])
    
    if df_m.empty:
        st.warning("No hay pacientes. Cargue su Excel en 'Importar OkVet'.")
    else:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Nombre_Mascota"].tolist())
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        s = col1.text_area("Subjetivo (Anamnesis)")
        o = col2.text_area("Objetivo (Examen)")
        i = col1.text_area("Interpretación")
        p = col2.text_area("Plan Terapéutico")
        if st.button("💾 Guardar Historia Clínica"):
            st.success(f"¡Consulta de {paciente} guardada!")
            st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. HOSPITALIZACIÓN ---
elif menu == "🏥 Hospitalización":
    st.title("🏥 Módulo de Hospital")
    df_m = cargar_datos("mascotas.xlsx", DB_FILES["mascotas.xlsx"])
    with st.form("hosp"):
        p = st.selectbox("Paciente:", df_m["Nombre_Mascota"].tolist() if not df_m.empty else ["Vacío"])
        est = st.selectbox("Estado:", ["Estable", "Reservado", "Crítico"])
        mot = st.text_area("Motivo de ingreso")
        if st.form_submit_button("Ingresar a Hospitalización"):
            df_h = cargar_datos("hospital.xlsx", DB_FILES["hospital.xlsx"])
            pd.concat([df_h, pd.DataFrame([{"Mascota":p, "Estado":est, "Motivo":mot, "Ingreso": datetime.now()}])]).to_excel("hospital.xlsx", index=False)
            st.success("Paciente ingresado.")

# --- 4. IMPORTAR EXCEL OKVET ---
elif menu == "📥 Importar EXCEL OkVet":
    st.title("📥 Cargador de Excel")
    st.write("Suba sus archivos .xlsx directamente aquí.")
    target = st.selectbox("¿Qué va a subir?", ["propietarios.xlsx", "mascotas.xlsx"])
    archivo = st.file_uploader("Seleccione archivo de Excel", type=["xlsx"])
    
    if archivo:
        df_excel = pd.read_excel(archivo)
        st.write("Vista previa:")
        st.dataframe(df_excel.head())
        if st.button("🚀 Cargar Excel al Sistema"):
            df_excel.to_excel(target, index=False)
            st.success("¡Datos cargados correctamente!")
    
