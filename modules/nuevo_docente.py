import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver a Gestión de Docentes", key="back_to_docs"):
        st.session_state['reg_vista'] = "docentes"
        st.rerun()

    # --- CSS EN ALTA VIBRACIÓN GRÁFICA (Cero palidez) ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen: Azul Eléctrico Intenso */
.summary-box { 
    background: linear-gradient(135deg, #1e40af 0%, #0047ff 100%) !important; 
    border: 2px solid #0036d6; 
    border-radius: 16px; 
    padding: 25px; 
    box-shadow: 0 10px 25px rgba(0, 71, 255, 0.25); 
    position: sticky; 
    top: 20px; 
}
.summary-title { font-size: 1.25rem; font-weight: 900; color: white !important; margin-bottom: 22px; text-transform: uppercase; letter-spacing: 0.5px; }
.summary-item { display: flex; align-items: center; margin-bottom: 18px; background: rgba(255, 255, 255, 0.18); padding: 14px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.25); }

/* Iconos encendidos */
.summary-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; flex-shrink: 0; background: white; }
.summary-details { display: flex; flex-direction: column; }
.summary-lbl { font-size: 0.85rem; color: #dbeafe !important; font-weight: 700; margin-bottom: 2px; }
.summary-val { font-size: 1.05rem; font-weight: 800; color: white !important; }

/* Checklist lateral */
.req-title { font-size: 1.1rem; font-weight: 800; color: white !important; margin-top: 25px; margin-bottom: 14px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.95rem; color: #f8fafc !important; font-weight: 700; }
.check-icon { margin-right: 12px; font-size: 1.1rem; }
.badge-doc { padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; }

/* Botones inferiores */
.btn-guardar button { background-color: #3b82f6 !important; color: white !important; font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 6px rgba(59,130,246,0.3); }
.btn-guardar button:hover { background-color: #2563eb !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

    # --- CONSULTA REAL A LA TABLA ASIGNATURAS (COLUMNA REAL: nombre_materia) ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT nombre_materia FROM asignaturas")
        if db_asig:
            lista_asignaturas = [str(item[0]).strip() for item in db_asig if item[0]]
    except Exception as e:
        st.sidebar.warning(f"Aviso de carga de asignaturas: {e}")
    
    if not lista_asignaturas:
        lista_asignaturas = ["Introducción a la Ingeniería de Software", "Desarrollo de Software I", "Estructuras de Datos y Algoritmos"]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo docente evaluador</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Completa los campos del formulario mapeados con la estructura de la base de datos.</div>', unsafe_allow_html=True)

    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS DE IDENTIDAD (Mapeado a campos reales de profesores) ---
        st.markdown('<div class="form-section-title">1. Datos de identidad</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            # Campo Real BD: nombre_completo
            nombre_completo = st.text_input("Nombre completo del docente *", placeholder="Ej. María Fernanda López Gómez")
        with g_col2:
            # Programa por defecto: Ingeniería de Software
            programa = st.selectbox("Programa / Área *", ["Ingeniería de Software", "Ingeniería de Sistemas", "Administración de Empresas"])

        # --- 2. ASIGNACIÓN ACADÉMICA (Mapeado a horas_dedicacion y asignaturas) ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            asig_seleccionadas = st.multiselect("Asignaturas RAP a dictar *", options=lista_asignaturas, placeholder="Selecciona los cursos")
        with a_col2:
            # Campo Real BD: horas_dedicacion
            horas_dedicacion = st.number_input("Horas de dedicación asignadas *", min_value=0, max_value=100, value=4, step=1)

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Notas del proceso</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Observaciones adicionales", max_chars=500, placeholder="Anotaciones de soporte académico...")

        # --- ACCIONES ---
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1, 0.8, 2])
        with b_col1:
            st.markdown('<div class="btn-guardar">', unsafe_allow_html=True)
            btn_save = st.button("📥 Guardar docente", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="btn-cancelar">', unsafe_allow_html=True)
            if st.button("Cancelar", use_container_width=True):
                st.session_state['reg_vista'] = "docentes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col3:
            st.markdown('<p style="margin-top:12px;"><a href="#" style="color:#3b82f6; font-weight:700; text-decoration:none;">Guardar y crear otro</a></p>', unsafe_allow_html=True)

        if btn_save:
            if nombre_completo and asig_seleccionadas:
                st.success(f"🎉 ¡Docente '{nombre_completo}' listo con {horas_dedicacion} hrs de dedicación!")
            else:
                st.error("❌ Por favor completa los campos requeridos (*)")

    # --- BARRA LATERAL EN VIVO (CERO SANGRIAS PARA DESPLEGAR EL HTML) ---
    with col_sum:
        # Concatenación directa sin espacios al inicio de cada línea para el motor Markdown
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">💻</div><div class="summary-details"><span class="summary-lbl">Programa académico</span><span class="summary-val">{programa}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas de la BD</span><span class="summary-val">{len(asig_seleccionadas)} seleccionadas</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">🕒</div><div class="summary-details"><span class="summary-lbl">Horas dedicación</span><span class="summary-val">{horas_dedicacion} horas</span></div></div>'
        html_sum_box += '<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin:20px 0;">'
        html_sum_box += '<div class="req-title">Estatus de campos obligatorios</div>'
        
        c_nom = '#10b981' if nombre_completo else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre_completo else "○"}</span> nombre_completo</div>'
        
        c_asig = '#10b981' if asig_seleccionadas else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> asignaturas reales</div>'
        
        html_sum_box += '<div class="checklist-item"><span class="check-icon" style="color:#10b981;">●</span> horas_dedicacion</div>'
        html_sum_box += '</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)