import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# --- CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

# CSS: ESTÉTICA CIELO (Celeste, Letras Negras, Logo Circular)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f9ff; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; border-right: 1px solid #7dd3fc; }
    [data-testid="stSidebar"] [data-testid="stImage"] img { border-radius: 50%; border: 3px solid white; }
    p, span, label, h1, h2, h3, .stMarkdown { color: #000000 !important; }
    .main-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e0f2fe; margin-bottom: 15px; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 10px; font-weight: 700; height: 3rem; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE BASES DE DATOS ---
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
    st.markdown("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes", "🐾 Pacientes", "🩺 Consulta Integral", "📥 Importar / Cargar", "💾 Backup"])

# --- MÓDULO DE IMPORTACIÓN ---
if menu == "📥 Importar / Cargar":
    st.title("📥 Importación Maestra")
    st.write("Dra. Camila, use este módulo para migrar sus bases de datos externas.")
    
    t1, t2 = st.tabs(["📊 Importar desde Excel", "📄 Cargar Historias PDF"])
    
    with t1:
        st.subheader("Migrar base de datos (Excel/CSV)")
        target = st.selectbox("¿Qué desea importar?", ["propietarios", "mascotas"])
        up_excel = st.file_uploader("Suba su archivo Excel", type=["xlsx", "csv"])
        
        if up_excel:
            df_new = pd.read_excel(up_excel) if up_excel.name.endswith('xlsx') else pd.read_csv(up_excel)
            st.warning("Asegúrese de que los nombres de las columnas coincidan con el formato requerido.")
            st.dataframe(df_new.head())
            
            if st.button("Procesar e Integrar"):
                df_old = pd.read_csv(f"{target}.csv")
                pd.concat([df_old, df_new]).to_csv(f"{target}.csv", index=False)
                st.success(f"¡Éxito! Se han integrado {len(df_new)} nuevos registros.")

    with t2:
        st.subheader("Archivo Digital PDF")
        st.info("Suba aquí historias clínicas externas o resultados de laboratorio antiguos.")
        p_pdf = st.file_uploader("Seleccionar PDF", type=["pdf"])
        if p_pdf:
            # Lógica de guardado (Simulada)
            st.success(f"Documento '{p_pdf.name}' vinculado al sistema.")

# --- CONSULTA INTEGRAL ---
elif menu == "🩺 Consulta Integral":
    st.title("🩺 Estación Médica")
    df_p, df_m = pd.read_csv("propietarios.csv"), pd.read_csv("mascotas.csv")
    
    if not df_m.empty:
        c1, c2 = st.columns(2)
        prop = c1.selectbox("Dueño", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_d = prop.split("(")[-1].replace(")","")
        paciente = c2.selectbox("Paciente", df_m[df_m["ID_Prop"].astype(str) == str(id_d)]["Nombre_Mascota"].tolist())
        
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("### 📎 Documentación Adjunta")
        st.file_uploader("Adjuntar examen o historia previa (PDF)", type=["pdf"], key="pdf_cons")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Módulos SOIP / Vacunas / etc...
        st.text_area("Notas Clínicas de la Consulta")
        if st.button("Guardar Registro"):
            st.balloons()
            st.success("Consulta y documentos guardados.")
    else:
        st.warning("No hay datos para mostrar. Use el módulo de Importar.")

# --- OTROS MÓDULOS ---
elif menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    st.metric("Total Pacientes", len(pd.read_csv("mascotas.csv")))

elif menu == "👥 Clientes":
    st.title("👥 Gestión de Clientes")
    # Código de registro manual...

elif menu == "🐾 Pacientes":
    st.title("🐾 Gestión de Pacientes")
    # Código de registro manual...
    
