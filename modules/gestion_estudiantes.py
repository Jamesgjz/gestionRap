import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD Y MÁXIMA VIBRACIÓN (Mockup image_366ec6.jpg) ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }

/* Títulos de sección */
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen: Azul Eléctrico Premium Sincronizado */
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

.summary-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; flex-shrink: 0; background: white; }
.summary-details { display: flex; flex-direction: column; }
.summary-lbl { font-size: 0.85rem; color: #dbeafe !important; font-weight: 700; margin-bottom: 2px; }
.summary-val { font-size: 1.05rem; font-weight: 800; color: white !important; }

/* Checklist lateral de validación */
.req-title { font-size: 1.1rem; font-weight: 800; color: white !important; margin-top: 25px; margin-bottom: 14px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.95rem; color: #f8fafc !important; font-weight: 700; }
.check-icon { margin-right: 12px; font-size: 1.1rem; }
.badge-est { padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; background-color: #10b981; color: white; }

/* Botonera inferior corporativa */
.btn-guardar button { background-color: #0047ff !important; color: white !important; font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,71,255,0.2); }
.btn-guardar button:hover { background-color: #0036d6 !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN DE CURSOS DESDE LA BD (nombre_materia) ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT nombre_materia FROM asignaturas")
        if db_asig:
            lista_asignaturas = [str(item[0]).strip() for item in db_asig if item[0]]
    except Exception as e:
        st.sidebar.warning(f"Aviso de carga en Estudiantes: {e}")
    
    if not lista_asignaturas:
        lista_asignaturas = ["Introducción a la Ingeniería de Software", "Desarrollo de Software I", "Estructuras de Datos y Algoritmos", "Análisis y Diseño de Sistemas"]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo estudiante</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Completa la información para registrar un nuevo estudiante en el proceso RAP.</div>', unsafe_allow_html=True)

    # Grid de dos columnas
    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES ---
        st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            id_banner = st.text_input("ID Banner *", placeholder="Ej. 90012345")
            documento = st.text_input("Documento *", placeholder="Ej. 1.234.567.890")
            programa_acad = st.selectbox("Programa académico *", ["Ingeniería de Software", "Ingeniería de Sistemas", "Administración de Empresas"])
        with g_col2:
            nombre_completo = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
            correo = st.text_input("Correo institucional *", placeholder="Ej. maria.lopez@uniminuto.edu.co")
            
            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                periodo = st.selectbox("Periodo *", ["202610", "202620", "202630"])
            with sub_c2:
                estado = st.selectbox("Estado *", ["Matriculado", "Inscrito", "Graduado"])

        # --- 2. ASIGNACIÓN ACADÉMICA ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            # Multi-select alimentado de la base de datos
            asig_seleccionadas = st.multiselect("Asignaturas RAP *", options=lista_asignaturas, placeholder="Selecciona las asignaturas")
        with a_col2:
            modalidad = st.selectbox("Modalidad *", ["Virtual", "Presencial", "Híbrida"])

        # Control Switch e Info del Mockup
        st.markdown("<br>", unsafe_allow_html=True)
        st.toggle("Corrección de ID Banner", key="id_banner_toggle", help="Active esta casilla únicamente si requiere corregir un ID Banner previamente indexado.")

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Observaciones</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Observaciones adicionales", max_chars=500, placeholder="Ej. Información adicional relevante sobre el estudiante, apoyos requeridos, novedades, etc.")

        # --- BOTONERA ---
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1, 0.8, 2])
        with b_col1:
            st.markdown('<div class="btn-guardar">', unsafe_allow_html=True)
            btn_save = st.button("📥 Guardar estudiante", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="btn-cancelar">', unsafe_allow_html=True)
            if st.button("Cancelar", use_container_width=True):
                st.session_state['reg_vista'] = "dashboard"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col3:
            st.markdown('<p style="margin-top:12px;"><a href="#" style="color:#3b82f6; font-weight:700; text-decoration:none;">Guardar y crear otro</a></p>', unsafe_allow_html=True)

        if btn_save:
            if nombre_completo and id_banner and documento and asig_seleccionadas:
                st.success(f"🎉 ¡Estudiante '{nombre_completo}' procesado de forma correcta para almacenamiento!")
            else:
                st.error("❌ Diligencie todos los campos de carácter obligatorio (*)")

    # --- BARRA LATERAL ULTRA-VIBRANTE (Cero sangrías de margen izquierdo) ---
    with col_sum:
        # Construcción lineal continua para blindar el motor Markdown de Streamlit
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">🎓</div><div class="summary-details"><span class="summary-lbl">Programa académico</span><span class="summary-val">{programa_acad}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">✓</div><div class="summary-details"><span class="summary-lbl">Estado</span><span><b class="badge-est">{estado}</b></span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas seleccionadas</span><span class="summary-val">{len(asig_seleccionadas)} seleccionadas</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">📅</div><div class="summary-details"><span class="summary-lbl">Periodo</span><span class="summary-val">{periodo}</span></div></div>'
        
        html_sum_box += '<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin:20px 0;">'
        html_sum_box += '<div class="req-title">Datos requeridos</div>'
        
        c_nom = '#10b981' if nombre_completo else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre_completo else "○"}</span> Nombre completo</div>'
        
        c_ban = '#10b981' if id_banner else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_ban};">{"●" if id_banner else "○"}</span> ID Banner</div>'
        
        c_doc = '#10b981' if documento else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_doc};">{"●" if documento else "○"}</span> Documento</div>'
        
        c_cor = '#10b981' if '@' in correo else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_cor};">{"●" if "@" in correo else "○"}</span> Correo institucional</div>'
        
        html_sum_box += '<div class="checklist-item"><span class="check-icon" style="color:#10b981;">●</span> Programa académico</div>'
        
        c_asig = '#10b981' if asig_seleccionadas else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> Asignaturas RAP</div>'
        
        html_sum_box += '</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)