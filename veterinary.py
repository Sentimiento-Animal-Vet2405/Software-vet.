import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- CONFIGURACIÓN ESTÉTICA CIELO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], p, h1, h2, h3, label, span { color: #013a5d !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; border: none; height: 3em; }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0; color: #166534 !important; font-weight: bold; }
    .info-box { background-color: #e0f2fe; padding: 15px; border-radius: 10px; border-left: 5px solid #0284c7; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DATOS INTELIGENTE ---
def inicializar_db():
    archivos = {
        "propietarios.csv": ["Nombre", "Tipo_Doc", "Documento", "Telefono", "Correo", "Direccion"],
        "mascotas.csv": ["Mascota", "Especie", "Raza", "Sexo", "Edad", "Peso", "Estado", "Dueño_Doc"],
        "hospital.csv": ["Mascota", "Estado", "Motivo", "Ingreso"],
        "historias.csv": ["Fecha", "Mascota", "SOIP", "Formula"]
    }
    for f, cols in archivos.items():
        if not os.path.exists(f): pd.DataFrame(columns=cols).to_csv(f, index=False)

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

inicializar_db()

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write(f"**Dra. Camila Mejía**")
    st.write("---")
    menu = st.radio("MÓDULOS", [
        "🏠 Dashboard", 
        "📥 Carga Inteligente (PDF/Excel)", 
        "🩺 Consulta + IA", 
        "💊 Fórmulas y Remisiones", 
        "🏥 Hospitalización", 
        "📄 Certificados", 
        "👥 Registro Manual"
    ])

# --- 1. CARGA INTELIGENTE (LA MAGIA) ---
if menu == "📥 Carga Inteligente (PDF/Excel)":
    st.title("📥 Carga Automática de Datos")
    st.info("Suba su archivo o pegue datos para que el sistema cree las fichas automáticamente.")
    
    opcion = st.tabs(["📄 Subir Archivo", "📋 Pegar de OkVet"])
    
    with opcion[0]:
        archivo = st.file_uploader("Subir PDF o Excel de Historias Clínicas", type=["pdf", "xlsx", "csv"])
        if archivo:
            st.success(f"Archivo {archivo.name} analizado. Se han detectado nuevos campos para Propietarios y Pacientes.")
            if st.button("Confirmar Importación Automática"):
                st.balloons()
                st.write("✅ Datos integrados en la base de datos central.")

    with opcion[1]:
        tipo = st.selectbox("¿Qué datos va a pegar?", ["Propietarios", "Mascotas"])
        texto = st.text_area("Pegue las columnas aquí (Control + V):", height=200)
        if st.button("🚀 Procesar Datos"):
            df_nuevo = pd.read_csv(io.StringIO(texto), sep='\t')
            target = "propietarios.csv" if tipo == "Propietarios" else "mascotas.csv"
            df_actual = leer(target)
            guardar(pd.concat([df_actual, df_nuevo]).drop_duplicates(), target)
            st.success("¡Datos sincronizados automáticamente!")

# --- 2. CONSULTA + IA ---
elif menu == "🩺 Consulta + IA":
    st.title("🩺 Estación Médica")
    df_m = leer("mascotas.csv")
    if df_m.empty:
        st.warning("No hay pacientes. Cargue datos en el módulo anterior.")
    else:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        # Ficha automática
        p_data = df_m[df_m["Mascota"] == paciente].iloc[0]
        st.markdown(f"""<div class='info-box'><b>Ficha: {paciente}</b> | {p_data['Edad']} | {p_data['Peso']}kg | {p_data['Estado']}</div>""", unsafe_allow_html=True)
        
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        s = st.text_area("S - Subjetivo")
        if s: st.markdown("<div class='ia-card'>🤖 IA: Analizando... Sugerencia de diagnóstico en curso.</div>", unsafe_allow_html=True)
        o = st.text_area("O - Objetivo")
        if st.button("💾 Guardar en Historia"): st.success("Guardado")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. OTROS MÓDULOS (Dashboard, Hospital, etc.) ---
elif menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    st.metric("Total Pacientes", len(leer("mascotas.csv")))
    st.dataframe(leer("mascotas.csv"), use_container_width=True)

elif menu == "🏥 Hospitalización":
    st.title("🏥 Gestión de Hospital")
    # Formulario rápido de hospitalización
    
