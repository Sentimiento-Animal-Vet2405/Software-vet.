import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL "CIELO" (MÁXIMA COMPATIBILIDAD) ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    /* Fondo claro y limpio */
    .stApp { background-color: #f0f9ff; }
    
    /* Barra lateral azul profundo profesional */
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: #f0f9ff !important; }
    
    /* Tarjetas blancas con bordes suaves */
    .main-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid #bae6fd; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
        margin-bottom: 20px; 
    }
    
    /* Botones en degradado azul cielo */
    .stButton>button { 
        background: linear-gradient(95deg, #0284c7 0%, #0369a1 100%) !important; 
        color: white !important; 
        border-radius: 12px; 
        font-weight: 600; 
        border: none; 
        height: 3.5em; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); }

    /* Títulos y textos */
    h1, h2, h3 { color: #0c4a6e !important; }
    .metric-card { background: white; padding: 20px; border-radius: 15px; border-top: 5px solid #0284c7; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASES DE DATOS ---
DB_FILES = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo"],
    "mascotas.csv": ["Mascota", "Especie", "Raza", "Peso_Actual", "Dueño_Doc"],
    "historias.csv": ["Fecha", "Mascota", "Peso", "Evolucion"],
    "inventario.csv": ["Item", "Precio"],
    "facturas.csv": ["ID", "Fecha", "Mascota", "Total"]
}

for f, cols in DB_FILES.items():
    if not os.path.exists(f) or os.stat(f).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(f, index=False)

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐾</h1>", unsafe_allow_html=True)
    st.title("Sentimiento Animal")
    st.write("Dra. Camila Mejía")
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN", [
        "📊 Dashboard", "🩺 Consulta y Peso", "📚 Historias", "💰 Facturación", "📦 Precios"
    ])

# --- 4. DASHBOARD (GRÁFICAS LUMINOSAS) ---
if menu == "📊 Dashboard":
    st.title("📊 Resumen de la Clínica")
    df_m, df_f = leer("mascotas.csv"), leer("facturas.csv")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><h3>Pacientes</h3><h2>{len(df_m)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><h3>Ingresos</h3><h2>${df_f['Total'].sum():,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-card'><h3>Estado</h3><h2>Activo</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📈 Evolución de Ingresos")
    if not df_f.empty:
        # Gráfica nativa (sin errores de carga)
        st.area_chart(df_f.groupby("Fecha")["Total"].sum(), color="#0284c7")
    else: st.info("Esperando datos de facturación...")

# --- 5. CONSULTA Y PESO ---
elif menu == "🩺 Consulta y Peso":
    st.title("🩺 Nueva Consulta")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        pac_sel = st.selectbox("Paciente:", df_m["Mascota"].tolist())
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        peso = st.number_input("Peso Actual (Kg):", min_value=0.0, step=0.1)
        det = st.text_area("Notas Médicas (SOIP):")
        if st.button("💾 Guardar Consulta"):
            # Guardar historia
            df_h = leer("historias.csv")
            nueva = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), pac_sel, peso, det]], columns=df_h.columns)
            guardar(pd.concat([df_h, nueva]), "historias.csv")
            # Actualizar peso actual
            df_m.loc[df_m['Mascota'] == pac_sel, 'Peso_Actual'] = peso
            guardar(df_m, "mascotas.csv")
            st.success("¡Información guardada y peso actualizado!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. HISTORIAS Y GRÁFICA DE PESO ---
elif menu == "📚 Historias":
    st.title("📚 Expedientes Médicos")
    df_h = leer("historias.csv")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        pac = st.selectbox("Ver a:", df_m["Mascota"].tolist())
        registros = df_h[df_h["Mascota"] == pac].sort_values("Fecha")
        
        if not registros.empty:
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            st.subheader(f"📈 Curva de Peso de {pac}")
            # Gráfica de peso azul cielo
            st.line_chart(registros.set_index("Fecha")["Peso"], color="#0ea5e9")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("### Evoluciones")
            st.dataframe(registros[["Fecha", "Peso", "Evolucion"]], use_container_width=True)
            
            # Botón de descarga
            txt = registros.to_string()
            st.download_button("📥 Descargar Historia Clínica", txt, file_name=f"Historia_{pac}.txt")

# --- 7. FACTURACIÓN ---
elif menu == "💰 Facturación":
    st.title("💰 Cobros y Caja")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    df_m = leer("mascotas.csv")
    pac = st.selectbox("Cobrar a:", df_m["Mascota"].tolist() if not df_m.empty else [])
    total = st.number_input("Total de la Cuenta ($):", min_value=0)
    if st.button("✅ Confirmar Pago"):
        df_f = leer("facturas.csv")
        nueva_f = pd.DataFrame([[len(df_f)+1, datetime.now().strftime("%Y-%m-%d"), pac, total]], columns=df_f.columns)
        guardar(pd.concat([df_f, nueva_f]), "facturas.csv")
        st.success(f"Cobro de ${total} registrado con éxito.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. PRECIOS ---
elif menu == "📦 Precios":
    st.title("📦 Tarifario")
    with st.form("tarifas"):
        it = st.text_input("Servicio o Medicamento")
        pr = st.number_input("Precio ($)")
        if st.form_submit_button("Guardar"):
            df = leer("inventario.csv")
            guardar(pd.concat([df, pd.DataFrame([[it, pr]], columns=df.columns)]), "inventario.csv")
            st.rerun()
    st.dataframe(leer("inventario.csv"), use_container_width=True)
    
