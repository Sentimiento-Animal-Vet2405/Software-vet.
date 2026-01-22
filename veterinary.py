import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

# --- CONFIGURACIÓN ESTÉTICA AVANZADA ---
st.set_page_config(page_title="Sentimiento Animal - OkVet", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    .stButton>button { 
        border-radius: 8px; background-color: #2563eb; color: white; 
        font-weight: bold; height: 3.5rem; border: none;
    }
    .st-expander { background-color: white !important; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1, h2 { color: #1e293b; font-family: 'Helvetica Neue', sans-serif; }
    .card { background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
DB_PATH = "base_datos_vet.csv"
if not os.path.exists(DB_PATH):
    columnas = ["Fecha", "Mascota", "Propietario", "Tipo", "Detalles", "Peso", "T", "FC", "FR", "Plan"]
    pd.DataFrame(columns=columnas).to_csv(DB_PATH, index=False)

def guardar_registro(data):
    df = pd.read_csv(DB_PATH)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DB_PATH, index=False)

# --- MENÚ LATERAL ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png")
    st.title("OKVET SYSTEM")
    st.markdown("---")
    menu = st.radio("Navegación Profesional", [
        "🏠 Dashboard",
        "📋 Consulta (SOIP)",
        "🏥 Hospitalización",
        "💉 Vacunación",
        "💊 Fórmulas Médicas",
        "📂 Historial General"
    ])

# --- MÓDULO: HOSPITALIZACIÓN (Con Tabla de Constantes) ---
if menu == "🏥 Hospitalización":
    st.header("🏥 Registro de Hospitalización / Monitoreo")
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        paciente = c1.text_input("Paciente")
        propietario = c2.text_input("Propietario")
        fecha_ingreso = c3.date_input("Fecha de Ingreso")

        st.markdown("#### 📊 Monitoreo de Constantes Fisiológicas")
        # Tabla de constantes como en OkVet
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        temp = col_t1.text_input("T° (°C)")
        fc = col_t2.text_input("FC (lpm)")
        fr = col_t3.text_input("FR (rpm)")
        tllc = col_t4.text_input("TLLC (seg)")
        
        fluidos = st.text_area("Fluidoterapia y Medicación Intrahospitalaria")
        evolucion = st.text_area("Notas de Evolución Clínica")

        if st.button("💾 GUARDAR MONITOREO"):
            data = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Mascota": paciente, "Propietario": propietario,
                "Tipo": "Hospitalización", "T": temp, "FC": fc, "FR": fr,
                "Detalles": evolucion, "Plan": fluidos
            }
            guardar_registro(data)
            st.success("Registro de hospitalización guardado.")

# --- MÓDULO: VACUNACIÓN ---
elif menu == "💉 Vacunación":
    st.header("💉 Plan de Vacunación")
    with st.expander("Registrar Aplicación de Vacuna", expanded=True):
        col_v1, col_v2 = st.columns(2)
        v_paciente = col_v1.text_input("Nombre Mascota")
        v_tipo = col_v2.selectbox("Vacuna", ["Triple Felina", "Rabia", "Parvovirus/Moquillo", "Pentavalente", "Leucemia", "Otra"])
        
        v_lote = st.text_input("Lote / Marca de la Vacuna")
        v_proxima = st.date_input("Fecha sugerida de refuerzo")
        
        if st.button("💾 REGISTRAR VACUNA"):
            data = {"Fecha": datetime.now().strftime("%Y-%m-%d"), "Mascota": v_paciente, "Tipo": "Vacuna", "Detalles": f"{v_tipo} - Lote: {v_lote}", "Plan": f"Refuerzo: {v_proxima}"}
            guardar_registro(data)
            st.success("Vacuna registrada en el historial.")

# --- MÓDULO: CONSULTA SOIP (Repetimos para consistencia) ---
elif menu == "📋 Consulta (SOIP)":
    st.header("📋 Consulta Médica (SOIP)")
    with st.form("soip_form"):
        c1, c2 = st.columns(2)
        paciente = c1.text_input("Mascota")
        dueno = c2.text_input("Propietario")
        
        s = st.text_area("Subjetivo")
        o = st.text_area("Objetivo")
        i = st.text_area("Interpretación")
        p = st.text_area("Plan")
        
        if st.form_submit_button("💾 GUARDAR CONSULTA"):
            data = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Mascota": paciente, "Propietario": dueno, "Tipo": "Consulta", "Detalles": f"S:{s} O:{o} I:{i}", "Plan": p}
            guardar_registro(data)
            st.success("Consulta guardada.")

# --- MÓDULO: DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.header("🏠 Resumen Sentimiento Animal")
    df = pd.read_csv(DB_PATH)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Pacientes Totales", len(df["Mascota"].unique()))
    col_b.metric("Atenciones Mes", len(df))
    col_c.metric("Estado de Red", "Online ✅")
    
    st.markdown("### 📅 Últimas 5 Actividades")
    st.dataframe(df.tail(5), use_container_width=True)

# --- MÓDULO: HISTORIAL ---
elif menu == "📂 Historial General":
    st.header("📂 Buscador de Historias Clínicas")
    buscar = st.text
