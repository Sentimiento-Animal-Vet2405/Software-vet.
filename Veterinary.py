import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# --- CONFIGURACIÓN Y DATOS PROFESIONALES ---
st.set_page_config(page_title="Sentimiento Animal Vet", layout="wide")
LOGO_PATH = "logo.png" 

DATOS_VET = {
    "nombre": "Dra. Camila Mejía Muñoz",
    "titulo": "Médica Veterinaria y Zootecnista",
    "clinica": "Sentimiento Animal Vet",
    "info_extra": "Atención Veterinaria Domiciliaria"
}

# --- FUNCIÓN PARA GENERAR EL PDF DE LA RECETA ---
def generar_receta_pdf(paciente, dueno, tratamiento, peso):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Encabezado con Logo y Datos
    try:
        img = Image(LOGO_PATH, width=100, height=100)
        info_vet = Paragraph(f"<b>{DATOS_VET['nombre']}</b><br/>{DATOS_VET['titulo']}<br/>{DATOS_VET['info_extra']}", styles['Normal'])
        header_table = Table([[img, info_vet]], colWidths=[120, 350])
        elementos.append(header_table)
    except:
        elementos.append(Paragraph(f"<b>{DATOS_VET['clinica']}</b>", styles['Title']))

    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("<hr/>", styles['Normal']))
    
    # Datos del Paciente
    data_paciente = [
        ["PACIENTE:", paciente.upper(), "PESO:", f"{peso} kg"],
        ["PROPIETARIO:", dueno.upper(), "FECHA:", datetime.now().strftime("%d/%m/%Y")]
    ]
    t_pax = Table(data_paciente, colWidths=[100, 150, 80, 150])
    t_pax.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('BACKGROUND', (0,0), (0,1), colors.whitesmoke)]))
    elementos.append(t_pax)
    
    elementos.append(Spacer(1, 30))
    
    # Tratamiento
    elementos.append(Paragraph("<b>RP / PLAN TERAPÉUTICO:</b>", styles['Heading3']))
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(tratamiento.replace("\n", "<br/>"), styles['Normal']))
    
    # Firma
    elementos.append(Spacer(1, 60))
    elementos.append(Paragraph("__________________________", styles['Normal']))
    elementos.append(Paragraph(f"{DATOS_VET['nombre']}<br/>{DATOS_VET['titulo']}", styles['Normal']))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

# --- INTERFAZ DE LA APLICACIÓN ---
st.sidebar.image(LOGO_PATH, width=150) if st.sidebar.button("Cargar Logo") or True else None
menu = st.sidebar.radio("MENÚ PRINCIPAL", ["Consulta e Historia", "Vacunas y Desparasitación", "Cálculo de Dosis", "Hospitalización"])

if menu == "Consulta e Historia":
    st.header("📝 Nueva Consulta Clínica")
    
    with st.form("form_consulta"):
        c1, c2 = st.columns(2)
        with c1:
            paciente = st.text_input("Nombre de la Mascota")
            especie = st.selectbox("Especie", ["Canino", "Felino", "Equino", "Otro"])
            peso = st.number_input("Peso Actual (kg)", min_value=0.1)
        with c2:
            dueno = st.text_input("Nombre del Propietario")
            motivo = st.text_input("Motivo de la visita")
            
        anamnesis = st.text_area("Anamnesis y Examen Físico")
        tratamiento = st.text_area("Prescripción Médica (Lo que saldrá en el PDF)")
        
        guardar = st.form_submit_button("Guardar Consulta y Generar Receta")
        
        if guardar:
            pdf = generar_receta_pdf(paciente, dueno, tratamiento, peso)
            st.success(f"¡Historia de {paciente} guardada correctamente!")
            st.download_button(label="📩 Descargar Receta para WhatsApp", 
                             data=pdf, 
                             file_name=f"Receta_{paciente}_{datetime.now().strftime('%Y%m%d')}.pdf", 
                             mime="application/pdf")

elif menu == "Cálculo de Dosis":
    st.header("🧮 Calculadora de Dosis")
    col1, col2, col3 = st.columns(3)
    with col1:
        p_kg = st.number_input("Peso del Paciente (kg)", 0.1)
    with col2:
        d_mg = st.number_input("Dosis (mg/kg)", 0.1)
    with col3:
        c_mgml = st.number_input("Concentración (mg/ml)", 0.1)
    
    if c_mgml > 0:
        total = (p_kg * d_mg) / c_mgml
        st.metric("Volumen a administrar", f"{total:.2f} ml")
        st.info(f"Fórmula: ({p_kg}kg x {d_mg}mg) / {c_mgml}mg/ml")

elif menu == "Vacunas y Desparasitación":
    st.header("💉 Control Preventivo")
    st.date_input("Fecha de Aplicación")
    st.text_input("Producto / Marca")
    st.selectbox("Tipo", ["Vacuna", "Desparasitante Interno", "Desparasitante Externo"])
    st.write("Sugerencia de refuerzo: 21 días (Vacunas) / 3 meses (Parásitos)")

elif menu == "Hospitalización":
    st.header("🏥 Seguimiento de Paciente Domiciliario")
    st.text_area("Constantes Fisiológicas (T°, FC, FR, TLLC)")
    st.text_area("Evolución del Cuadro")
    
