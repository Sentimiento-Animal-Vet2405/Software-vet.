import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- 1. ESTÉTICA CIELO ELITE ---
st.set_page_config(page_title="Sentimiento Animal Elite", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f0f9ff; }
    [data-testid="stSidebar"] { background-color: #0c4a6e !important; }
    [data-testid="stSidebar"] * { color: #f0f9ff !important; }
    .main-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #bae6fd; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { 
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important; 
        color: white !important; border-radius: 12px; font-weight: 600; border: none; height: 3.5em; width: 100%; transition: 0.4s;
    }
    .ia-card { background-color: #f0fdf4; padding: 15px; border-radius: 12px; border-left: 6px solid #22c55e; color: #166534; font-weight: bold; }
    .hosp-alert { background-color: #fef2f2; border-left: 6px solid #ef4444; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    h1, h2, h3 { color: #0c4a6e !important; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS (20 MÓDULOS) ---
DB_ARCHIVOS = {
    "propietarios.csv": ["Nombre", "Documento", "Telefono", "Correo", "Direccion"],
    "mascotas.csv": ["Mascota", "Especie", "Raza", "Sexo", "Edad", "Peso_Actual", "Estado", "Dueño_Doc"],
    "historias.csv": ["Fecha", "Mascota", "Peso", "S", "O", "I", "P", "Laboratorio", "Tratamiento"],
    "hospital.csv": ["Mascota", "Cama", "Ingreso", "Motivo", "Medicacion_Actual", "Estado"],
    "inventario.csv": ["Item", "Categoría", "Precio", "Stock"],
    "facturas.csv": ["ID", "Fecha", "Mascota", "Total", "Metodo"],
    "agenda.csv": ["Fecha", "Hora", "Paciente", "Motivo"]
}

for f, cols in DB_ARCHIVOS.items():
    if not os.path.exists(f) or os.stat(f).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(f, index=False)

def leer(n): return pd.read_csv(n)
def guardar(df, n): df.to_csv(n, index=False)

# --- 3. BARRA LATERAL MAESTRA ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🏥</h1>", unsafe_allow_html=True)
    st.title("Sentimiento Animal")
    st.write(f"Dra. Camila Mejía")
    st.markdown("---")
    menu = st.radio("MÓDULOS ELITE", [
        "📊 Dashboard General",
        "📥 Importar Datos (OkVet)",
        "👥 Gestión Tutores/Pacientes",
        "🩺 Consulta Médica + IA",
        "🏥 Hospitalización Crítica",
        "📈 Monitor de Peso",
        "🧪 Lab & Diagnóstico",
        "💰 Facturación Pro",
        "📦 Inventario Farmacia",
        "📋 Certificados & Firmas",
        "📅 Agenda de Citas"
    ])

# --- 4. LÓGICA DE MÓDULOS SELECCIONADOS ---

if menu == "📊 Dashboard General":
    st.title("📊 Control de Mando Clínica")
    df_m, df_f, df_h = leer("mascotas.csv"), leer("facturas.csv"), leer("hospital.csv")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pacientes Totales", len(df_m))
    c2.metric("Ventas Mes", f"${df_f['Total'].sum():,.0f}")
    c3.metric("En Hospital", len(df_h))
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("📈 Flujo de Caja")
    if not df_f.empty:
        st.area_chart(df_f.groupby("Fecha")["Total"].sum(), color="#0284c7")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🩺 Consulta Médica + IA":
    st.title("🩺 Estación Médico-Clínica")
    df_m = leer("mascotas.csv")
    if not df_m.empty:
        paciente = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        peso = col1.number_input("Peso Actual (Kg):", step=0.1)
        lab_ref = col2.text_input("Ref. Laboratorio / Imágenes:")
        
        s = st.text_area("S - Subjetivo (Anamnesis)")
        if "vomito" in s.lower() or "sangre" in s.lower():
            st.markdown("<div class='ia-card'>🤖 IA: Alerta. Posible cuadro infeccioso o hemorrágico. Sugerido: Hemograma completo y ecografía abdominal.</div>", unsafe_allow_html=True)
        
        o, i, p = st.text_area("O - Objetivo"), st.text_area("I - Interpretación"), st.text_area("P - Plan Terapéutico")
        
        if st.button("💾 Cerrar Historia Clínica"):
            df_h = leer("historias.csv")
            nueva = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), paciente, peso, s, o, i, p, lab_ref, "Medicamentos prescritos"]], columns=df_h.columns)
            guardar(pd.concat([df_h, nueva]), "historias.csv")
            df_m.loc[df_m['Mascota'] == paciente, 'Peso_Actual'] = peso
            guardar(df_m, "mascotas.csv")
            st.success("Historia guardada y peso actualizado.")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🏥 Hospitalización Crítica":
    st.title("🏥 Panel de Hospitalización")
    df_hosp = leer("hospital.csv")
    
    with st.expander("➕ Ingresar Paciente a Hospitalización"):
        df_m = leer("mascotas.csv")
        pac_h = st.selectbox("Mascota a Hospitalizar:", df_m["Mascota"].tolist())
        cama = st.text_input("Cama/Jaula asignada:")
        mot = st.text_input("Motivo de Ingreso:")
        med = st.text_area("Kardex de Medicación (Dosis/Horarios):")
        if st.button("Confirmar Ingreso a Hospital"):
            nueva_h = pd.DataFrame([[pac_h, cama, datetime.now().strftime("%Y-%m-%d"), mot, med, "Bajo Observación"]], columns=df_hosp.columns)
            guardar(pd.concat([df_hosp, nueva_h]), "hospital.csv")
            st.rerun()

    st.write("### 🐾 Pacientes Internados Actualmente")
    for _, r in df_hosp.iterrows():
        st.markdown(f"""
        <div class='hosp-alert'>
            <h4>{r['Mascota']} - {r['Cama']}</h4>
            <b>Ingreso:</b> {r['Ingreso']} | <b>Motivo:</b> {r['Motivo']}<br>
            <b>💊 Tratamiento:</b> {r['Medicacion_Actual']}<br>
            <b>Estado:</b> {r['Estado']}
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Dar de Alta a {r['Mascota']}", key=r['Mascota']):
            df_hosp = df_hosp[df_hosp["Mascota"] != r['Mascota']]
            guardar(df_hosp, "hospital.csv")
            st.rerun()

elif menu == "📈 Monitor de Peso":
    st.title("📈 Análisis de Evolución de Peso")
    df_h = leer("historias.csv")
    df_m = leer("mascotas.csv")
    pac = st.selectbox("Seleccione Paciente:", df_m["Mascota"].tolist())
    reg = df_h[df_h["Mascota"] == pac].sort_values("Fecha")
    if not reg.empty:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.line_chart(reg.set_index("Fecha")["Peso"], color="#ef4444")
        st.markdown("</div>", unsafe_allow_html=True)
    else: st.info("No hay suficientes registros de peso para generar gráfica.")

elif menu == "💰 Facturación Pro":
    st.title("💰 Facturación y Cierre de Caja")
    df_inv = leer("inventario.csv")
    df_m = leer("mascotas.csv")
    
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        pac = st.selectbox("Mascota:", df_m["Mascota"].tolist() if not df_m.empty else [])
        servicios = st.multiselect("Items a cobrar:", df_inv["Item"].tolist())
        total = df_inv[df_inv["Item"].isin(servicios)]["Precio"].sum()
        st.write(f"### Subtotal: ${total:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        metodo = st.selectbox("Pago:", ["Efectivo", "Transferencia", "Tarjeta"])
        if st.button("✅ Procesar Venta"):
            df_f = leer("facturas.csv")
            nueva_f = pd.DataFrame([[len(df_f)+1, datetime.now().strftime("%Y-%m-%d"), pac, total, metodo]], columns=df_f.columns)
            guardar(pd.concat([df_f, nueva_f]), "facturas.csv")
            st.success("¡Venta Exitosa!")
            st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📦 Inventario Farmacia":
    st.title("📦 Inventario y Precios")
    with st.form("nuevo_i"):
        it, pr, stck = st.text_input("Nombre"), st.number_input("Precio"), st.number_input("Stock")
        if st.form_submit_button("Añadir al Sistema"):
            df = leer("inventario.csv")
            guardar(pd.concat([df, pd.DataFrame([[it, "Medicamento", pr, stck]], columns=df.columns)]), "inventario.csv")
            st.rerun()
    st.dataframe(leer("inventario.csv"), use_container_width=True)

elif menu == "📥 Importar Datos (OkVet)":
    st.title("📥 Sincronización Masiva")
    tipo = st.selectbox("Destino:", ["propietarios.csv", "mascotas.csv"])
    raw = st.text_area("Pegue las columnas de OkVet aquí:", height=200)
    if st.button("🚀 Iniciar Carga"):
        df_new = pd.read_csv(io.StringIO(raw), sep='\t')
        df_old = leer(tipo)
        guardar(pd.concat([df_old, df_new]).drop_duplicates(), tipo)
        st.success("Datos integrados correctamente.")
    
