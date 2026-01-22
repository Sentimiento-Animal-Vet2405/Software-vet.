import streamlit as st
import pandas as pd
import io
from datetime import datetime

# --- CONFIGURACIÓN DE APARIENCIA ---
st.set_page_config(page_title="Sentimiento Animal - OkVet Style", layout="wide")

# CSS para imitar la interfaz de las fotos (OkVet)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #3b82f6; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .block-container { padding-top: 2rem; }
    .st-expander { background-color: white; border-radius: 15px; border: 1px solid #e2e8f0; }
    h1 { color: #1e3a8a; font-family: 'sans-serif'; }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ LATERAL (Como el de la foto) ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.title("SENTIMIENTO ANIMAL VET")
    st.markdown("---")
    menu = st.radio("MENÚ", [
        "🏠 Historia Clínica", 
        "📋 Consultas (SOIP)", 
        "💉 Vacunación", 
        "💊 Fórmulas médicas",
        "🐛 Desparasitaciones",
        "🏥 Hospitalización",
        "🧬 Exámenes",
        "🚑 Remisiones"
    ])

# --- LÓGICA DE MÓDULOS ---

if menu == "📋 Consultas (SOIP)":
    st.markdown(f"## 📋 Registro de Consulta - {datetime.now().strftime('%d/%m/%Y')}")
    
    with st.container():
        # Encabezado rápido
        col_p1, col_p2, col_p3 = st.columns(3)
        paciente = col_p1.text_input("Mascota", placeholder="Ej: Lucky Munera")
        propietario = col_p2.text_input("Propietario", placeholder="Ej: Mariana Munera")
        motivo = col_p3.selectbox("Motivo", ["Consulta General", "Urgencia", "Control", "Procedimiento"])

        st.markdown("---")
        
        # Formato SOIP (Como en tu foto)
        col1, col2 = st.columns(2)
        with col1:
            subjetivo = st.text_area("S: Subjetivo (Anamnesis)", placeholder="Motivo de la consulta y antecedentes...")
            interpretacion = st.text_area("I: Interpretación (Diagnóstico)", placeholder="Diagnóstico presuntivo o final...")
        
        with col2:
            objetivo = st.text_area("O: Objetivo (Examen Físico)", placeholder="Detalles del examen, listado de problemas...")
            plan = st.text_area("P: Plan Terapéutico", placeholder="Tratamiento y medicamentos...")

        st.markdown("---")
        proximo = st.date_input("Próximo control")
        
        if st.button("💾 GUARDAR CONSULTA Y GENERAR PDF"):
            st.success(f"Consulta de {paciente} guardada exitosamente en el sistema.")
            # Aquí se activaría la descarga del PDF que ya tenemos configurada

elif menu == "🏠 Historia Clínica":
    st.header("🐾 Datos Generales de la Mascota")
    # Simulación de la ficha de la foto
    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("Cargar foto de la mascota")
    with c2:
        st.markdown("""
        **Especie:** Canino | **Raza:** Schnauzer Gigante | **Género:** Hembra
        **Peso:** 10.79 kg | **Edad:** 14 años, 2 meses
        """)
        st.line_chart([10.5, 11.2, 10.8, 10.79]) # Gráfico de peso como en la foto

elif menu == "💊 Fórmulas médicas":
    st.header("💊 Registro de Fórmula Médica")
    with st.expander("+ Agregar Medicamento", expanded=True):
        st.text_input("Nombre del Medicamento")
        col_f1, col_f2 = st.columns(2)
        col_f1.text_input("Presentación")
        col_f2.number_input("Cantidad", value=1)
        st.text_area("Posología (Forma de administración)")
    st.button("Generar Receta Médica")

# --- LOS DEMÁS MÓDULOS SIGUEN LA MISMA ESTÉTICA ---
else:
    st.info(f"Módulo de {menu} en desarrollo para imitar la interfaz de OkVet.")
