import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# --- CONFIGURACIÓN DE ALTA GAMA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: Diseño Minimalista de Lujo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #fcfcfd; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b; }
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border: 1px solid #f1f5f9; }
    .ia-card { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #38bdf8; }
    .stButton>button { background: #2563eb; color: white; border-radius: 12px; font-weight: 700; height: 3.5rem; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DATOS ---
DB_FILES = {
    "propietarios": "propietarios.csv",
    "mascotas": "mascotas.csv",
    "historias": "historias.csv"
}

def init_db():
    for key, path in DB_FILES.items():
        if not os.path.exists(path):
            if key == "propietarios":
                cols = ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"]
            elif key == "mascotas":
                cols = ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"]
            elif key == "historias":
                cols = ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P"]
            pd.DataFrame(columns=cols).to_csv(path, index=False)

init_db()

# --- MOTOR SENTIMIENTO IA ---
def sentimiento_ia_engine(s, o, p, paciente):
    analisis = []
    texto = (s + " " + o).lower()
    # Lógica para exóticos y comunes
    if any(x in texto for x in ["vómito", "diarrea"]): analisis.append("🩺 **SIA:** Evaluar hidratación. En exóticos, revisar temperatura ambiental.")
    if "huevo" in texto or "cloaca" in texto: analisis.append("🥚 **SIA Alerta:** Posible retención de huevo o distocia.")
    if any(x in texto for x in ["tos", "agitado"]): analisis.append("🫀 **SIA:** Evaluar disnea. Considerar estrés por manejo.")
    
    whatsapp = f"🐾 *REPORTE SENTIMIENTO ANIMAL*\n\nHola, hoy atendimos a *{paciente}*.\n\n🔍 *Hallazgos:* {o[:120]}...\n\n💊 *Plan Médico:* {p}\n\nDra. Camila Mejía."
    return analisis, whatsapp

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h1 style='color:white;'>Sentimiento Animal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#38bdf8;'>Asistente: <b>Sentimiento IA</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENÚ", ["💎 Dashboard", "👥 Clientes", "🐶 Registro Pacientes", "🩺 Consulta IA", "💾 Backup"])

# --- MODULO CLIENTES ---
if menu == "👥 Clientes":
    st.title("👥 Gestión de Propietarios")
    with st.form("form_cliente", clear_on_submit=True):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        nombre = st.text_input("Nombre Completo *")
        c1, c2 = st.columns(2)
        t_doc = c1.selectbox("Tipo de Documento", ["Cédula de Ciudadanía", "Cédula de Extranjería", "NIT", "Pasaporte"])
        n_doc = c2.text_input("Número de Documento *")
        c3, c4 = st.columns(2)
        tel = c3.text_input("Teléfono / WhatsApp")
        mail = c4.text_input("Correo Electrónico")
        dir = st.text_input("Dirección")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("Guardar Propietario"):
            if nombre and n_doc:
                df = pd.read_csv(DB_FILES["propietarios"])
                pd.concat([df, pd.DataFrame([{"Nombre": nombre, "Tipo_Doc": t_doc, "Numero": n_doc, "Teléfono": tel, "Correo": mail, "Dirección": dir}])]).to_csv(DB_FILES["propietarios"], index=False)
                st.success(f"✅ Propietario registrado.")

# --- MÓDULO PACIENTES (EXÓTICOS + CAMPOS DETALLADOS) ---
elif menu == "🐶 Registro Pacientes":
    st.title("🐶 Registro Detallado del Paciente")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    if not df_p.empty:
        sel_prop = st.selectbox("Asignar a Dueño:", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_prop = sel_prop.split("(")[-1].replace(")","")
        
        with st.form("form_mascota", clear_on_submit=True):
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            n_mascota = c1.text_input("Nombre del Paciente *")
            especie = c2.selectbox("Especie", ["Canino", "Felino", "Ave", "Reptil", "Roedor", "Conejo", "Equino", "Otro Exótico"])
            
            c3, c4 = st.columns(2)
            raza = c3.text_input("Raza / Variedad")
            sexo = c4.selectbox("Sexo", ["Macho", "Hembra", "Macho Castrado", "Hembra Esterilizada", "Desconocido (Exóticos)"])
            
            c5, c6, c7 = st.columns(3)
            color = c5.text_input("Color / Señas Especiales")
            peso = c6.number_input("Peso Actual (kg/g)", min_value=0.0, step=0.01, help="Usa 0.5 para 500g")
            f_nac = c7.date_input("Fecha de Nacimiento (Aprox)", value=date(2023, 1, 1))
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Registrar Paciente"):
                if n_mascota:
                    df_m = pd.read_csv(DB_FILES["mascotas"])
                    pd.concat([df_m, pd.DataFrame([{"ID_Prop":id_prop, "Nombre_Mascota":n_mascota, "Especie":especie, "Raza":raza, "Sexo": sexo, "Color": color, "Peso_kg": peso, "Nacimiento": f_nac}])]).to_csv(DB_FILES["mascotas"], index=False)
                    st.success(f"🐾 {n_mascota} registrado correctamente.")

# --- MÓDULO CONSULTA ---
elif menu == "🩺 Consulta IA":
    st.title("🩺 Estación de Trabajo Sentimiento IA")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    df_m = pd.read_csv(DB_FILES["mascotas"])
    
    if not df_m.empty:
        col_s1, col_s2 = st.columns(2)
        p_sel = col_s1.selectbox("Propietario", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        doc_id = p_sel.split("(")[-1].replace(")","")
        m_list = df_m[df_m["ID_Prop"].astype(str) == str(doc_id)]["Nombre_Mascota"].tolist()
        
        if m_list:
            m_act = col_s2.selectbox("Paciente", m_list)
            m_data = df_m[df_m["Nombre_Mascota"] == m_act].iloc[0]
            
            # Cálculo de edad simple
            edad = date.today().year - datetime.strptime(str(m_data['Nacimiento']), '%Y-%m-%d').year
            st.info(f"📋 **Ficha:** {m_data['Especie']} | {m_data['Raza']} | {m_data['Sexo']} | {m_data['Peso_kg']} kg | ~{edad} años")
            
            c_cl, c_ia = st.columns([2, 1])
            with c_cl:
                s = st.text_area("S: Subjetivo")
                o = st.text_area("O: Objetivo")
                i = st.text_area("I: Interpretación")
                p = st.text_area("P: Plan Terapéutico")
            with c_ia:
                st.markdown("#### 🤖 Sentimiento IA")
                alertas, ws = sentimiento_ia_engine(s, o, p, m_act)
                st.markdown(f"<div class='ia-card'>{ '<br>'.join(alertas) if alertas else 'Analizando datos...'}</div>", unsafe_allow_html=True)
                st.text_area("📱 WhatsApp:", ws, height=180)
            
            if st.button("💾 REGISTRAR CONSULTA"):
                pd.concat([pd.read_csv(DB_FILES["historias"]), pd.DataFrame([{"Fecha": date.today(), "ID_Prop": doc_id, "Mascota": m_act, "S": s, "O": o, "I": i, "P": p}])]).to_csv(DB_FILES["historias"], index=False)
                st.balloons()
                st.success("Historia guardada.")
    else:
        st.warning("Sin datos de pacientes.")

# --- DASHBOARD ---
elif menu == "💎 Dashboard":
    st.title("💎 Panel de Control")
    df_h = pd.read_csv(DB_FILES["historias"])
    st.metric("Consultas Totales", len(df_h))
    st.dataframe(df_h, use_container_width=True)

# --- BACKUP ---
elif menu == "💾 Backup":
    st.title("💾 Copia de Seguridad")
    st.download_button("Exportar Clientes", pd.read_csv(DB_FILES["propietarios"]).to_csv(index=False), "Clientes.csv")
    st.download_button("Exportar Pacientes", pd.read_csv(DB_FILES["mascotas"]).to_csv(index=False), "Mascotas.csv")
                        
