import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #083344 !important; }
    .main-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { 
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important; 
        color: white !important; border-radius: 12px; font-weight: 600; border: none; height: 3.5em; width: 100%;
    }
    .metric-box { background: white; padding: 20px; border-radius: 15px; border-top: 5px solid #0284c7; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE BASES DE DATOS ---
DB_ARCHIVOS = {
    "propietarios.csv": ["Nombre", "Tipo_Doc", "Documento", "Telefono", "Correo", "Direccion"],
    "mascotas.csv": ["Mascota", "Especie", "Raza", "Sexo", "Edad", "Peso_Actual", "Estado", "Dueño_Doc"],
    "historias.csv": ["Fecha", "Mascota", "Peso", "S", "O", "I", "P"],
    "inventario.csv": ["Item", "Categoría", "Precio"],
    "facturas.csv": ["ID", "Fecha", "Mascota", "Total", "Items"]
}

for f, cols in DB_ARCHIVOS.items():
    if not os.path.exists(f) or os.stat(f).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(f, index=False)

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. MENÚ LATERAL ---
with st.sidebar:
    st.title("Sentimiento Animal")
    st.write("🏥 **Dra. Camila Mejía**")
    st.markdown("---")
    menu = st.radio("MENÚ PRINCIPAL", [
        "📊 Dashboard General",
        "🩺 Consulta + Peso",
        "📚 Historiales & Gráficas",
        "💰 Facturación Pro",
        "📦 Inventario",
        "📥 Importar Datos"
    ])

# --- 4. DASHBOARD (GRÁFICAS COMPATIBLES) ---
if menu == "📊 Dashboard General":
    st.title("📊 Resumen de Gestión")
    df_p, df_m, df_f = leer("propietarios.csv"), leer("mascotas.csv"), leer("facturas.csv")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Dueños", len(df_p))
    m2.metric("Pacientes", len(df_m))
    m3.metric("Ingresos Total", f"${df_f['Total'].sum():,.0f}" if not df_f.empty else "$0")
    
    st.write("---")
    st.subheader("📈 Evolución de Ingresos (Vista Rápida)")
    if not df_f.empty:
        # Gráfica nativa de Streamlit (No requiere Plotly)
        df_f['Fecha'] = pd.to_datetime(df_f['Fecha'])
        st.line_chart(df_f.set_index('Fecha')['Total'])
    else: st.info("Sin datos financieros aún.")

# --- 5. CONSULTA MÉDICA ---
elif menu == "🩺 Consulta + Peso":
    st.title("🩺 Estación Médica")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        peso_v = col1.number_input("Peso Hoy (Kg)", min_value=0.0, step=0.1)
        fecha_v = col2.date_input("Fecha", datetime.now())
        s = st.text_area("S - Subjetivo")
        o, i, p = st.text_area("O - Objetivo"), st.text_area("I - Interpretación"), st.text_area("P - Plan")
        
        if st.button("💾 Guardar Consulta"):
            df_h = leer("historias.csv")
            nueva_h = pd.DataFrame([[fecha_v.strftime("%Y-%m-%d"), paciente, peso_v, s, o, i, p]], columns=df_h.columns)
            guardar(pd.concat([df_h, nueva_h]), "historias.csv")
            df_m.loc[df_m['Mascota'] == paciente, 'Peso_Actual'] = peso_v
            guardar(df_m, "mascotas.csv")
            st.success("Guardado correctamente.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. HISTORIAL Y GRÁFICA DE PESO COMPATIBLE ---
elif menu == "📚 Historiales & Gráficas":
    st.title("📚 Expediente de Peso")
    df_h = leer("historias.csv")
    df_m = leer("mascotas.csv")
        
