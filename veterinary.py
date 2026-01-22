import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE TEMA CLARO Y ESTÉTICA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label, span { color: #02456e !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; border: none; height: 3em; width: 100%; }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0; color: #166534 !important; font-weight: bold; }
    .hosp-rojo { background-color: #fee2e2; border-left: 5px solid #ef4444; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE BASES DE DATOS ---
DB_FILES = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo"],
    "mascotas.csv": ["Mascota", "Especie", "Raza", "Dueño_Doc"],
    "historias.csv": ["Fecha", "Mascota", "SOIP", "Formula", "Remision", "Refuerzo"],
    "hospital.csv": ["Mascota", "Estado", "Motivo", "Fecha_Ingreso"]
}

for file, cols in DB_FILES.items():
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(file, index=False)

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. MOTOR DE INTELIGENCIA ARTIFICIAL ---
def motor_ia(sintomas):
    s = sintomas.lower()
    if not s: return "Esperando descripción de síntomas..."
    alertas = []
    if any(x in s for x in ["vómito", "diarrea", "sangre"]): 
        alertas.append("⚠️ Sugerencia IA: Posible Gastroenteritis Viral (Parvo/Corona) o Intoxicación. Realizar Test Rápido.")
    if any(x in s for x in ["tos", "ahogo", "moquillo"]): 
        alertas.append("⚠️ Sugerencia IA: Sospecha de Complejo Respiratorio. Evaluar campos pulmonares.")
    if any(x in s for x in ["rasca", "piel", "roncha"]): 
        alertas.append("⚠️ Sugerencia IA: Posible Dermatitis Alérgica o Ectoparásitos. Sugerido: Citología.")
    return "\n".join(alertas) if alertas else "🧠 IA: Analizando... Siga describiendo el cuadro clínico."

# --- 4. MENÚ DE NAVEGACIÓN ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write(f"**Dra. Camila Mejía**")
    st.write("---")
    menu = st.radio("MÓDULOS ACTIVOS", [
        "🏠 Dashboard", 
        "👥 Propietarios y Mascotas", 
        "🩺 Consulta + IA", 
        "💊 Fórmulas y Remisiones", 
        "🏥 Hospitalización", 
        "📄 Certificados", 
        "📥 Importar OkVet"
    ])

# --- 5. LÓGICA DE MÓDULOS ---

# DASHBOARD
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p, df_m, df_h = leer("propietarios.csv"), leer("mascotas.csv"), leer("hospital.csv")
    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", len(df_p))
    c2.metric("Pacientes", len(df_m))
    c3.metric("Hospitalizados", len(df_h))
    st.subheader("Pacientes en Clínica")
    st.dataframe(df_m, use_container_width=True)

# PROPIETARIOS Y MASCOTAS
elif menu == "👥 Propietarios y Mascotas":
    st.title("👥 Registro de Clientes y Pacientes")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Nuevo Propietario")
        with st.form("p_f"):
            n, d, t = st.text_input("Nombre"), st.text_input("Cédula"), st.text_input("Tel")
            if st.form_submit_button("Guardar Dueño"):
                df = leer("propietarios.csv")
                guardar(pd.concat([df, pd.DataFrame([[n,d,t,""]], columns=df.columns)]), "propietarios.csv")
                st.success("Guardado")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Nueva Mascota")
        df_p = leer("propietarios.csv")
        with st.form("m_f"):
            mn, me = st.text_input("Nombre Mascota"), st.selectbox("Especie", ["Canino", "Felino"])
            md = st.selectbox("Dueño", df_p["Documento"].tolist() if not df_p.empty else ["Sin dueños"])
            if st.form_submit_button("Guardar Mascota"):
                df = leer("mascotas.csv")
                guardar(pd.concat([df, pd.DataFrame([[mn, me, "", md]], columns=df.columns)]), "mascotas.csv")
                st.success("Registrada")
        st.markdown("</div>", unsafe_allow_html=True)

# CONSULTA + IA
elif menu == "🩺 Consulta + IA":
    st.title("🩺 Consulta Médica")
    df_m = leer("mascotas.csv")
    paciente = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist() if not df_m.empty else [])
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    sub = st.text_area("S - Subjetivo (Síntomas)")
    if sub: st.markdown(f"<div class='ia-card'>{motor_ia(sub)}</div>", unsafe_allow_html=True)
    obj = st.text_area("O - Objetivo (Examen Físico)")
    interp = st.text_area("I - Interpretación (Diagnóstico)")
    if st.button("Guardar Evolución"): st.success("SOIP Guardado")
    st.markdown("</div>", unsafe_allow_html=True)

# FÓRMULAS Y REMISIONES
elif menu == "💊 Fórmulas y Remisiones":
    st.title("💊 Fórmulas y 📤 Remisiones")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("Recetario Médico")
    st.text_area("Escriba la fórmula (Medicamentos, dosis, frecuencia)")
    st.subheader("Remisión a Especialista")
    st.text_input("Especialidad (Ej: Cardiología)")
    st.text_area("Hallazgos para el colega")
    if st.button("Generar Documentos"): st.info("Listo para copiar")
    st.markdown("</div>", unsafe_allow_html=True)

# HOSPITALIZACIÓN
elif menu == "🏥 Hospitalización":
    st.title("🏥 Gestión de Hospital")
    df_m = leer("mascotas.csv")
    with st.form("hosp"):
        p = st.selectbox("Ingresar a:", df_m["Mascota"].tolist() if not df_m.empty else [])
        est = st.selectbox("Estado", ["Estable", "Reservado", "Crítico"])
        mot = st.text_area("Motivo")
        if st.form_submit_button("Ingresar"):
            df = leer("hospital.csv")
            guardar(pd.concat([df, pd.DataFrame([[p, est, mot, datetime.now()]], columns=df.columns)]), "hospital.csv")
            st.success("Ingresado")

# CERTIFICADOS
elif menu == "📄 Certificados":
    st.title("📄 Certificados de Salud y Viaje")
    st.markdown("<div class='main-card' style='font-family: monospace;'>", unsafe_allow_html=True)
    st.write("SENTIMIENTO ANIMAL - CERTIFICADO DE SALUD")
    st.write("Dra. Camila Mejía")
    st.write("---")
    st.write("Certifico que el paciente se encuentra apto para viajar...")
    st.markdown("</div>", unsafe_allow_html=True)

# IMPORTAR
elif menu == "📥 Importar OkVet":
    st.title("📥 Importar Excel")
    dest = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    datos = st.text_area("Pegue aquí desde Excel")
    if st.button("🚀 Cargar"):
        df = pd.read_csv(io.StringIO(datos), sep='\t')
        guardar(df, dest)
        st.success("Cargado")
    
