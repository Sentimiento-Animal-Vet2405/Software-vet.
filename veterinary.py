import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, timedelta

# --- CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Sentimiento Animal Elite - IA", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f8fafc; color: #1e293b !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    .stButton>button { background: #0284c7 !important; color: white !important; font-weight: bold; border-radius: 10px; }
    .ia-card { background: #f0fdf4; padding: 20px; border-radius: 15px; border: 1px solid #bbf7d0; margin-top: 10px; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 15px; }
    h1, h2, h3 { color: #0c4a6e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
DB_NAMES = ["propietarios.csv", "mascotas.csv", "historias.csv"]
for db in DB_NAMES:
    if not os.path.exists(db): pd.DataFrame().to_csv(db, index=False)

def leer(n):
    try: return pd.read_csv(n)
    except: return pd.DataFrame()

# --- LÓGICA DE IA DIAGNÓSTICA ---
def asistente_ia(sintomas):
    sintomas = sintomas.lower()
    sugerencias = []
    if "vómito" in sintomas or "diarrea" in sintomas:
        sugerencias.append("🚨 Diferenciales: Parvovirus, Gastroenteritis hemorrágica, Cuerpo extraño.")
        sugerencias.append("🧪 Sugerencia: Cuadro hemático, Test de Parvo, Ecografía abdominal.")
    if "tos" in sintomas or "estornudo" in sintomas:
        sugerencias.append("🚨 Diferenciales: Complejo respiratorio felino/canino, Colapso traqueal.")
        sugerencias.append("🧪 Sugerencia: Placa de tórax, PCR respiratorio.")
    if "rasca" in sintomas or "piel" in sintomas or "pelo" in sintomas:
        sugerencias.append("🚨 Diferenciales: DAPP, Dermatitis atópica, Sarna sarcóptica.")
        sugerencias.append("🧪 Sugerencia: Raspado de piel, Citología cutánea.")
    
    if not sugerencias:
        return "🧠 IA: Analizando... Describa más síntomas (vómito, tos, picazón) para dar sugerencias clínicas."
    return "\n".join(sugerencias)

# --- MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    tarjeta = st.text_input("Tarjeta Profesional:", "TP-XXXX-MV")
    menu = st.radio("MÓDULOS", ["🏠 Dashboard", "🩺 Consulta + IA", "🏥 Hospitalización", "📄 Certificados", "📥 Carga OkVet"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Resumen de Clínica")
    df_p, df_m = leer("propietarios.csv"), leer("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Clientes", len(df_p))
    c2.metric("Pacientes", len(df_m))
    st.dataframe(df_m.tail(5), use_container_width=True)

# --- 2. CONSULTA + IA ---
elif menu == "🩺 Consulta + IA":
    st.title("🩺 Estación Médica con IA")
    df_m = leer("mascotas.csv")
    if df_m.empty:
        st.warning("Cargue pacientes primero.")
    else:
        nombres = df_m.iloc[:, 1].tolist() if len(df_m.columns) > 1 else df_m.iloc[:, 0].tolist()
        paciente = st.selectbox("Seleccione Paciente:", nombres)
        
        tab1, tab2, tab3 = st.tabs(["📝 Historia SOIP", "💊 Fórmulas/Remisión", "💉 Preventivos"])
        
        with tab1:
            st.subheader("Evolución SOIP")
            s = st.text_area("S - Subjetivo (Síntomas detectados)")
            
            # Módulo de IA Activo
            if s:
                st.markdown("<div class='ia-card'>", unsafe_allow_html=True)
                st.write("🤖 **Sugerencia IA Diagnóstica:**")
                st.info(asistente_ia(s))
                st.markdown("</div>", unsafe_allow_html=True)
                
            o = st.text_area("O - Objetivo (Examen físico)")
            i = st.text_area("I - Interpretación")
            p = st.text_area("P - Plan")
        
        with tab2:
            st.subheader("💊 Fórmula y Remisión")
            formula = st.text_area("Recetario médico")
            remit = st.text_area("Remisión a especialistas")
            
        with tab3:
            st.subheader("💉 Preventivos")
            c1, c2 = st.columns(2)
            vac = c1.text_input("Vacuna")
            des = c2.text_input("Desparasitante")

        if st.button("💾 GUARDAR TODO"):
            st.success("Registro médico guardado exitosamente.")

# --- 3. CERTIFICADOS ---
elif menu == "📄 Certificados":
    st.title("📄 Generador de Documentos")
    df_m = leer("mascotas.csv")
    p_sel = st.selectbox("Paciente:", df_m.iloc[:, 1].tolist() if not df_m.empty else [])
    tipo = st.selectbox("Tipo:", ["Certificado de Salud (Viajes)", "Certificado de Vacunación"])
    
    st.markdown(f"""
    <div style='background: white; border: 2px solid #0c4a6e; padding: 40px; border-radius: 10px;'>
        <h2 style='text-align: center;'>SENTIMIENTO ANIMAL</h2>
        <p style='text-align: center;'>Dra. Camila Mejía - Médica Veterinaria<br>Matrícula: {tarjeta}</p>
        <hr>
        <h3 style='text-align: center;'>{tipo.upper()}</h3>
        <p>Se certifica que la mascota <b>{p_sel}</b> se encuentra en buen estado de salud...</p>
        <br><br>
        <p style='text-align: center;'>__________________________<br>Firma Médica</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. CARGA OKVET ---
elif menu == "📥 Carga OkVet":
    st.title("📥 Carga de Datos")
    target = st.selectbox("Archivo:", ["propietarios.csv", "mascotas.csv"])
    datos = st.text_area("Pegue desde Excel:")
    if st.button("🚀 Cargar"):
        df = pd.read_csv(io.StringIO(datos), sep='\t')
        df.to_csv(target, index=False)
        st.success("¡Datos sincronizados!")
        
