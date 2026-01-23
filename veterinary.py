import streamlit as st
import pandas as pd
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURACIÓN E IDENTIDAD VISUAL ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🏥</h1>", unsafe_allow_html=True)
    st.title("Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    tema = st.toggle("🌙 Modo Noche Profesional", value=False)
    st.divider()

# Colores dinámicos
if tema:
    bg, card, txt, border = "#0f172a", "#1e293b", "#f1f5f9", "#334155"
else:
    bg, card, txt, border = "#f8fafc", "#ffffff", "#0f172a", "#cbd5e1"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; }}
    [data-testid="stSidebar"] {{ background-color: #0c4a6e !important; }}
    .main-card {{
        background: {card}; padding: 25px; border-radius: 20px;
        border: 1px solid {border}; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        color: {txt}; margin-bottom: 20px;
    }}
    .status-red {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 12px; border-left: 6px solid #ef4444; margin-bottom: 10px; }}
    .kardex-row {{ background: #f1f5f9; padding: 15px; border-radius: 12px; border-left: 6px solid #0ea5e9; margin-bottom: 10px; color: #0f172a; }}
    .stButton>button {{
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important; border-radius: 12px; font-weight: bold; border: none; height: 3.5em; width: 100%;
    }}
    .whatsapp-btn {{ background-color: #25d366; color: white !important; padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS MULTICAPA ---
def init_db():
    tablas = {
        "clientes.csv": ["Documento", "Nombre", "WhatsApp", "Correo"],
        "pacientes.csv": ["ID", "Mascota", "Especie", "Raza", "Dueño_Doc"],
        "clinica.csv": ["Fecha", "Mascota", "Peso", "SOIP", "Tipo"],
        "ventas.csv": ["ID", "Fecha", "Mascota", "Total", "Metodo"],
        "hospital.csv": ["Mascota", "Cama", "Medicamento", "Frecuencia", "Recomendaciones"]
    }
    for file, cols in tablas.items():
        if not os.path.exists(file) or os.stat(file).st_size == 0:
            pd.DataFrame(columns=cols).to_csv(file, index=False)

init_db()
def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. NAVEGACIÓN ---
menu = st.sidebar.radio("SISTEMA MAESTRO", [
    "📊 Dashboard & Fidelización",
    "👥 Registro de Pacientes",
    "🩺 Historia Clínica SOIP",
    "🏥 Hospitalización & UCI",
    "💰 Caja & Facturación",
    "📥 Carga Masiva (OkVet)"
])

# --- 4. DASHBOARD & SEMÁFORO DE SALUD ---
if menu == "📊 Dashboard & Fidelización":
    st.title("📊 Inteligencia de Negocios")
    df_p, df_h, df_v, df_c = leer("pacientes.csv"), leer("clinica.csv"), leer("ventas.csv"), leer("clientes.csv")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos Totales", f"${df_v['Total'].sum():,.0f}")
    c2.metric("Pacientes Activos", len(df_p))
    c3.metric("Estatus Clínica", "Elite #1")

    col_g1, col_g2 = st.columns([2, 1])
    with col_g1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("🚩 Radar de Pacientes Inactivos (> 6 meses)")
        if not df_h.empty:
            df_h['Fecha'] = pd.to_datetime(df_h['Fecha'])
            ultimo = df_h.groupby('Mascota')['Fecha'].max().reset_index()
            limite = datetime.now() - timedelta(days=180)
            inactivos = ultimo[ultimo['Fecha'] < limite]
            if not inactivos.empty:
                for _, row in inactivos.iterrows():
                    info_p = df_p[df_p['Mascota'] == row['Mascota']]
                    if not info_p.empty:
                        doc = info_p['Dueño_Doc'].values[0]
                        info_c = df_c[df_c['Documento'] == doc]
                        if not info_c.empty:
                            tutor, tel = info_c['Nombre'].values[0], info_c['WhatsApp'].values[0]
                            st.markdown(f"<div class='status-red'><b>{row['Mascota']}</b> (Tutor: {tutor}) • Sin visita desde {row['Fecha'].strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)
                            msg = f"Hola {tutor}, te extrañamos en Sentimiento Animal. Hace tiempo no vemos a {row['Mascota']}. ¿Agendamos?"
                            st.markdown(f'<a href="https://wa.me/{tel}?text={urllib.parse.quote(msg)}" target="_blank" class="whatsapp-btn">📲 Enviar WhatsApp</a>', unsafe_allow_html=True)
            else: st.success("¡Todos tus pacientes están al día!")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_g2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("🐕 Especialidad por Raza")
        if not df_p.empty: st.bar_chart(df_p['Raza'].value_counts().head(5), color="#0ea5e9")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. REGISTRO ---
elif menu == "👥 Registro de Pacientes":
    st.title("👥 Gestión de Directorio")
    t1, t2 = st.tabs(["👤 Registro Propietario", "🐾 Registro Mascota"])
    with t1:
        with st.form("f_c"):
            doc, nom, wa, cor = st.text_input("Cédula/NIT"), st.text_input("Nombre Completo"), st.text_input("WhatsApp"), st.text_input("Correo")
            if st.form_submit_button("Guardar"):
                df = leer("clientes.csv")
                guardar(pd.concat([df, pd.DataFrame([[doc, nom, wa, cor]], columns=df.columns)]), "clientes.csv")
                st.success("Guardado.")
    with t2:
        df_c = leer("clientes.csv")
        with st.form("f_m"):
            m_nom, m_raz = st.text_input("Nombre Mascota"), st.text_input("Raza")
            m_due = st.selectbox("Asignar Dueño (Doc)", df_c["Documento"].tolist() if not df_c.empty else [])
            if st.form_submit_button("Vincular"):
                df = leer("pacientes.csv")
                guardar(pd.concat([df, pd.DataFrame([[len(df)+1, m_nom, "Canino", m_raz, m_due]], columns=df.columns)]), "pacientes.csv")
                st.success("Registrada.")

# --- 6. CONSULTA ---
elif menu == "🩺 Historia Clínica SOIP":
    st.title("🩺 Estación de Consulta")
    df_p = leer("pacientes.csv")
    pac = st.selectbox("Paciente:", df_p["Mascota"].tolist() if not df_p.empty else ["Sin Datos"])
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    peso = st.number_input("Peso (Kg)", step=0.1)
    soip = st.text_area("SOIP (Subjetivo, Objetivo, Interpretación, Plan):", height=300)
    if st.button("💾 Guardar Historia"):
        df = leer("clinica.csv")
        guardar(pd.concat([df, pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), pac, peso, soip, "Presencial"]], columns=df.columns)]), "clinica.csv")
        st.success("Historia Clínica Guardada.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. HOSPITALIZACIÓN ---
elif menu == "🏥 Hospitalización y UCI":
    st.title("🏥 Kardex y Altas")
    df_h, df_p = leer("hospital.csv"), leer("pacientes.csv")
    col_k, col_a = st.columns([1.5, 1])
    with col_k:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("📋 UCI Activa")
        for i, r in df_h.iterrows():
            st.markdown(f"<div class='kardex-row'><b>🐾 {r['Mascota']}</b> (Cama {r['Cama']})<br>💉 {r['Medicamento']}</div>", unsafe_allow_html=True)
            if st.button(f"🚩 Dar Alta {r['Mascota']}"):
                st.session_state['alta_rec'] = r.to_dict(); df_h = df_h.drop(i); guardar(df_h, "hospital.csv"); st.rerun()
        with st.expander("➕ Nuevo Ingreso"):
            with st.form("f_h"):
                p, c, m, rec = st.selectbox("Mascota", df_p["Mascota"].tolist()), st.text_input("Cama"), st.text_input("Medicación"), st.text_area("Recomendaciones Casa")
                if st.form_submit_button("Confirmar"):
                    guardar(pd.concat([df_h, pd.DataFrame([[p, c, m, "Cada 12h", rec]], columns=df_h.columns)]), "hospital.csv"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_a:
        if 'alta_rec' in st.session_state:
            st.markdown(f"<div class='main-card' style='border: 2px solid green;'><h3>ORDEN DE ALTA</h3><b>Paciente:</b> {st.session_state['alta_rec']['Mascota']}<br><b>Cuidado en casa:</b> {st.session_state['alta_rec']['Recomendaciones']}</div>", unsafe_allow_html=True)

# --- 8. CAJA ---
elif menu == "💰 Caja & Facturación":
    st.title("💰 Terminal de Venta")
    df_p = leer("pacientes.csv")
    p_f = st.selectbox("Facturar a:", df_p["Mascota"].tolist() if not df_p.empty else ["Sin Datos"])
    monto = st.number_input("Valor ($)", min_value=0)
    if st.button("💳 Generar Factura"):
        df_v = leer("ventas.csv")
        guardar(pd.concat([df_v, pd.DataFrame([[len(df_v)+1, datetime.now().strftime("%Y-%m-%d"), p_f, monto, "Digital"]], columns=df_v.columns)]), "ventas.csv")
        st.balloons(); st.success("Pago Procesado.")

# --- 9. CARGA MASIVA ---
elif menu == "📥 Carga Masiva (OkVet)":
    st.title("📥 Sincronización")
    raw = st.text_area("Pegue columnas de Excel:")
    if st.button("🚀 Cargar Datos"):
        try:
            df_new = pd.read_csv(io.StringIO(raw), sep='\t')
            guardar(df_new, "pacientes.csv")
            st.success("Base de datos actualizada.")
        except: st.error("Formato inválido.")
                          
