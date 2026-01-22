import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: ESTÉTICA CIELO (Letras negras y fondo celeste)
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; }
    .stButton>button { background: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0f2fe; margin-bottom: 10px; color: black; }
    .hosp-rojo { background: #fee2e2; border-left: 5px solid #ef4444; padding: 10px; border-radius: 8px; margin-bottom: 5px; }
    p, h1, h2, h3, label, span { color: #02456e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DATOS ROBUSTO ---
ARCHIVOS = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo"],
    "mascotas.csv": ["Doc_Dueño", "Nombre_Mascota", "Especie", "Raza", "Sexo"],
    "historias.csv": ["Fecha", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab"],
    "hospital.csv": ["Mascota", "Estado", "Motivo", "Fecha_Ingreso"]
}

for archivo, columnas in ARCHIVOS.items():
    if not os.path.exists(archivo) or os.stat(archivo).st_size == 0:
        pd.DataFrame(columns=columnas).to_csv(archivo, index=False)

def leer_datos(archivo):
    return pd.read_csv(archivo)

# --- NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write(f"**Dra. Camila Mejía**")
    st.write("---")
    menu = st.radio("SECCIONES DEL HOSPITAL", ["🏠 Dashboard", "🩺 Consulta SOIP", "🏥 Hospitalización", "💉 Vacunación", "🧪 Laboratorio", "📥 Importar OkVet"])

# --- 1. DASHBOARD (RESUMEN) ---
if menu == "🏠 Dashboard":
    st.title("🏠 Resumen del Hospital")
    df_p = leer_datos("propietarios.csv")
    df_m = leer_datos("mascotas.csv")
    df_h = leer_datos("hospital.csv")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", len(df_p))
    c2.metric("Pacientes", len(df_m))
    c3.metric("Hospitalizados", len(df_h))
    
    st.subheader("🚨 Alerta de Hospitalización")
    if not df_h.empty:
        for i, r in df_h.iterrows():
            st.markdown(f"<div class='hosp-rojo'><b>🐶 {r['Mascota']}</b> - {r['Estado']}<br>{r['Motivo']}</div>", unsafe_allow_html=True)
    else:
        st.info("No hay pacientes críticos internados.")

# --- 2. CONSULTA SOIP ---
elif menu == "🩺 Consulta SOIP":
    st.title("🩺 Historia Clínica (SOIP)")
    df_m = leer_datos("mascotas.csv")
    if df_m.empty:
        st.warning("Primero cargue pacientes en la sección 'Importar OkVet'.")
    else:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Nombre_Mascota"].unique())
        col1, col2 = st.columns(2)
        s = col1.text_area("Subjetivo (Anamnesis)")
        o = col2.text_area("Objetivo (Examen Físico)")
        i = col1.text_area("Interpretación (Diagnóstico)")
        p = col2.text_area("Plan (Tratamiento)")
        
        if st.button("💾 Guardar Historia Clínica"):
            df_his = leer_datos("historias.csv")
            nueva_h = {"Fecha": datetime.now().date(), "Mascota": paciente, "S": s, "O": o, "I": i, "P": p}
            pd.concat([df_his, pd.DataFrame([nueva_h])]).to_csv("historias.csv", index=False)
            st.success("¡Historia guardada exitosamente!")
            st.balloons()

# --- 3. HOSPITALIZACIÓN ---
elif menu == "🏥 Hospitalización":
    st.title("🏥 Control de Internamiento")
    df_m = leer_datos("mascotas.csv")
    with st.form("form_hosp"):
        p_hosp = st.selectbox("Paciente para ingreso:", df_m["Nombre_Mascota"].unique() if not df_m.empty else ["Sin datos"])
        est = st.selectbox("Estado de salud:", ["Estable", "Reservado", "Crítico"])
        mot = st.text_area("Motivo de hospitalización")
        if st.form_submit_button("Ingresar Paciente"):
            df_h = leer_datos("hospital.csv")
            pd.concat([df_h, pd.DataFrame([{"Mascota":p_hosp, "Estado":est, "Motivo":mot, "Fecha_Ingreso": datetime.now()}])]).to_csv("hospital.csv", index=False)
            st.success("Paciente registrado en hospital.")

# --- 4. IMPORTAR OKVET (EL MOTOR DE DATOS) ---
elif menu == "📥 Importar OkVet":
    st.title("📥 Carga de Datos desde OkVet")
    tipo = st.selectbox("¿Qué va a subir?", ["propietarios.csv", "mascotas.csv"])
    f = st.file_uploader("Suba su archivo CSV o Excel", type=["csv", "xlsx"])
    
    if f:
        try:
            # Lector flexible para evitar el error de openpyxl
            if f.name.endswith('xlsx'):
                df_up = pd.read_excel(f)
            else:
                df_up = pd.read_csv(f, sep=None, engine='python')
            
            st.write("✅ **Vista previa:**")
            st.dataframe(df_up.head())
            if st.button("🚀 Integrar al Sistema"):
                df_up.to_csv(tipo, index=False)
                st.success("¡Datos migrados! Ya puede verlos en el Dashboard.")
        except:
            st.error("Error al leer el archivo. Intente guardarlo como CSV en Excel.")
            
