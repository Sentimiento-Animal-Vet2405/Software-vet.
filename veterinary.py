import streamlit as st
import pandas as pd
import os
import io
import plotly.express as px
from datetime import datetime

# --- 1. ESTÉTICA DE ALTA GAMA (AZUL CIELO Y BLANCO) ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #083344 !important; }
    .main-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { 
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important; 
        color: white !important; border-radius: 12px; font-weight: 600; border: none; height: 3.5em; width: 100%; transition: all 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 12px; border-left: 6px solid #22c55e; color: #166534; }
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
    st.markdown("<h1 style='text-align: center;'>🐾</h1>", unsafe_allow_html=True)
    st.title("Sentimiento Animal")
    st.write("🏥 **Dra. Camila Mejía**")
    st.markdown("---")
    menu = st.radio("MENÚ PRINCIPAL", [
        "📊 Dashboard General",
        "🩺 Consulta + IA + Peso",
        "📚 Historiales & Gráficas",
        "💰 Facturación y Caja",
        "📦 Tarifario e Inventario",
        "👥 Registro de Clientes",
        "📥 Importar Datos"
    ])

# --- 4. DASHBOARD (ANÁLISIS DE NEGOCIO) ---
if menu == "📊 Dashboard General":
    st.title("📊 Análisis Estratégico")
    df_p, df_m, df_f = leer("propietarios.csv"), leer("mascotas.csv"), leer("facturas.csv")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='metric-box'><h3>Dueños</h3><h2>{len(df_p)}</h2></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-box'><h3>Pacientes</h3><h2>{len(df_m)}</h2></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'><h3>Ingresos</h3><h2>${df_f['Total'].sum():,.0f}</h2></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='metric-box'><h3>Clínica</h3><h2>Elite</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("📈 Crecimiento de Ingresos")
        if not df_f.empty:
            fig_v = px.line(df_f.sort_values("Fecha"), x="Fecha", y="Total", template="plotly_white")
            st.plotly_chart(fig_v, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("🐕 Composición de Pacientes")
        if not df_m.empty:
            fig_p = px.pie(df_m, names='Especie', hole=0.4)
            st.plotly_chart(fig_p, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. CONSULTA MÉDICA + PESO ---
elif menu == "🩺 Consulta + IA + Peso":
    st.title("🩺 Estación Médica")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        peso_v = col1.number_input("Peso Actual (Kg)", min_value=0.0, step=0.1)
        fecha_v = col2.date_input("Fecha", datetime.now())
        
        s = st.text_area("S - Subjetivo (Síntomas)")
        if "vómito" in s.lower() or "diarrea" in s.lower():
            st.markdown("<div class='ia-card'>🤖 IA: Alerta gastrointestinal. Considerar test de Parvo/Corona y ayuno.</div>", unsafe_allow_html=True)
        
        o, i, p = st.text_area("O - Objetivo"), st.text_area("I - Interpretación"), st.text_area("P - Plan")
        
        if st.button("💾 Guardar y Actualizar Peso"):
            df_h = leer("historias.csv")
            nueva_h = pd.DataFrame([[fecha_v.strftime("%Y-%m-%d"), paciente, peso_v, s, o, i, p]], columns=df_h.columns)
            guardar(pd.concat([df_h, nueva_h]), "historias.csv")
            
            df_m.loc[df_m['Mascota'] == paciente, 'Peso_Actual'] = peso_v
            guardar(df_m, "mascotas.csv")
            st.success("Consulta guardada exitosamente.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. HISTORIALES Y GRÁFICAS DE PESO ---
elif menu == "📚 Historiales & Gráficas":
    st.title("📚 Expediente y Evolución de Peso")
    df_h = leer("historias.csv")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        paciente = st.selectbox("Expediente de:", df_m["Mascota"].tolist())
        registros = df_h[df_h["Mascota"] == paciente].sort_values("Fecha")
        
        if not registros.empty:
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            st.subheader(f"📈 Curva de Peso - {paciente}")
            fig_peso = px.line(registros, x="Fecha", y="Peso", markers=True, color_discrete_sequence=['#ef4444'])
            st.plotly_chart(fig_peso, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            for _, r in registros.iloc[::-1].iterrows():
                with st.expander(f"📅 {r['Fecha']} | {r['Peso']} Kg"):
                    st.write(f"**Plan:** {r['P']}")
                    
            # Descarga de Historia
            txt_hist = f"HISTORIA: {paciente}\n" + registros.to_string()
            st.download_button("📥 Descargar Historia Clínica", txt_hist, file_name=f"Historia_{paciente}.txt")

# --- 7. FACTURACIÓN Y CAJA ---
elif menu == "💰 Facturación y Caja":
    st.title("💰 Facturación Pro")
    df_inv = leer("inventario.csv")
    df_m = leer("mascotas.csv")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        paciente = st.selectbox("Facturar a:", df_m["Mascota"].tolist() if not df_m.empty else [])
        item = st.selectbox("Servicio/Medicamento:", df_inv["Item"].tolist() if not df_inv.empty else [])
        if 'carrito' not in st.session_state: st.session_state.carrito = []
        if st.button("➕ Agregar"):
            precio = df_inv[df_inv["Item"] == item]["Precio"].values[0]
            st.session_state.carrito.append({"item": item, "precio": precio})
        st.table(pd.DataFrame(st.session_state.carrito))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_b:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        total = sum([x['precio'] for x in st.session_state.carrito])
        st.subheader("Total Cobro")
        st.title(f"${total:,.0f}")
        if st.button("✅ Finalizar Venta"):
            df_f = leer("facturas.csv")
            nueva_f = pd.DataFrame([[len(df_f)+1, datetime.now().strftime("%Y-%m-%d"), paciente, total, "Varios"]], columns=df_f.columns)
            guardar(pd.concat([df_f, nueva_f]), "facturas.csv")
            st.session_state.carrito = []
            st.success("Venta Guardada")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 8. INVENTARIO ---
elif menu == "📦 Tarifario e Inventario":
    st.title("📦 Inventario y Precios")
    with st.form("inv"):
        it, cat, pre = st.text_input("Item"), st.selectbox("Categoría", ["Servicio", "Medicamento", "Vacuna"]), st.number_input("Precio", min_value=0)
        if st.form_submit_button("Guardar Item"):
            df = leer("inventario.csv")
            guardar(pd.concat([df, pd.DataFrame([[it, cat, pre]], columns=df.columns)]), "inventario.csv")
            st.rerun()
    st.dataframe(leer("inventario.csv"), use_container_width=True)

# --- 9. IMPORTAR DATOS ---
elif menu == "📥 Importar Datos":
    st.title("📥 Sincronización Masiva")
    st.write("Copie y pegue sus datos de OkVet o PDF para cargarlos al sistema de inmediato.")
    target = st.selectbox("Destino", ["propietarios.csv", "mascotas.csv"])
    raw = st.text_area("Datos (Pegar aquí):")
    if st.button("🚀 Cargar"):
        df_new = pd.read_csv(io.StringIO(raw), sep='\t')
        df_old = leer(target)
        guardar(pd.concat([df_old, df_new]).drop_duplicates(), target)
        st.success("Sincronizado")
    
