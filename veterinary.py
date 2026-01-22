import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL FORZADA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS inyectado para asegurar que los colores carguen
st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff !important; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1, h2, h3, p, span { color: #0c4a6e !important; }
    .stButton>button { background: #0284c7 !important; color: white !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ARCHIVOS (CREACIÓN AUTOMÁTICA) ---
def inicializar_db():
    archivos = {
        "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo"],
        "mascotas.csv": ["Mascota", "Especie", "Raza", "Peso_Actual", "Dueño_Doc"],
        "historias.csv": ["Fecha", "Mascota", "Peso", "SOIP"],
        "hospital.csv": ["Mascota", "Cama", "Motivo", "Tratamiento"],
        "inventario.csv": ["Item", "Precio"],
        "facturas.csv": ["ID", "Fecha", "Mascota", "Total"]
    }
    for nombre, columnas in archivos.items():
        if not os.path.exists(nombre):
            pd.DataFrame(columns=columnas).to_csv(nombre, index=False)

inicializar_db()

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. MENÚ DE NAVEGACIÓN ---
with st.sidebar:
    st.title("🐾 Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.divider()
    menu = st.radio("Módulos:", [
        "📊 Dashboard", 
        "🩺 Consulta Médica", 
        "🏥 Hospitalización", 
        "📈 Evolución de Peso",
        "💰 Facturación Pro", 
        "📦 Inventario",
        "📥 Carga Masiva (OkVet)"
    ])

# --- 4. MÓDULOS ---

if menu == "📊 Dashboard":
    st.title("📊 Resumen General")
    df_m = leer("mascotas.csv")
    df_f = leer("facturas.csv")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pacientes", len(df_m))
    col2.metric("Ingresos Total", f"${df_f['Total'].sum():,.0f}")
    col3.metric("Estado", "Operativo")
    
    st.subheader("Ventas")
    if not df_f.empty:
        st.line_chart(df_f.set_index("Fecha")["Total"])

elif menu == "🩺 Consulta Médica":
    st.title("🩺 Nueva Consulta")
    df_m = leer("mascotas.csv")
    if df_m.empty:
        st.warning("Debe registrar pacientes primero en 'Carga Masiva' o 'Propietarios'.")
    else:
        with st.container():
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            pac = st.selectbox("Mascota:", df_m["Mascota"].tolist())
            peso = st.number_input("Peso (Kg):", step=0.1)
            soip = st.text_area("Notas Médicas (S-O-I-P):")
            
            if st.button("💾 Guardar Historia"):
                df_h = leer("historias.csv")
                nueva = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), pac, peso, soip]], columns=df_h.columns)
                guardar(pd.concat([df_h, nueva]), "historias.csv")
                st.success("Guardado con éxito")
            st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🏥 Hospitalización":
    st.title("🏥 Pacientes Internados")
    df_hosp = leer("hospital.csv")
    if df_hosp.empty:
        st.info("No hay pacientes en hospitalización.")
    else:
        st.table(df_hosp)

elif menu == "📈 Evolución de Peso":
    st.title("📈 Curvas de Peso")
    df_h = leer("historias.csv")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        pac = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        datos = df_h[df_h["Mascota"] == pac]
        if not datos.empty:
            st.line_chart(datos.set_index("Fecha")["Peso"])
        else:
            st.write("No hay datos de peso para este paciente.")

elif menu == "💰 Facturación Pro":
    st.title("💰 Facturación")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    df_m = leer("mascotas.csv")
    pac = st.selectbox("Facturar a:", df_m["Mascota"].tolist() if not df_m.empty else [])
    total = st.number_input("Monto total ($):", min_value=0)
    if st.button("Finalizar Venta"):
        df_f = leer("facturas.csv")
        nueva_f = pd.DataFrame([[len(df_f)+1, datetime.now().strftime("%Y-%m-%d"), pac, total]], columns=df_f.columns)
        guardar(pd.concat([df_f, nueva_f]), "facturas.csv")
        st.success("Venta guardada")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📥 Carga Masiva (OkVet)":
    st.title("📥 Importar Datos")
    st.write("Pegue aquí sus datos de Excel o OkVet para empezar.")
    raw = st.text_area("Datos (Formato Tabla):")
    if st.button("Cargar Pacientes"):
        df_new = pd.read_csv(io.StringIO(raw), sep='\t')
        df_old = leer("mascotas.csv")
        guardar(pd.concat([df_old, df_new]).drop_duplicates(), "mascotas.csv")
        st.success("¡Datos cargados!")

elif menu == "📦 Inventario":
    st.title("📦 Inventario")
    df_i = leer("inventario.csv")
    st.dataframe(df_i, use_container_width=True)
    
