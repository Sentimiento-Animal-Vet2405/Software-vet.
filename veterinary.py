import streamlit as st
import pandas as pd
import os
import io

# --- ESTÉTICA CIELO ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #f0f9ff; color: black !important; }
    [data-testid="stSidebar"] { background-color: #bae6fd !important; }
    .main-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0f2fe; color: black; margin-bottom:10px; }
    h1, h2, h3, p, label { color: black !important; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE BASES DE DATOS (CON COLUMNAS PARA EVITAR ERRORES) ---
DB_FILES = {
    "propietarios.csv": ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"],
    "mascotas.csv": ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"],
    "historias.csv": ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab", "Hosp"],
    "hospitalizados.csv": ["Paciente", "Propietario", "Estado", "Motivo", "Ingreso"]
}

for db, cols in DB_FILES.items():
    if not os.path.exists(db) or os.stat(db).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# --- FUNCION PARA LEER SEGURO ---
def cargar_datos(archivo):
    try:
        df = pd.read_csv(archivo)
        return df
    except:
        return pd.DataFrame(columns=DB_FILES[archivo])

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("## 🐾 Sentimiento Animal")
    st.write("---")
    menu = st.radio("MENÚ", ["🏠 Dashboard", "📥 Importar Datos", "🩺 Consulta", "👥 Clientes"])

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Inicio")
    df_p = cargar_datos("propietarios.csv")
    df_m = cargar_datos("mascotas.csv")
    
    col1, col2 = st.columns(2)
    col1.metric("Clientes Registrados", len(df_p))
    col2.metric("Mascotas Registradas", len(df_m))
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("Bienvenida Dra. Camila Mejía")
    if len(df_p) == 0:
        st.info("👋 El sistema está listo. Para empezar, vaya a 'Importar Datos' y suba su archivo de OkVet o registre un cliente manualmente.")
    else:
        st.success("Sistema activo con datos cargados.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MODULO DE IMPORTACIÓN ---
elif menu == "📥 Importar Datos":
    st.title("📥 Importación de Datos (OkVet)")
    target = st.selectbox("¿Qué datos va a subir?", ["propietarios.csv", "mascotas.csv"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    archivo = st.file_uploader("Subir archivo CSV (Si tiene Excel, guárdelo como CSV primero)", type=["csv"])
    
    if archivo:
        try:
            # Intenta leer con diferentes separadores comunes en Excel/Latam
            try:
                df = pd.read_csv(archivo, sep=',')
            except:
                df = pd.read_csv(archivo, sep=';')
            
            st.write("✅ Vista previa de los datos encontrados:")
            st.dataframe(df.head(5))
            
            if st.button("🚀 GUARDAR E INTEGRAR DATOS"):
                df_actual = cargar_datos(target)
                df_final = pd.concat([df_actual, df]).drop_duplicates()
                df_final.to_csv(target, index=False)
                st.success(f"¡Éxito! Se han integrado los datos en {target}.")
                st.balloons()
        except Exception as e:
            st.error("Error al leer el archivo. Asegúrese de que sea un archivo CSV válido.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CLIENTES (REGISTRO MANUAL) ---
elif menu == "👥 Clientes":
    st.title("👥 Registro Manual")
    with st.form("manual_cli"):
        n = st.text_input("Nombre")
        d = st.text_input("Documento")
        t = st.text_input("Teléfono")
        if st.form_submit_button("Guardar"):
            df_p = cargar_datos("propietarios.csv")
            new_p = pd.DataFrame([{"Nombre":n, "Numero":d, "Teléfono":t}])
            pd.concat([df_p, new_p]).to_csv("propietarios.csv", index=False)
            st.success("Guardado manualmente.")
            
