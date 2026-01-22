import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- ESTÉTICA PROFESIONAL "MODO CIELO" ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], p, h1, h2, h3, label, span { color: #013a5d !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; border: none; height: 3em; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .info-box { background-color: #e0f2fe; padding: 15px; border-radius: 10px; border-left: 5px solid #0284c7; margin-bottom: 10px; }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0; color: #166534 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BASES DE DATOS ---
def leer(n):
    if os.path.exists(n):
        try: return pd.read_csv(n)
        except: return pd.DataFrame()
    return pd.DataFrame()

def guardar(df, n):
    df.to_csv(n, index=False)

# --- LÓGICA IA DIAGNÓSTICA ---
def analizar_ia(sintomas):
    s = sintomas.lower()
    if "vómito" in s or "diarrea" in s: return "🚨 IA: Sospecha de cuadro gastroentérico. Sugerencia: Test Parvo/Corona y Cuadro Hemático."
    if "tos" in s or "estornudo" in s: return "🚨 IA: Sospecha de afección respiratoria. Sugerencia: Auscultación pulmonar y Placa de Tórax."
    if "rasca" in s or "piel" in s: return "🚨 IA: Alerta dermatológica. Sugerencia: Raspado cutáneo y Citología."
    return "🧠 IA: Analizando... Describa más hallazgos para sugerencias diferenciales."

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write(f"**Dra. Camila Mejía**")
    st.write("---")
    menu = st.radio("MENÚ MÉDICO", [
        "🏠 Dashboard", 
        "👤 Registro Propietarios", 
        "🐕 Registro Pacientes", 
        "🩺 Consulta + IA", 
        "💊 Fórmulas y Remisiones", 
        "🏥 Hospitalización", 
        "📄 Certificados", 
        "📥 Importar OkVet"
    ])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Resumen de la Clínica")
    df_p, df_m = leer("propietarios.csv"), leer("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Propietarios", len(df_p))
    c2.metric("Pacientes", len(df_m))
    st.write("### Lista General de Pacientes")
    st.dataframe(df_m, use_container_width=True)

# --- 2. REGISTRO PROPIETARIOS ---
elif menu == "👤 Registro Propietarios":
    st.title("👤 Ficha del Propietario")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    with st.form("form_prop"):
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Nombre Completo")
        t_doc = c2.selectbox("Tipo de Documento", ["Cédula", "CE", "Pasaporte", "NIT"])
        n_doc = c1.text_input("Número de Documento")
        tel = c2.text_input("Teléfono / WhatsApp")
        mail = c1.text_input("Correo Electrónico")
        dir = c2.text_input("Dirección de Residencia")
        if st.form_submit_button("💾 Guardar Propietario"):
            df = leer("propietarios.csv")
            nuevo = pd.DataFrame([[nombre, t_doc, n_doc, tel, mail, dir]], 
                                 columns=["Nombre", "Tipo_Doc", "Documento", "Telefono", "Correo", "Direccion"])
            guardar(pd.concat([df, nuevo]), "propietarios.csv")
            st.success("Propietario registrado con éxito.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. REGISTRO PACIENTES ---
elif menu == "🐕 Registro Pacientes":
    st.title("🐕 Ficha del Paciente")
    df_p = leer("propietarios.csv")
    if df_p.empty:
        st.warning("Debe registrar un propietario primero.")
    else:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        # Buscador de Dueño
        df_p['Busqueda'] = df_p['Nombre'].astype(str) + " (" + df_p['Documento'].astype(str) + ")"
        dueno_sel = st.selectbox("Asignar a Propietario:", df_p['Busqueda'].tolist())
        doc_dueno = dueno_sel.split("(")[-1].replace(")", "")

        with st.form("form_pac"):
            c1, c2, c3 = st.columns(3)
            m_nom = c1.text_input("Nombre de la Mascota")
            m_esp = c2.selectbox("Especie", ["Canino", "Felino", "Exótico"])
            m_raz = c3.text_input("Raza")
            
            c4, c5, c6 = st.columns(3)
            m_sex = c4.selectbox("Sexo", ["Macho", "Hembra"])
            m_edad = c5.text_input("Edad (Ej: 2 años)")
            m_peso = c6.number_input("Peso Actual (Kg)", min_value=0.0, step=0.1)
            
            m_cas = st.radio("Estado Reproductivo", ["Castrado", "No Castrado"], horizontal=True)
            
            if st.form_submit_button("🐾 Registrar Mascota"):
                df = leer("mascotas.csv")
                nueva = pd.DataFrame([[m_nom, m_esp, m_raz, m_sex, m_edad, m_peso, m_cas, doc_dueno]], 
                                     columns=["Mascota", "Especie", "Raza", "Sexo", "Edad", "Peso", "Estado", "Dueño"])
                guardar(pd.concat([df, nueva]), "mascotas.csv")
                st.success(f"¡{m_nom} registrado!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. CONSULTA + IA ---
elif menu == "🩺 Consulta + IA":
    st.title("🩺 Estación Médica")
    df_m = leer("mascotas.csv")
    if df_m.empty:
        st.info("Registre pacientes para iniciar consultas.")
    else:
        paciente = st.selectbox("Seleccione Paciente para Consulta:", df_m["Mascota"].tolist())
        
        # FICHA RÁPIDA (Búsqueda automática de datos)
        datos_p = df_m[df_m["Mascota"] == paciente].iloc[0]
        st.markdown(f"""
        <div class='info-box'>
            <b>📌 Ficha Médica de {paciente}:</b><br>
            • Especie: {datos_p['Especie']} | Raza: {datos_p['Raza']} | Sexo: {datos_p['Sexo']}<br>
            • Edad: {datos_p['Edad']} | Peso: {datos_p['Peso']} Kg | Estado: {datos_p['Estado']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        sub = st.text_area("S - Subjetivo (Síntomas y motivo de consulta)")
        if sub: st.markdown(f"<div class='ia-card'>{analizar_ia(sub)}</div>", unsafe_allow_html=True)
        
        obj = st.text_area("O - Objetivo (Examen físico / Constantes)")
        inte = st.text_area("I - Interpretación (Diagnóstico presuntivo)")
        plan = st.text_area("P - Plan (Exámenes y pasos a seguir)")
        
        if st.button("💾 Guardar Historia Clínica"):
            st.success("Historia Clínica guardada.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. FÓRMULAS Y REMISIONES ---
elif menu == "💊 Fórmulas y Remisiones":
    st.title("💊 Recetario y 📤 Remisiones")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("💊 Fórmula Médica")
    st.text_area("Escriba medicamentos y dosis...")
    st.subheader("📤 Remisión")
    st.text_input("Especialista / Centro de Referencia")
    st.text_area("Motivo de remisión y hallazgos...")
    st.button("🖨️ Generar para Imprimir")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. HOSPITALIZACIÓN ---
elif menu == "🏥 Hospitalización":
    st.title("🏥 Pacientes en Hospital")
    st.write("Módulo de monitoreo de internos.")

# --- 7. CERTIFICADOS ---
elif menu == "📄 Certificados":
    st.title("📄 Certificados de Salud")
    st.write("Generador de documentos legales para viajes y vacunas.")

# --- 8. IMPORTAR OKVET ---
elif menu == "📥 Importar OkVet":
    st.title("📥 Importar desde Excel")
    dest = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    datos = st.text_area("Pegue las celdas aquí:")
    if st.button("🚀 Cargar"):
        df = pd.read_csv(io.StringIO(datos), sep='\t')
        guardar(df, dest)
        st.success("Sincronizado correctamente.")
                
