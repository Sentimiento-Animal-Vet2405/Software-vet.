import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

# Intentamos importar reportlab, si falla, le avisamos al sistema
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sentimiento Animal Vet", layout="wide")

# Intentar cargar el logo (evita errores si el archivo no existe aún)
LOGO_PATH = "logo.png"
existe_logo = os.path.exists(LOGO_PATH)

# --- FUNCIÓN PDF ---
def generar_receta_pdf(paciente, dueno, tratamiento):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []
    
    if existe_logo:
        try:
            img = Image(LOGO_PATH, width=100, height=100)
            elementos.append(img)
        except: pass
    
    elementos.append(Paragraph(f"<b>Dra. Camila Mejia Muñoz</b>", styles['Title']))
    elementos.append(Paragraph(f"Paciente: {paciente} | Dueño: {dueno}", styles['Normal']))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("INDICACIONES:", styles['Heading3']))
    elementos.append(Paragraph(tratamiento, styles['Normal']))
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

# --- INTERFAZ ---
st.title("🐾 Sentimiento Animal Vet")
st.sidebar.header("Menú de Control")
opcion = st.sidebar.radio("Ir a:", ["Consulta", "Cálculo de Dosis", "Vacunas", "Hospitalización"])

if opcion == "Consulta":
    st.header("📝 Nueva Historia Clínica")
    c1, c2 = st.columns(2)
    pax = c1.text_input("Nombre Mascota")
    propie = c2.text_input("Propietario")
    tratamiento = st.text_area("Tratamiento (para la receta)")
    
    if st.button("Guardar Consulta"):
        if PDF_DISPONIBLE:
            pdf = generar_receta_pdf(pax, propie, tratamiento)
            st.success("¡Datos listos!")
            st.download_button("📩 Descargar Receta PDF", data=pdf, file_name=f"Receta_{pax}.pdf", mime="application/pdf")
        else:
            st.error("Error: El archivo requirements.txt no se ha cargado correctamente aún.")

elif opcion == "Cálculo de Dosis":
    st.header("🧮 Calculadora")
    peso = st.number_input("Peso (kg)", 0.1)
    dosis = st.number_input("Dosis (mg/kg)", 0.1)
    conc = st.number_input("Concentración (mg/ml)", 0.1)
    if conc > 0:
        st.metric("Volumen a aplicar", f"{(peso*dosis)/conc:.2f} ml")

elif opcion == "Vacunas":
    st.header("💉 Próximas Vacunas")
    st.info("Módulo de registro preventivo")

elif opcion == "Hospitalización":
    st.header("🏥 Seguimiento")
    st.text_area("Evolución del paciente")
