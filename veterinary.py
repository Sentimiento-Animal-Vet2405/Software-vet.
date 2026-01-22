import streamlit as st
import pandas as pd
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURACIÓN DE LUJO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    .main-card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px; color: #0f172a; }
    .kardex-row { background: #f1f5f9; padding: 15px; border-radius: 12px; border-left: 6px solid #0ea5e9; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important; color: white !important; border-radius: 12px; font-weight: bold; border: none; height: 3.5em; }
    .alta-box { background: #f0fdf4; border: 2px dashed #16a34a; padding: 20px; border-radius: 15px; color: #166534; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS MULTI-MÓDULO ---
def init_db():
    tablas = {
        "clientes.csv": ["Documento", "Nombre", "WhatsApp", "Correo"],
        "pacientes.csv": ["ID", "Mascota", "Especie", "Raza", "Dueño_Doc"],
        "clinica.csv": ["Fecha", "Mascota", "Peso", "SOIP", "Tipo"],
        "ventas.csv": ["ID", "Fecha", "Mascota", "Total", "Metodo"],
        "hospital.csv": ["Mascota", "Cama", "Medicamento", "Frecuencia", "Hora_Inicio"]
    }
    for file, cols in tablas.items():
        if not os.path.exists(file) or os.stat(file).st_size == 0:
            pd.DataFrame(columns=cols).to_csv(file, index=False)

init_db()
def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. MENÚ LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; color: #bae6fd;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SISTEMA MAESTRO", [
        "📊 Dashboard e IA",
        "👥 Registro Clientes/Pacientes",
        "🩺 Consulta Médica SOIP",
        "🏥 Hospitalización y Altas",
        "💰 Caja y Pagos",
        "📥 Importación OkVet"
    ])

# --- 4. DASHBOARD E INTELIGENCIA ---
if menu == "📊 Dashboard e IA":
    st.title("📊 Inteligencia de Negocios")
    df_v = leer("ventas.csv")
    df_p = leer("pacientes.csv")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos Totales", f"${df_v['Total'].sum():,.0f}")
    c2.metric("Pacientes Activos", len(df_p))
    c3.metric("Reporte Semanal", "Programado Dom 8am")
    
    if not df_v.empty:
        st.area_chart(df_v.groupby("Fecha")["Total"].sum(), color="#0ea5e9")

# --- 5. REGISTRO ---
elif menu == "👥 Registro Clientes/Pacientes":
    st.title("👥 Gestión de Base de Datos")
    t1, t2 = st.tabs(["👤 Nuevo Propietario", "🐾 Nueva Mascota"])
    with t1:
        with st.form("f_prop"):
            doc, nom, wa = st.text_input("Cédula"), st.text_input("Nombre"), st.text_input("WhatsApp")
            if st.form_submit_button("Guardar"):
                df = leer("clientes.csv")
                guardar(pd.concat([df, pd.DataFrame([[doc, nom, wa, ""]], columns=df.columns)]), "clientes.csv")
                st.success("Cliente Creado.")
    with t2:
        df_c = leer("clientes.csv")
        with st.form("f_masc"):
            m_nom, m_raz = st.text_input("Mascota"), st.text_input("Raza")
            m_due = st.selectbox("Dueño", df_c["Documento"].tolist() if not df_c.empty else ["Cree un dueño primero"])
            if st.form_submit_button("Registrar"):
                df = leer("pacientes.csv")
                guardar(pd.concat([df, pd.DataFrame([[len(df)+1, m_nom, "Canino", m_raz, m_due]], columns=df.columns)]), "pacientes.csv")
                st.success("Mascota Registrada.")

# --- 6. CONSULTA ---
elif menu == "🩺 Consulta Médica SOIP":
    st.title("🩺 Estación Clínica")
    df_p = leer("pacientes.csv")
    pac = st.selectbox("Paciente:", df_p["Mascota"].tolist() if not df_p.empty else ["Sin Datos"])
    soip = st.text_area("Notas Médicas:", height=250)
    if st.button("💾 Guardar Historia"):
        df = leer("clinica.csv")
        guardar(pd.concat([df, pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), pac, 0, soip, "Presencial"]], columns=df.columns)]), "clinica.csv")
        st.success("Historia Blindada.")

# --- 7. HOSPITALIZACIÓN Y ALTAS (NUEVO) ---
elif menu == "🏥 Hospitalización y Altas":
    st.title("🏥 Control de Críticos y Altas Médicas")
    df_h = leer("hospital.csv")
    df_p = leer("pacientes.csv")
    
    col_k, col_a = st.columns([1.5, 1])
    
    with col_k:
        st.subheader("📋 Kardex de Hospitalización")
        if not df_h.empty:
            for i, r in df_h.iterrows():
                st.markdown(f"""<div class='kardex-row'><b>🐾 {r['Mascota']}</b> (Cama {r['Cama']})<br>💉 {r['Medicamento']} - {r['Frecuencia']}</div>""", unsafe_allow_html=True)
                if st.button(f"🚩 Dar de Alta: {r['Mascota']}"):
                    st.session_state['alta'] = r.to_dict()
                    df_h = df_h.drop(i)
                    guardar(df_h, "hospital.csv")
                    st.rerun()
        else: st.info("UCI Vacía.")
        
        with st.expander("➕ Ingresar Paciente"):
            with st.form("ing_h"):
                p, c, m, f = st.selectbox("Paciente", df_p["Mascota"].tolist()), st.text_input("Cama"), st.text_input("Medicamento"), st.selectbox("Frec", ["8h", "12h", "24h"])
                if st.form_submit_button("Ingresar"):
                    guardar(pd.concat([df_h, pd.DataFrame([[p, c, m, f, ""]], columns=df_h.columns)]), "hospital.csv")
                    st.rerun()

    with col_a:
        st.subheader("📄 Orden de Salida")
        if 'alta' in st.session_state:
            a = st.session_state['alta']
            st.markdown(f"""
            <div class='alta-box'>
                <h3>ORDEN DE ALTA</h3>
                <b>PACIENTE:</b> {a['Mascota']}<br>
                <b>TRATAMIENTO RECIBIDO:</b> {a['Medicamento']}<br>
                <b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}<br><br>
                <i>Firma: Dra. Camila Mejía</i>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Limpiar Pantalla de Alta"):
                del st.session_state['alta']
                st.rerun()

# --- 8. CAJA ---
elif menu == "💰 Caja y Pagos":
    st.title("💰 Facturación")
    df_p = leer("pacientes.csv")
    p_f = st.selectbox("Cobrar a:", df_p["Mascota"].tolist() if not df_p.empty else ["Sin Datos"])
    monto = st.number_input("Total ($)", min_value=0)
    if st.button("✅ Procesar Pago"):
        df_v = leer("ventas.csv")
        guardar(pd.concat([df_v, pd.DataFrame([[len(df_v)+1, datetime.now().strftime("%Y-%m-%d"), p_f, monto, "Efectivo"]], columns=df_v.columns)]), "ventas.csv")
        st.balloons()
        st.success("Pago Exitoso.")
    
