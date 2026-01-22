import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- ESTÉTICA PROFESIONAL ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    html, body, [class*="css"], p, h1, h2, h3, label, span { color: #02456e !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #0284c7 !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; border: none; height: 3em; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 10px; border: 1px solid #bbf7d0; color: #166534 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
DB_FILES = ["propietarios.csv", "mascotas.csv", "hospital.csv"]
for f in DB_FILES:
    if not os.path.exists(f): pd.DataFrame().to_csv(f, index=False)

def leer(n):
    try: return pd.read_csv(n)
    except: return pd.DataFrame()

def guardar(df, n):
    df.to_csv(n, index=False)

# --- MENÚ ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.write("---")
    menu = st.radio("MÓDULOS", [
        "🏠 Dashboard", 
        "👥 Propietarios y Mascotas", 
        "🩺 Consulta + IA", 
        "💊 Fórmulas y Remisiones", 
        "🏥 Hospitalización", 
        "📄 Certificados", 
        "📥 Importar OkVet"
    ])

# --- MÓDULO: PROPIETARIOS Y MASCOTAS (CON BÚSQUEDA) ---
if menu == "👥 Propietarios y Mascotas":
    st.title("👥 Gestión de Clientes y Pacientes")
    
    tab1, tab2 = st.tabs(["👤 Registrar Propietario", "🐕 Anexar Mascota a Dueño"])
    
    with tab1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Datos del Nuevo Propietario")
        with st.form("nuevo_propietario"):
            nom = st.text_input("Nombre Completo del Dueño")
            doc = st.text_input("Cédula / Documento")
            tel = st.text_input("Teléfono de Contacto")
            if st.form_submit_button("💾 Guardar Propietario"):
                if nom and doc:
                    df_p = leer("propietarios.csv")
                    nuevo = pd.DataFrame([[nom, doc, tel]], columns=["Nombre", "Documento", "Telefono"])
                    guardar(pd.concat([df_p, nuevo]), "propietarios.csv")
                    st.success(f"¡Propietario {nom} registrado!")
                    st.rerun()
                else:
                    st.error("Nombre y Documento son obligatorios.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("➕ Registrar Mascota a Propietario Existente")
        df_p = leer("propietarios.csv")
        
        if df_p.empty:
            st.warning("⚠️ No hay propietarios registrados aún. Por favor cree uno en la pestaña anterior.")
        else:
            # AQUÍ ESTÁ EL BUSCADOR: Crea una lista combinando Nombre y Documento para que sea fácil buscarlos
            df_p['Busqueda'] = df_p['Nombre'].astype(str) + " (" + df_p['Documento'].astype(str) + ")"
            opciones_duenos = df_p['Busqueda'].tolist()
            
            seleccion = st.selectbox("🔍 Busque y Seleccione al Propietario:", opciones_duenos)
            
            # Extraemos el documento de la selección para guardarlo correctamente
            doc_seleccionado = seleccion.split("(")[-1].replace(")", "")
            
            with st.form("nueva_mascota"):
                m_nom = st.text_input("Nombre de la Mascota")
                m_esp = st.selectbox("Especie", ["Canino", "Felino", "Equino", "Otro"])
                m_raz = st.text_input("Raza")
                
                if st.form_submit_button("🐾 Anexar Mascota"):
                    if m_nom:
                        df_m = leer("mascotas.csv")
                        nueva_m = pd.DataFrame([[m_nom, m_esp, m_raz, doc_seleccionado]], 
                                             columns=["Mascota", "Especie", "Raza", "Dueño"])
                        guardar(pd.concat([df_m, nueva_m]), "mascotas.csv")
                        st.success(f"¡{m_nom} ha sido anexado(a) a {seleccion}!")
                        st.balloons()
                    else:
                        st.error("El nombre de la mascota es obligatorio.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- RESTO DE MÓDULOS (Dashboard, Consulta, etc.) ---
elif menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p = leer("propietarios.csv")
    df_m = leer("mascotas.csv")
    c1, c2 = st.columns(2)
    c1.metric("Propietarios", len(df_p))
    c2.metric("Pacientes", len(df_m))
    st.write("### Base de Datos de Pacientes")
    st.dataframe(df_m, use_container_width=True)

elif menu == "🩺 Consulta + IA":
    st.title("🩺 Consulta Médica")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        p_sel = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        st.text_area("S - Hallazgos IA (Escriba síntomas aquí)")
        st.button("Guardar Consulta")

elif menu == "📥 Importar OkVet":
    st.title("📥 Importar desde Excel")
    target = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    datos = st.text_area("Pegue aquí los datos:")
    if st.button("🚀 Cargar"):
        df_up = pd.read_csv(io.StringIO(datos), sep='\t')
        guardar(df_up, target)
        st.success("Sincronizado")
        
