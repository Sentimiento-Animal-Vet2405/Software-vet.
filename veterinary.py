import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, date
import xlsxwriter

# --- CONFIGURACIÓN DE ALTA GAMA ---
st.set_page_config(page_title="Sentimiento Animal | Elite System", layout="wide", page_icon="🐾")

# CSS: Diseño Neumórfico y Minimalismo Médico
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }
    
    /* Barra Lateral de Lujo */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Tarjetas de Información (Cards) */
    .stBlock, div[data-testid="stVerticalBlock"] > div {
        background-color: white;
        border-radius: 20px;
        padding: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Sentimiento IA Card */
    .ia-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border-left: 8px solid #38bdf8;
    }
    
    /* Botones de Acción */
    .stButton>button {
        background: #2563eb;
        color: white;
        border-radius: 12px;
        font-weight: 700;
        height: 3.5rem;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BASES DE DATOS ---
DB_FILES = {
    "propietarios": "propietarios.csv",
    "mascotas": "mascotas.csv",
    "historias": "historias.csv",
    "alertas": "alertas.csv"
}

def init_db():
    for key, path in DB_FILES.items():
        if not os.path.exists(path):
            if key == "propietarios": cols = ["Documento", "Nombre", "Teléfono", "Correo", "Dirección"]
            elif key == "mascotas": cols = ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Nacimiento"]
            elif key == "historias": cols = ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P"]
            elif key == "alertas": cols = ["Fecha_Cita", "Mascota", "Motivo", "Propietario"]
            pd.DataFrame(columns=cols).to_csv(path, index=False)

init_db()

# --- MOTOR DE SENTIMIENTO IA ---
def sentimiento_ia_engine(s, o, p, paciente):
    # Análisis clínico inteligente
    analisis = []
    texto = (s + " " + o).lower()
    if "vómito" in texto or "diarrea" in texto: 
        analisis.append("🩺 **SIA Alerta:** Sugiere descartar parásitos o sensibilidad alimentaria. Hidratación clave.")
    if "tos" in texto or "agitado" in texto:
        analisis.append("🫀 **SIA Alerta:** Posible compromiso cardiopulmonar. Auscultar soplos.")
    
    # Reporte para WhatsApp
    whatsapp = f"🐾 *REPORTE SENTIMIENTO ANIMAL*\n\nHola, hoy atendimos a *{paciente}*.\n\n"
    whatsapp += f"🔍 *Examen:* {o[:120]}...\n\n💊 *Plan Médico:* {p}\n\nCon cariño, Dra. Camila Mejía."
    return analisis, whatsapp

# --- INTERFAZ DE NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h1 style='color:white;'>Sentimiento Animal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#38bdf8;'>Powered by <b>Sentimiento IA</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("SISTEMA CENTRAL", ["💎 Dashboard", "👥 Gestión Propietarios", "🐶 Registro Mascotas", "🩺 Consulta Inteligente", "💾 Backup Elite"])

# --- DASHBOARD ---
if menu == "💎 Dashboard":
    st.title("💎 Panel de Control Elite")
    df_p, df_m, df_h, df_a = pd.read_csv(DB_FILES["propietarios"]), pd.read_csv(DB_FILES["mascotas"]), pd.read_csv(DB_FILES["historias"]), pd.read_csv(DB_FILES["alertas"])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clientes", len(df_p))
    c2.metric("Pacientes", len(df_m))
    c3.metric("Consultas", len(df_h))
    c4.metric("Alertas Hoy", len(df_a[df_a['Fecha_Cita'] == str(date.today())]))

    st.markdown("### 🔍 Buscador Maestro de Historias")
    bus = st.text_input("Escribe nombre de la mascota o dueño...", placeholder="Ej: Bruno")
    if bus:
        res = df_h[df_h['Mascota'].str.contains(bus, case=False, na=False)]
        st.dataframe(res, use_container_width=True)

# --- CONSULTA INTELIGENTE ---
elif menu == "🩺 Consulta Inteligente":
    st.title("🩺 Estación Médica Sentimiento IA")
    df_p, df_m = pd.read_csv(DB_FILES["propietarios"]), pd.read_csv(DB_FILES["mascotas"])
    
    if not df_m.empty:
        col_sel1, col_sel2 = st.columns(2)
        prop_label = col_sel1.selectbox("Propietario", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
        doc_id = prop_label.split("(")[-1].replace(")","")
        pacs_list = df_m[df_m["ID_Prop"].astype(str) == str(doc_id)]["Nombre_Mascota"].tolist()
        masc_sel = col_sel2.selectbox("Mascota", pacs_list)
        
        col_form, col_ia = st.columns([2, 1])
        
        with col_form:
            st.markdown("#### 📝 Registro Clínico (SOIP)")
            s = st.text_area("S: Subjetivo")
            o = st.text_area("O: Objetivo")
            i = st.text_area("I: Interpretación")
            p = st.text_area("P: Plan Terapéutico")
        
        with col_ia:
            st.markdown("#### 🤖 Sentimiento IA")
            analisis, ws_msg = sentimiento_ia_engine(s, o, p, masc_sel)
            st.markdown(f"<div class='ia-card'><b>IA Analizando...</b><br><br>{'<br>'.join(analisis) if analisis else 'Esperando datos clínicos...'}</div>", unsafe_allow_html=True)
            
            st.markdown("#### 📱 Reporte WhatsApp")
            st.text_area("Copia y pega:", ws_msg, height=150)
            
            st.markdown("#### 📅 Agendar Refuerzo")
            f_cita = st.date_input("Próxima cita", min_value=date.today())
            motivo = st.text_input("Motivo")

        if st.button("💾 FINALIZAR Y GUARDAR TODO"):
            # Guardar Historia
            nueva_h = {"Fecha": date.today(), "ID_Prop": doc_id, "Mascota": masc_sel, "S": s, "O": o, "I": i, "P": p}
            pd.concat([pd.read_csv(DB_FILES["historias"]), pd.DataFrame([nueva_h])]).to_csv(DB_FILES["historias"], index=False)
            # Guardar Alerta
            nueva_a = {"Fecha_Cita": str(f_cita), "Mascota": masc_sel, "Motivo": motivo, "Propietario": prop_label}
            pd.concat([pd.read_csv(DB_FILES["alertas"]), pd.DataFrame([nueva_a])]).to_csv(DB_FILES["alertas"], index=False)
            st.balloons()
            st.success("✅ Paciente atendido y recordatorio programado.")
    else:
        st.warning("Debe registrar clientes y mascotas primero.")

# --- MÓDULOS DE REGISTRO (Clientes y Mascotas) ---
elif menu == "👥 Gestión Propietarios":
    st.title("👥 Base de Clientes")
    with st.form("f_p", clear_on_submit=True):
        col1, col2 = st.columns(2)
        d = col1.text_input("Documento/Cédula *")
        n = col2.text_input("Nombre Completo *")
        t = col1.text_input("Teléfono")
        c = col2.text_input("Email")
        dir = st.text_input("Dirección")
        if st.form_submit_button("Guardar Propietario"):
            df = pd.read_csv(DB_FILES["propietarios"])
            pd.concat([df, pd.DataFrame([{"Documento":d,"Nombre":n,"Teléfono":t,"Correo":c,"Dirección":dir}])]).to_csv(DB_FILES["propietarios"], index=False)
            st.success("Guardado.")

elif menu == "🐶 Registro Mascotas":
    st.title("🐶 Registro de Pacientes")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    if not df_p.empty:
        sel = st.selectbox("Seleccionar Dueño", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
        id_p = sel.split("(")[-1].replace(")","")
        with st.form("f_m", clear_on_submit=True):
            nom = st.text_input("Nombre de la Mascota")
            esp = st.selectbox("Especie", ["Canino", "Felino", "Otro"])
            raz = st.text_input("Raza")
            if st.form_submit_button("Registrar Mascota"):
                df = pd.read_csv(DB_FILES["mascotas"])
                pd.concat([df, pd.DataFrame([{"ID_Prop":id_p,"Nombre_Mascota":nom,"Especie":esp,"Raza":raz}])]).to_csv(DB_FILES["mascotas"], index=False)
                st.success("Mascota vinculada.")

# --- BACKUP ---
elif menu == "💾 Backup Elite":
    st.title("💾 Respaldo y Seguridad")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        for key, path in DB_FILES.items():
            pd.read_csv(path).to_excel(writer, sheet_name=key.capitalize(), index=False)
    st.download_button("📥 DESCARGAR BASE DE DATOS COMPLETA (EXCEL)", buffer.getvalue(), f"SentimientoAnimal_Backup_{date.today()}.xlsx")
