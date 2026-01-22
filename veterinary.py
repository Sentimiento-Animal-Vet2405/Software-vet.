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
    .hosp-card { background: #fee2e2; border-left: 8px solid #ef4444; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { background: #0284c7; color: white !important; border-radius: 12px; font-weight: 700; height: 3rem; border: none; }
    .stTabs [aria-selected="true"] { background-color: #0284c7 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE BASES DE DATOS ---
DB_FILES = {
    "propietarios": ["Nombre", "Tipo_Doc", "Numero", "Teléfono", "Correo", "Dirección"],
    "mascotas": ["ID_Prop", "Nombre_Mascota", "Especie", "Raza", "Sexo", "Color", "Peso_kg", "Nacimiento"],
    "historias": ["Fecha", "ID_Prop", "Mascota", "S", "O", "I", "P", "Vacunas", "Lab", "Hosp"],
    "hospitalizados": ["Paciente", "Propietario", "Estado", "Motivo", "Ingreso"]
}

for db, cols in DB_FILES.items():
    if not os.path.exists(f"{db}.csv"):
        pd.DataFrame(columns=cols).to_csv(f"{db}.csv", index=False)

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>Sentimiento Animal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Dra. Camila Mejía</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENÚ PRINCIPAL", ["🏠 Dashboard", "👥 Clientes", "🐾 Pacientes", "🩺 Consulta Integral", "📥 Importar OkVet", "💾 Reportes"])

# --- 1. DASHBOARD CON BUSCADOR ---
if menu == "🏠 Dashboard":
    st.title("🏠 Panel de Control")
    df_p = pd.read_csv("propietarios.csv")
    df_m = pd.read_csv("mascotas.csv")
    df_hosp = pd.read_csv("hospitalizados.csv")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes", len(df_p))
    col2.metric("Pacientes", len(df_m))
    col3.metric("Internados", len(df_hosp))

    st.subheader("🔍 Buscador Rápido de Pacientes")
    search_query = st.text_input("Escriba el nombre de la mascota o el documento del dueño...")
    
    if search_query:
        # Búsqueda en mascotas y dueños
        res_m = df_m[df_m['Nombre_Mascota'].str.contains(search_query, case=False, na=False)]
        res_p = df_p[df_p['Numero'].astype(str).str.contains(search_query, na=False)]
        
        if not res_m.empty:
            st.write("Mascotas encontradas:")
            st.dataframe(res_m)
        elif not res_p.empty:
            st.write("Dueño encontrado. Sus mascotas son:")
            id_buscado = res_p.iloc[0]['Numero']
            st.dataframe(df_m[df_m['ID_Prop'].astype(str) == str(id_buscado)])
        else:
            st.warning("No se encontraron resultados.")

    st.subheader("🚨 Pacientes en Hospitalización")
    if not df_hosp.empty:
        for i, row in df_hosp.iterrows():
            st.markdown(f"<div class='hosp-card'><b>🐶 {row['Paciente']}</b> | {row['Estado']}<br><small>Ingreso: {row['Ingreso']} - Motivo: {row['Motivo']}</small></div>", unsafe_allow_html=True)
            if st.button(f"Dar de Alta a {row['Paciente']}", key=f"alta_{i}"):
                df_hosp.drop(i).to_csv("hospitalizados.csv", index=False)
                st.rerun()

# --- 2. CLIENTES ---
elif menu == "👥 Clientes":
    st.title("👥 Gestión de Clientes")
    with st.form("f_cli", clear_on_submit=True):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nombre Completo")
        num = c2.text_input("Número de Identificación (Cédula/NIT)")
        tel = c1.text_input("WhatsApp (Ej: 3001234567)")
        cor = c2.text_input("Correo Electrónico")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("Guardar Propietario"):
            df = pd.read_csv("propietarios.csv")
            pd.concat([df, pd.DataFrame([{"Nombre":nom, "Numero":num, "Teléfono":tel, "Correo":cor}])]).to_csv("propietarios.csv", index=False)
            st.success("Cliente guardado exitosamente.")

# --- 3. PACIENTES ---
elif menu == "🐾 Pacientes":
    st.title("🐾 Registro de Pacientes")
    df_p = pd.read_csv("propietarios.csv")
    if not df_p.empty:
        prop_sel = st.selectbox("Vincular a Propietario:", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_dueño = prop_sel.split("(")[-1].replace(")","")
        with st.form("f_mas"):
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            n_m = c1.text_input("Nombre del Paciente")
            esp = c2.selectbox("Especie", ["Canino", "Felino", "Ave", "Reptil", "Roedor", "Exótico"])
            raz = c1.text_input("Raza")
            sex = c2.selectbox("Sexo", ["Macho", "Hembra", "M. Castrado", "H. Esterilizada"])
            st.markdown("</div>", unsafe_allow_html=True)
            if st.form_submit_button("Registrar Paciente"):
                df_m = pd.read_csv("mascotas.csv")
                pd.concat([df_m, pd.DataFrame([{"ID_Prop":id_dueño, "Nombre_Mascota":n_m, "Especie":esp, "Raza":raz, "Sexo":sex}])]).to_csv("mascotas.csv", index=False)
                st.success("Mascota registrada y vinculada.")
    else:
        st.warning("Primero registre a un propietario.")

# --- 4. CONSULTA INTEGRAL (SOIP, VACUNAS, LABORATORIO) ---
elif menu == "🩺 Consulta Integral":
    st.title("🩺 Estación Médica Clínica")
    df_p, df_m = pd.read_csv("propietarios.csv"), pd.read_csv("mascotas.csv")
    if not df_m.empty:
        c1, c2 = st.columns(2)
        p_sel = c1.selectbox("Dueño", df_p["Nombre"] + " (" + df_p["Numero"].astype(str) + ")")
        id_d = p_sel.split("(")[-1].replace(")","")
        m_sel = c2.selectbox("Paciente", df_m[df_m["ID_Prop"].astype(str) == str(id_d)]["Nombre_Mascota"].tolist())
        
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Historia SOIP", "💉 Plan Sanitario", "🧪 Ayudas Diagnósticas", "🏥 Hospitalización"])
        
        with tab1:
            s = st.text_area("S - Subjetivo (Lo que el dueño cuenta)")
            o = st.text_area("O - Objetivo (Examen físico / Signos)")
            i = st.text_area("I - Interpretación (Diagnóstico presuntivo)")
            p = st.text_area("P - Plan Médico (Tratamiento)")
        with tab2:
            vac = st.text_input("Vacuna aplicada hoy")
            desp = st.text_input("Desparasitante aplicado")
        with tab3:
            labs = st.text_area("Laboratorios Solicitados")
            remi = st.text_area("Motivo de Remisión a Especialista")
        with tab4:
            es_hosp = st.checkbox("¿El paciente requiere hospitalización?")
            h_est = st.selectbox("Estado inicial", ["Estable", "Reservado", "Crítico", "Urgencia"])
            h_mot = st.text_area("Notas de evolución / Motivo de ingreso")

        if st.button("💾 GUARDAR CONSULTA COMPLETA"):
            df_h = pd.read_csv("historias.csv")
            h_data = {"Fecha":date.today(), "ID_Prop":id_d, "Mascota":m_sel, "S":s, "O":o, "I":i, "P":p, "Vacunas":vac, "Lab":labs, "Hosp":es_hosp}
            pd.concat([df_h, pd.DataFrame([h_data])]).to_csv("historias.csv", index=False)
            
            if es_hosp:
                df_hos = pd.read_csv("hospitalizados.csv")
                pd.concat([df_hos, pd.DataFrame([{"Paciente":m_sel, "Propietario":p_sel, "Estado":h_est, "Motivo":h_mot, "Ingreso":date.today()}])]).to_csv("hospitalizados.csv", index=False)
            
            st.balloons()
            st.success(f"¡Historia de {m_sel} guardada con éxito!")

# --- 5. IMPORTAR DATOS OKVET ---
elif menu == "📥 Importar OkVet":
    st.title("📥 Migración Maestra de Datos")
    st.info("Utilice esta herramienta para cargar sus bases de datos antiguas de OkVet.")
    target = st.radio("¿Qué base de datos va a importar?", ["propietarios", "mascotas"])
    up_f = st.file_uploader("Cargue su archivo Excel o CSV", type=["xlsx", "csv"])
    if up_f:
        try:
            df_new = pd.read_excel(up_f) if up_f.name.endswith('xlsx') else pd.read_csv(up_f)
            st.write("Vista previa de sus datos:")
            st.dataframe(df_new.head())
            if st.button("🚀 Iniciar Importación"):
                df_new.to_csv(f"{target}.csv", index=False)
                st.success("Base de datos actualizada con la información de OkVet.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

# --- 6. REPORTES Y COPIAS ---
elif menu == "💾 Reportes":
    st.title("💾 Centro de Reportes")
    df_h = pd.read_csv("historias.csv")
    if not df_h.empty:
        h_idx = st.selectbox("Seleccione consulta para generar reporte:", df_h.index, format_func=lambda x: f"{df_h.iloc[x]['Mascota']} - {df_h.iloc[x]['Fecha']}")
        data = df_h.iloc[h_idx]
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.write(f"### Reporte de Consulta: {data['Mascota']}")
        st.write(f"**Fecha:** {data['Fecha']}")
        st.write(f"**Tratamiento:** {data['P']}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No hay historias clínicas registradas para generar reportes.")
                
