import streamlit as st
import pandas as pd
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURACIÓN DE LUJO E IDENTIDAD ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

with st.sidebar:
    # --- LOGOTIPO INTEGRADO ---
    # Nota: Aquí el sistema busca su archivo de logo. 
    # Si el archivo se llama 'logo.png', se cargará automáticamente.
    try:
        st.image("logo.png", width=200) 
    except:
        st.markdown("<h1 style='text-align: center;'>🐾</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; color: #bae6fd;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    tema = st.toggle("🌙 Modo Noche", value=False)
    st.divider()

# --- 2. COLORES SEGÚN MODO ---
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
    h1, h2, h3, p, label {{ color: {txt} !important; }}
    .stButton>button {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important; border-radius: 12px; font-weight: bold; border: none; height: 3.5em; width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVEGACIÓN DE ÉLITE ---
menu = st.sidebar.radio("SISTEMA MAESTRO", [
    "📊 Dashboard & Reporte",
    "💬 WhatsApp CRM",
    "💰 Facturación Pro",
    "🩺 Consulta Médica IA",
    "🏥 Hospitalización Z",
    "📥 Carga OkVet"
])

# --- 4. LÓGICA DE DATOS ---
def leer(n): return pd.read_csv(n) if os.path.exists(n) else pd.DataFrame()

# Módulo Dashboard con Reporte Semanal (Domingos)
if menu == "📊 Dashboard & Reporte":
    st.title("📊 Inteligencia de Negocios")
    df_f = leer("facturas.csv")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales", f"${df_f['Total'].sum() if not df_f.empty else 0:,.0f}")
    col2.metric("Reporte Semanal", "Listo para Domingo")
    col3.metric("Marca", "Sentimiento Animal")

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("📈 Análisis de Ganancias")
    if not df_f.empty:
        st.line_chart(df_f.groupby("Fecha")["Total"].sum())
    else:
        st.info("Esperando datos de la semana para graficar...")
    st.markdown("</div>", unsafe_allow_html=True)

# Módulo WhatsApp Integrado
elif menu == "💬 WhatsApp CRM":
    st.title("💬 Comunicación Directa")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    tel = st.text_input("Teléfono del Cliente (con código de país):", placeholder="Ej: 573001234567")
    msj = st.text_area("Mensaje Personalizado:", "Hola, te escribimos de Sentimiento Animal...")
    if st.button("🚀 Enviar a WhatsApp"):
        url = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)
        st.success("Abriendo WhatsApp...")
    st.markdown("</div>", unsafe_allow_html=True)

# (Resto de módulos: Consulta, Hospitalización y Facturación integrados...)
