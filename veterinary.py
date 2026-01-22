import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, date

# Intentar importar librerías avanzadas sin bloquear el inicio
try:
    import plotly.express as px
    import xlsxwriter
except ImportError:
    st.error("Instalando componentes de alta gama... Por favor, espere 30 segundos y recargue la página.")

# --- CONFIGURACIÓN DE ALTA GAMA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: Diseño Minimalista de Lujo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b; }
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .ia-card { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #38bdf8; }
    .stButton>button { background: #2563eb; color: white; border-radius: 12px; font-weight: 700; height: 3.5rem; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DATOS ---
DB_FILES = {
    "propietarios": "propietarios.csv",
    "mascotas": "mascotas.csv",
    "historias": "historias.csv",
    "alertas": "alertas.csv"
}

def init_db():
    for key, path in DB_FILES.items():
        if not os.path.exists(path):
            cols = ["Documento", "Nombre", "Teléfono", "Correo", "Dirección"] if key == "propietarios" else \
                   ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Nacimiento"] if key == "mascotas" else \
                   ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P"] if key == "historias" else \
                   ["Fecha_Cita", "Mascota", "Motivo", "Propietario"]
            pd.DataFrame(columns=cols).to_csv(path, index=False)

init_db()

# --- MOTOR SENTIMIENTO IA ---
def sentimiento_ia_engine(s, o, p, paciente):
    analisis = []
    texto = (s + " " + o).lower()
    if any(x in texto for x in ["vómito", "diarrea"]): analisis.append("🩺 **SIA:** Evaluar hidratación y parásitos.")
    if any(x in texto for x in ["tos", "agitado"]): analisis.append("🫀 **SIA:** Posible soplos o compromiso pulmonar.")
    
    whatsapp = f"🐾 *REPORTE SENTIMIENTO ANIMAL*\n\nHola, atendimos a *{paciente}*.\n\n🔍 *Examen:* {o[:100]}...\n\n💊 *Plan:* {p}\n\nDra. Camila Mejía."
    return analisis, whatsapp

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h1 style='color:white;'>Sentimiento Animal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#38bdf8;'>Powered by <b>Sentimiento IA</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("SISTEMA", ["💎 Dashboard", "👥 Clientes", "🐶 Mascotas", "🩺 Consulta IA", "💾 Backup"])

# --- DASHBOARD ---
if menu == "💎 Dashboard":
    st.title("💎 Panel Elite")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    df_m = pd.read_csv(DB_FILES["mascotas"])
    df_h = pd.read_csv(DB_FILES["historias"])
    df_a = pd.read_csv(DB_FILES["alertas"])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clientes", len(df_p))
    c2.metric("Pacientes", len(df_m))
    c3.metric("Historias", len(df_h))
    
    hoy = str(date.today())
    alertas_hoy = df_a[df_a['Fecha_Cita'] == hoy]
    c4.metric("Alertas Hoy", len(alertas_hoy))
    
    st.markdown("### 🔍 Buscador de Historias")
    bus = st.text_input("Nombre de mascota...")
    if bus:
        st.dataframe(df_h[df_h['Mascota'].str.contains(bus, case=False, na=False)], use_container_width=True)

# --- CONSULTA ---
elif menu == "🩺 Consulta IA":
    st.title("🩺 Estación Sentimiento IA")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    df_m = pd.read_csv(DB_FILES["mascotas"])
    
    if not df_m.empty:
        col_s1, col_s2 = st.columns(2)
        prop_label = col_s1.selectbox("Dueño", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
        doc_id = prop_label.split("(")[-1].replace(")","")
        masc_sel = col_s2.selectbox("Mascota", df_m[df_m["ID_Prop"].astype(str) == str(doc_id)]["Nombre_Mascota"])
        
        c_f, c_ia = st.columns([2, 1])
        with c_f:
            s = st.text_area("S: Subjetivo")
            o = st.text_area("O: Objetivo")
            i = st.text_area("I: Interpretación")
            p = st.text_area("P: Plan")
        
        with c_ia:
            st.markdown("#### 🤖 Sentimiento IA")
            analisis, ws = sentimiento_ia_engine(s, o, p, masc_sel)
            st.markdown(f"<div class='ia-card'>{'<br>'.join(analisis) if analisis else 'Analizando...'}</div>", unsafe_allow_html=True)
            st.text_area("📱 WhatsApp:", ws, height=150)
            f_cita = st.date_input("Próximo Refuerzo", min_value=date.today())
            mot = st.text_input("Motivo Cita")

        if st.button("💾 FINALIZAR"):
            pd.concat([pd.read_csv(DB_FILES["historias"]), pd.DataFrame([{"Fecha": date.today(), "ID_Prop": doc_id, "Mascota": masc_sel, "S": s, "O": o, "I": i, "P": p}])]).to_csv(DB_FILES["historias"], index=False)
            pd.concat([pd.read_csv(DB_FILES["alertas"]), pd.DataFrame([{"Fecha_Cita": str(f_cita), "Mascota": masc_sel, "Motivo": mot, "Propietario": prop_label}])]).to_csv(DB_FILES["alertas"], index=False)
            st.success("Guardado exitosamente.")
    else:
        st.warning("Registre clientes y mascotas primero.")

# --- MÓDULOS REGISTRO ---
elif menu == "👥 Clientes":
    st.subheader("Nuevo Cliente")
    with st.form("fc"):
        d, n = st.text_input("Cédula"), st.text_input("Nombre")
        if st.form_submit_button("Guardar"):
            pd.concat([pd.read_csv(DB_FILES["propietarios"]), pd.DataFrame([{"Documento":d,"Nombre":n}])]).to_csv(DB_FILES["propietarios"], index=False)
            st.success("Ok")

elif menu == "🐶 Mascotas":
    st.subheader("Nueva Mascota")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    sel = st.selectbox("Dueño", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
    with st.form("fm"):
        nom = st.text_input("Nombre Mascota")
        if st.form_submit_button("Vincular"):
            pd.concat([pd.read_csv(DB_FILES["mascotas"]), pd.DataFrame([{"ID_Prop":sel.split("(")[-1].replace(")",""),"Nombre_Mascota":nom}])]).to_csv(DB_FILES["mascotas"], index=False)
            st.success("Ok")

# --- BACKUP ---
elif menu == "💾 Backup":
    st.title("💾 Respaldo")
    # Generación simple de CSV para evitar errores de librerías mientras cargan
    st.download_button("Descargar Historias (CSV)", pd.read_csv(DB_FILES["historias"]).to_csv(index=False), "Historias.csv")
    
