import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# --- CONFIGURACIÓN ESTÉTICA PREMIUM ---
st.set_page_config(page_title="Sentimiento Animal | Gestión Elite", layout="wide")

# CSS para elegancia: Sombras, gradientes y bordes redondeados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #fcfcfd;
    }
    
    /* Barra lateral elegante */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Tarjetas blancas con sombra sutil (como OkVet Pro) */
    .stBlock {
        background-color: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #f1f5f9;
        margin-bottom: 1.5rem;
    }
    
    /* Botones Premium */
    .stButton>button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Títulos con color azul marino */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    /* Inputs minimalistas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background-color: #f8fafc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
DB_PROPIETARIOS = "propietarios.csv"
DB_PACIENTES = "pacientes.csv"
DB_CONSULTAS = "consultas_soip.csv"

for db, cols in {
    DB_PROPIETARIOS: ["Documento", "Nombre", "Teléfono", "Correo", "Dirección"],
    DB_PACIENTES: ["ID_Prop", "Nombre_Mascota", "Especie", "Raza"],
    DB_CONSULTAS: ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P"]
}.items():
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# --- MENÚ LATERAL ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    st.markdown("<br><h3 style='color:white; text-align:center;'>Dra. Camila Mejía</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; text-align:center;'>Sentimiento Animal Vet</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN PRINCIPAL", 
                    ["✨ Dashboard", "👥 Clientes y Pacientes", "📋 Consulta Médica", "💾 Backup & Datos"])

# --- MÓDULO DASHBOARD ---
if menu == "✨ Dashboard":
    st.title("✨ Bienvenida al Sistema")
    st.markdown("Resumen general de tu práctica veterinaria.")
    
    df_p = pd.read_csv(DB_PROPIETARIOS)
    df_m = pd.read_csv(DB_PACIENTES)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Clientes", len(df_p))
    with c2:
        st.metric("Pacientes Registrados", len(df_m))
    with c3:
        st.metric("Consultas del Mes", "Digital")
    
    st.markdown("---")
    st.subheader("🔍 Localizador Rápido de Pacientes")
    busqueda = st.text_input("Buscar por nombre del paciente...", placeholder="Ej: Toby")
    if busqueda:
        df_c = pd.read_csv(DB_CONSULTAS)
        res = df_c[df_c["Mascota"].str.contains(busqueda, case=False, na=False)]
        st.dataframe(res, use_container_width=True)

# --- MÓDULO CLIENTES ---
elif menu == "👥 Clientes y Pacientes":
    st.title("👥 Gestión de Clientes")
    
    tab1, tab2 = st.tabs(["🆕 Registrar Dueño", "🐾 Vincular Paciente"])
    
    with tab1:
        with st.container():
            st.markdown("### Información del Propietario")
            with st.form("new_prop", clear_on_submit=True):
                col1, col2 = st.columns(2)
                doc = col1.text_input("Cédula / Documento *")
                nom = col2.text_input("Nombre Completo *")
                tel = col1.text_input("Teléfono de contacto")
                cor = col2.text_input("Correo electrónico")
                dir = st.text_input("Dirección de residencia")
                if st.form_submit_button("Guardar Propietario"):
                    if doc and nom:
                        df = pd.read_csv(DB_PROPIETARIOS)
                        pd.concat([df, pd.DataFrame([{"Documento":doc,"Nombre":nom,"Teléfono":tel,"Correo":cor,"Dirección":dir}])]).to_csv(DB_PROPIETARIOS, index=False)
                        st.success("✅ Propietario registrado exitosamente.")
    
    with tab2:
        df_p = pd.read_csv(DB_PROPIETARIOS)
        if not df_p.empty:
            st.markdown("### Nueva Mascota")
            propietario = st.selectbox("Seleccione el Dueño:", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
            id_p = propietario.split("(")[-1].replace(")","")
            
            with st.form("new_pet", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                p_nom = c1.text_input("Nombre Mascota")
                p_esp = c2.selectbox("Especie", ["Canino", "Felino", "Equino", "Otro"])
                p_raz = c3.text_input("Raza")
                if st.form_submit_button("Vincular al Sistema"):
                    df_m = pd.read_csv(DB_PACIENTES)
                    pd.concat([df_m, pd.DataFrame([{"ID_Prop":id_p,"Nombre_Mascota":p_nom,"Especie":p_esp,"Raza":p_raz}])]).to_csv(DB_PACIENTES, index=False)
                    st.success(f"🐾 {p_nom} ha sido vinculado correctamente.")

# --- MÓDULO CONSULTA ---
elif menu == "📋 Consulta Médica":
    st.title("📋 Registro Clínico SOIP")
    df_p = pd.read_csv(DB_PROPIETARIOS)
    df_m = pd.read_csv(DB_PACIENTES)
    
    if not df_p.empty and not df_m.empty:
        col_sel1, col_sel2 = st.columns(2)
        prop = col_sel1.selectbox("Propietario", df_p["Nombre"] + " (" + df_p["Documento"].astype(str) + ")")
        doc_id = prop.split("(")[-1].replace(")","")
        
        mascotas = df_m[df_m["ID_Prop"].astype(str) == doc_id]["Nombre_Mascota"].tolist()
        masc_sel = col_sel2.selectbox("Paciente", mascotas)
        
        st.markdown("---")
        with st.container():
            col_s, col_o = st.columns(2)
            s = col_s.text_area("S: Subjetivo", height=120, placeholder="Anamnesis y síntomas...")
            o = col_o.text_area("O: Objetivo", height=120, placeholder="Constantes y examen físico...")
            
            col_i, col_p = st.columns(2)
            i = col_i.text_area("I: Interpretación", height=120, placeholder="Diagnóstico...")
            p = col_p.text_area("P: Plan Terapéutico", height=120, placeholder="Tratamiento y medicina...")
            
            if st.button("💾 FINALIZAR Y GUARDAR CONSULTA"):
                df_c = pd.read_csv(DB_CONSULTAS)
                nueva = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "ID_Prop": doc_id, "Mascota": masc_sel, "S": s, "O": o, "I": i, "P": p}
                pd.concat([df_c, pd.DataFrame([nueva])]).to_csv(DB_CONSULTAS, index=False)
                st.balloons()
                st.success(f"Consulta de {masc_sel} guardada con éxito.")

# --- MÓDULO BACKUP ---
elif menu == "💾 Backup & Datos":
    st.title("💾 Centro de Datos")
    st.info("Desde aquí puedes descargar tus respaldos o importar registros masivos.")
    
    # Aquí irían los botones de descarga de Excel que ya configuramos
    st.write("Seleccione la acción deseada:")
    st.button("📥 Descargar Copia de Seguridad Excel")
    st.button("📤 Importar Pacientes de Excel")
