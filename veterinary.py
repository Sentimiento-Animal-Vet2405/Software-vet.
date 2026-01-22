import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; border-right: 2px solid #7dd3fc; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0f2fe; margin-bottom: 15px; }
    .stButton>button { background: #0284c7 !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; }
    .hosp-alert { background: #fee2e2; border-left: 5px solid #ef4444; padding: 10px; border-radius: 5px; margin-bottom: 5px; }
    p, h1, h2, h3, label, span { color: #02456e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS (AUTO-CREACIÓN) ---
DB_CONFIG = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo"],
    "mascotas.csv": ["Doc_Dueño", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Peso"],
    "historias.csv": ["Fecha", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab"],
    "hospitalizados.csv": ["Mascota", "Estado", "Motivo", "Fecha_Ingreso"]
}

for db, cols in DB_CONFIG.items():
    if not os.path.exists(db) or os.stat(db).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(db, index=False)

def cargar(db):
    return pd.read_csv(db)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("SISTEMA INTEGRAL", ["🏠 Dashboard", "🩺 Consulta Full", "🏥 Hospitalización", "📥 Migrar OkVet"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Resumen de la Clínica")
    df_p = cargar("propietarios.csv")
    df_m = cargar("mascotas.csv")
    df_h = cargar("hospitalizados.csv")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes", len(df_p))
    col2.metric("Pacientes", len(df_m))
    col3.metric("En Hospital", len(df_h))
    
    st.subheader("🚨 Pacientes Internados")
    if not df_h.empty:
        for i, r in df_h.iterrows():
            st.markdown(f"<div class='hosp-alert'>🐶 <b>{r['Mascota']}</b> - Estado: {r['Estado']}<br><small>{r['Motivo']}</small></div>", unsafe_allow_html=True)
    else:
        st.info("No hay pacientes en hospital en este momento.")

# --- 2. CONSULTA FULL (SOIP + VACUNAS + LABS) ---
elif menu == "🩺 Consulta Full":
    st.title("🩺 Estación Médica Integral")
    df_m = cargar("mascotas.csv")
    
    if df_m.empty:
        st.warning("Debe cargar pacientes desde 'Migrar OkVet' primero.")
    else:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Nombre_Mascota"].tolist())
        
        t1, t2, t3 = st.tabs(["📝 Historia SOIP", "💉 Vacunas y Desp.", "🧪 Labs y Remisión"])
        
        with t1:
            col_a, col_b = st.columns(2)
            sub = col_a.text_area("Subjetivo (Anamnesis)")
            obj = col_b.text_area("Objetivo (Examen Físico)")
            int_p = col_a.text_area("Interpretación (Diagnóstico)")
            plan = col_b.text_area("Plan (Tratamiento)")
        
        with t2:
            vac = st.text_input("Vacuna Aplicada")
            desp = st.text_input("Desparasitación")
        
        with t3:
            lab_sol = st.text_area("Laboratorios Solicitados")
            remit = st.text_area("Remisión a Especialista")

        if st.button("💾 Guardar Consulta y Generar Reporte"):
            df_his = cargar("historias.csv")
            nueva_h = {"Fecha": datetime.now().strftime("%Y-%m-%d"), "Mascota": paciente, "S": sub, "O": obj, "I": int_p, "P": plan, "Vacunas": vac, "Lab": lab_sol}
            pd.concat([df_his, pd.DataFrame([nueva_h])]).to_csv("historias.csv", index=False)
            st.success("¡Historia guardada!")
            st.balloons()

# --- 3. HOSPITALIZACIÓN ---
elif menu == "🏥 Hospitalización":
    st.title("🏥 Módulo de Internamiento")
    df_m = cargar("mascotas.csv")
    
    with st.form("hosp_form"):
        p_hosp = st.selectbox("Paciente a ingresar:", df_m["Nombre_Mascota"].tolist() if not df_m.empty else ["Sin datos"])
        estado = st.selectbox("Estado:", ["Estable", "Reservado", "Crítico"])
        motivo = st.text_area("Motivo de ingreso y observaciones")
        if st.form_submit_button("Confirmar Ingreso"):
            df_hos = cargar("hospitalizados.csv")
            pd.concat([df_hos, pd.DataFrame([{"Mascota":p_hosp, "Estado":estado, "Motivo":motivo, "Fecha_Ingreso": datetime.now()}])]).to_csv("hospitalizados.csv", index=False)
            st.success("Paciente ingresado a hospitalización.")

# --- 4. MIGRACIÓN ---
elif menu == "📥 Migrar OkVet":
    st.title("📥 Importador de OkVet")
    target = st.selectbox("¿Qué archivo va a subir?", ["propietarios.csv", "mascotas.csv"])
    f = st.file_uploader("Suba su archivo (Preferiblemente CSV)", type=["csv", "xlsx"])
    
    if f:
        try:
            df_up = pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f, sep=None, engine='python')
            st.dataframe(df_up.head())
            if st.button("🚀 Procesar Migración"):
                df_up.to_csv(target, index=False)
                st.success("¡Migración terminada!")
        except:
            st.error("Error al leer. Intente guardar su Excel como 'CSV (delimitado por comas)'.")
            
