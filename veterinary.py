import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# --- CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: ESTÉTICA CIELO (Celeste claro, letras negras, logo circular)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background-color: #f0f9ff; 
        color: #000000 !important;
    }

    /* Barra Lateral Celeste Pastel */
    [data-testid="stSidebar"] {
        background-color: #bae6fd !important;
        border-right: 1px solid #7dd3fc;
    }

    /* Logo Circular */
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Textos en negro absoluto para lectura perfecta */
    p, span, label, h1, h2, h3, .stMarkdown {
        color: #000000 !important;
    }

    /* Tarjetas de registro blancas */
    .main-card { 
        background: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
        margin-bottom: 15px;
        border: 1px solid #e0f2fe;
    }

    /* Caja de Sentimiento IA */
    .ia-card { 
        background: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 10px solid #0ea5e9; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        color: #000000;
    }

    /* Botones principales en Azul Clínico */
    .stButton>button {
        background: #0284c7;
        color: white !important;
        border-radius: 10px;
        font-weight: 700;
        height: 3rem;
        border: none;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #0369a1;
        border: none;
    }
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
            if key == "propietarios": cols = ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"]
            elif key == "mascotas": cols = ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"]
            elif key == "historias": cols = ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P"]
            elif key == "alertas": cols = ["Fecha_Cita", "Paciente", "Motivo", "Propietario"]
            pd.DataFrame(columns=cols).to_csv(path, index=False)
init_db()

# --- NAVEGACIÓN ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    st.markdown("<h2 style='text-align:center;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes", "🐾 Mascotas", "🩺 Consulta IA", "💾 Backup"])

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_h = pd.read_csv(DB_FILES["historias"])
    df_a = pd.read_csv(DB_FILES["alertas"])
    
    col1, col2 = st.columns(2)
    col1.metric("Consultas Totales", len(df_h))
    
    st.subheader("📅 Próximas Citas y Recordatorios")
    if not df_a.empty:
        # Filtrar solo citas futuras o de hoy
        df_a['Fecha_Cita'] = pd.to_datetime(df_a['Fecha_Cita'])
        hoy = pd.to_datetime(date.today())
        pendientes = df_a[df_a['Fecha_Cita'] >= hoy].sort_values(by='Fecha_Cita')
        st.table(pendientes)
    else:
        st.write("No hay citas programadas.")

# --- CLIENTES ---
elif menu == "👥 Clientes":
    st.title("👥 Registro de Clientes")
    with st.form("f_cliente", clear_on_submit=True):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        nombre = st.text_input("Nombre Completo")
        c1, c2 = st.columns(2)
        t_doc = c1.selectbox("Tipo Doc", ["Cédula", "Pasaporte", "NIT"])
        n_doc = c2.text_input("Número de Documento")
        tel = st.text_input("Teléfono / WhatsApp")
        cor = st.text_input("Correo")
        dir = st.text_input("Dirección")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("Guardar Propietario"):
            df = pd.read_csv(DB_FILES["propietarios"])
            pd.concat([df, pd.DataFrame([{"Nombre":nombre,"Tipo_Doc":t_doc,"Numero":n_doc,"Teléfono":tel,"Correo":cor,"Dirección":dir}])]).to_csv(DB_FILES["propietarios"], index=False)
            st.success("Cliente registrado con éxito.")

# --- MASCOTAS ---
elif menu == "🐾 Mascotas":
    st.title("🐾 Registro de Pacientes")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    if not df_p.empty:
        dueño = st.selectbox("Asignar a:", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_dueño = dueño.split("(")[-1].replace(")","")
        with st.form("f_mascota", clear_on_submit=True):
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            nom = st.text_input("Nombre Mascota")
            esp = st.selectbox("Especie", ["Canino", "Felino", "Ave", "Reptil", "Exótico"])
            raz = st.text_input("Raza")
            sex = st.selectbox("Sexo", ["Macho", "Hembra", "M. Castrado", "H. Esterilizada"])
            pes = st.number_input("Peso (kg)", step=0.01)
            nac = st.date_input("Fecha Nacimiento (Aprox)")
            st.markdown("</div>", unsafe_allow_html=True)
            if st.form_submit_button("Vincular Mascota"):
                df_m = pd.read_csv(DB_FILES["mascotas"])
                pd.concat([df_m, pd.DataFrame([{"ID_Prop":id_dueño,"Nombre_Mascota":nom,"Especie":esp,"Raza":raz,"Sexo":sex,"Peso_kg":pes,"Nacimiento":nac}])]).to_csv(DB_FILES["mascotas"], index=False)
                st.success("Paciente registrado.")
    else:
        st.warning("Registre un cliente primero.")

# --- CONSULTA IA CON AGENDAMIENTO ---
elif menu == "🩺 Consulta IA":
    st.title("🩺 Estación Sentimiento IA")
    df_p = pd.read_csv(DB_FILES["propietarios"])
    df_m = pd.read_csv(DB_FILES["mascotas"])
    
    if not df_m.empty:
        c1, c2 = st.columns(2)
        prop = c1.selectbox("Dueño", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_p = prop.split("(")[-1].replace(")","")
        mascotas = df_m[df_m["ID_Prop"].astype(str) == str(id_p)]["Nombre_Mascota"].tolist()
        
        if mascotas:
            paciente = c2.selectbox("Paciente", mascotas)
            m_info = df_m[df_m["Nombre_Mascota"] == paciente].iloc[0]
            st.write(f"📌 **Ficha:** {m_info['Especie']} | {m_info['Sexo']} | {m_info['Peso_kg']}kg")
            
            with st.container():
                s = st.text_area("Subjetivo")
                o = st.text_area("Objetivo")
                i = st.text_area("Interpretación")
                p = st.text_area("Plan")
                
            st.markdown("### 🤖 Análisis de Sentimiento IA")
            st.markdown(f"<div class='ia-card'><b>Sugerencia:</b> Monitorear evolución y seguir el plan médico al pie de la letra.</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📅 Próxima Cita / Recordatorio")
            col_f, col_m = st.columns(2)
            fecha_prox = col_f.date_input("Fecha de re-control", value=date.today())
            motivo_prox = col_m.text_input("Motivo del recordatorio", placeholder="Ej: Refuerzo vacuna / Control exóticos")

            if st.button("💾 GUARDAR CONSULTA Y AGENDAR"):
                # Guardar Historia
                df_h = pd.read_csv(DB_FILES["historias"])
                pd.concat([df_h, pd.DataFrame([{"Fecha":date.today(),"ID_Prop":id_p,"Mascota":paciente,"S":s,"O":o,"I":i,"P":p}])]).to_csv(DB_FILES["historias"], index=False)
                # Guardar Alerta
                df_a = pd.read_csv(DB_FILES["alertas"])
                pd.concat([df_a, pd.DataFrame([{"Fecha_Cita":str(fecha_prox),"Paciente":paciente,"Motivo":motivo_prox,"Propietario":prop}])]).to_csv(DB_FILES["alertas"], index=False)
                st.balloons()
                st.success("¡Consulta guardada y cita agendada!")
        else:
            st.error("Este dueño no tiene mascotas.")

# --- BACKUP ---
elif menu == "💾 Backup":
    st.title("💾 Respaldo de Datos")
    st.download_button("Descargar Historias Clínicas", pd.read_csv(DB_FILES["historias"]).to_csv(index=False), "Historias.csv")
    st.download_button("Descargar Base de Clientes", pd.read_csv(DB_FILES["propietarios"]).to_csv(index=False), "Clientes.csv")
            
