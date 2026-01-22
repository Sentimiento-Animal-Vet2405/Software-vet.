import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime, date

# --- CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: ESTÉTICA CIELO (Celeste claro, Letras Negras, Logo Circular)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f9ff; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; border-right: 1px solid #7dd3fc; }
    [data-testid="stSidebar"] [data-testid="stImage"] img { border-radius: 50%; border: 3px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    p, span, label, h1, h2, h3, .stMarkdown { color: #000000 !important; }
    .main-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e0f2fe; margin-bottom: 20px; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 12px; font-weight: 700; height: 3rem; border: none; }
    .stDownloadButton>button { background: #0ea5e9 !important; color: white !important; border-radius: 12px; font-weight: 700; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- BASES DE DATOS ---
DB_FILES = {
    "propietarios": ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"],
    "mascotas": ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"],
    "historias": ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab", "Hosp"]
}

for db, cols in DB_FILES.items():
    if not os.path.exists(f"{db}.csv"):
        pd.DataFrame(columns=cols).to_csv(f"{db}.csv", index=False)

# --- NAVEGACIÓN ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=140)
    st.markdown("<h2 style='text-align:center;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENÚ PRINCIPAL", ["🏠 Dashboard", "👥 Clientes", "🐾 Pacientes", "🩺 Consulta IA", "📥 Importar de OkVet", "💾 Reportes"])

# --- MODULO IMPORTAR ---
if menu == "📥 Importar de OkVet":
    st.title("📥 Migración Maestra desde OkVet")
    st.write("Dra. Camila, siga estos pasos para traer su información:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("1. Descargar Plantilla")
        t_tipo = st.selectbox("Elija qué va a organizar:", ["propietarios", "mascotas"])
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            pd.DataFrame(columns=DB_FILES[t_tipo]).to_excel(writer, index=False)
        st.download_button(f"📥 Bajar Plantilla de {t_tipo}", buffer.getvalue(), f"plantilla_{t_tipo}.xlsx")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("2. Subir Archivo Listo")
        ok_file = st.file_uploader("Suba el Excel con los datos de OkVet", type=["xlsx"])
        if ok_file:
            df_up = pd.read_excel(ok_file)
            if st.button("🚀 Cargar a la Nube"):
                df_base = pd.read_csv(f"{t_tipo}.csv")
                pd.concat([df_base, df_up]).to_csv(f"{t_tipo}.csv", index=False)
                st.success("¡Datos migrados con éxito!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- MODULO REPORTES ---
elif menu == "💾 Reportes":
    st.title("💾 Centro de Impresión")
    df_h = pd.read_csv("historias.csv")
    if not df_h.empty:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        h_sel = st.selectbox("Seleccione Consulta para Imprimir:", df_h.index, format_func=lambda x: f"{df_h.iloc[x]['Mascota']} - {df_h.iloc[x]['Fecha']}")
        data = df_h.iloc[h_sel]
        
        # Formato de Impresión Elegante
        txt_print = f"""
        🐾 SENTIMIENTO ANIMAL ELITE 🐾
        Dra. Camila Mejía - Médica Veterinaria
        ------------------------------------------
        HISTORIA CLÍNICA - {data['Fecha']}
        ------------------------------------------
        PACIENTE: {data['Mascota']}
        DUEÑO (ID): {data['ID_Prop']}
        
        EXAMEN FÍSICO (O):
        {data['O']}
        
        DIAGNÓSTICO (I):
        {data['I']}
        
        TRATAMIENTO (P):
        {data['P']}
        ------------------------------------------
        Generado por Sentimiento IA.
        """
        st.text_area("Previsualización de Impresión", txt_print, height=300)
        st.download_button("📥 Descargar para Imprimir", txt_print, f"Historia_{data['Mascota']}.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No hay historias guardadas aún.")

# --- OTROS MÓDULOS ---
elif menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    st.metric("Pacientes Totales", len(pd.read_csv("mascotas.csv")))
    st.info("Utilice el menú de la izquierda para navegar.")

elif menu == "🩺 Consulta IA":
    st.title("🩺 Estación Médica")
    st.write("Aquí se cargará la lista de pacientes importados de OkVet.")
    # (Lógica de consulta SOIP...)
    
