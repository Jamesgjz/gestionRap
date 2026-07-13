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

/* Títulos de sección */
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen: Azul Eléctrico de Alta Densidad (Adiós Palidez) */
.summary-box { 
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
    border: 2px solid #2563eb; 
    border-radius: 16px; 
    padding: 25px; 
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1); 
    position: sticky; 
    top: 20px; 
}
.summary-title { font-size: 1.25rem; font-weight: 900; color: #1e3a8a; margin-bottom: 22px; text-transform: uppercase; letter-spacing: 0.5px; }
.summary-item { display: flex; align-items: center; margin-bottom: 18px; background: white; padding: 14px; border-radius: 12px; border: 1px solid #bfdbfe; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }

/* Iconos super encendidos */
.summary-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; flex-shrink: 0; }
.summary-details { display: flex; flex-direction: column; }
.summary-lbl { font-size: 0.85rem; color: #1e40af; font-weight: 700; margin-bottom: 2px; }
.summary-val { font-size: 1.05rem; font-weight: 800; color: #0f172a; }

/* Checklist lateral */
.req-title { font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin-top: 25px; margin-bottom: 14px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.95rem; color: #1e293b; font-weight: 700; }
.check-icon { margin-right: 12px; font-size: 1.1rem; }

.badge-doc { padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; }

/* Botones inferiores */
.btn-guardar button { background-color: #0047ff !important; color: white !important; font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,47,255,0.15); }
.btn-guardar button:hover { background-color: #0036d6 !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

    # --- CONSULTA REAL A LA TABLA ASIGNATURAS (COLUMNA: nombre_materia) ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT nombre_materia FROM asignaturas")
        if db_asig:
            # Limpieza y desempaquetado plano de los cursos de la BD
            lista_asignaturas = [str(item[0]).strip() for item in db_asig if item[0]]
    except Exception as e:
        st.sidebar.warning(f"Aviso de carga de asignaturas: {e}")
    
    # Fallback exacto con los nombres reales de tu tabla por si acaso
    if not lista_asignaturas:
        lista_asignaturas = [
            "Introducción a la Ingeniería de Software",
            "Desarrollo de Software I",
            "Estructuras de Datos y Algoritmos",
            "Análisis y Diseño de Sistemas",
            "Sistemas de Gestión de Bases de Datos",
            "Ingeniería de Software I",
            "Desarrollo de Software II",
            "Pruebas de Software"
        ]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo docente evaluador</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Completa la información para registrar a un nuevo docente que participará en el proceso RAP.</div>', unsafe_allow_html=True)

    # Distribución en dos columnas
    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES (Campos reales mapeados a Profesores) ---
        st.markdown('<div class="form-section-title">1. Datos de identidad</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            # Campo Real de la BD: nombre_completo
            nombre_completo = st.text_input("Nombre completo del docente *", placeholder="Ej. María Fernanda López Gómez")
            programa = st.selectbox("Programa / Área *", ["Ingeniería de Software", "Ingeniería de Sistemas", "Administración de Empresas"])
        with g_col2:
            documento_id = st.text_input("Documento de identidad *", placeholder="Ej. 1.234.567.890")
            estado = st.selectbox("Estado inicial *", ["Activo", "En revisión", "Inactivo"])

        # --- 2. ASIGNACIÓN ACADÉMICA (Horas dedicación + Cursos Reales) ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            # Selector múltiple alimentado directamente con los cursos de tu tabla 'asignaturas'
            asig_seleccionadas = st.multiselect("Asignaturas RAP a dictar *", options=lista_asignaturas, placeholder="Selecciona los cursos")
        with a_col2:
            # Campo Real de la BD: horas_dedicacion
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
            st.markdown('<p style="margin-top:12px;"><a href="#" style="color:#0047ff; font-weight:700; text-decoration:none;">Guardar y crear otro</a></p>', unsafe_allow_html=True)

        if btn_save:
            if nombre_completo and documento_id and asig_seleccionadas:
                st.success(f"🎉 ¡Docente '{nombre_completo}' listo para impactar con {horas_dedicacion} hrs de dedicación!")
                # Aquí estructurarías tu consulta real usando los campos mapeados exactos:
                # INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s, %s)
            else:
                st.error("❌ Por favor completa los campos requeridos marcados con (*)")

    # --- BARRA LATERAL EN VIVO (CERO SANGRIAS PARA RENDERIZADO IMPECABLE) ---
    with col_sum:
        badge_style = "background-color: #10b981; color: white;" if estado == "Activo" else "background-color: #f59e0b; color: white;"
        
        # Concatenación ligada al extremo izquierdo sin tabulaciones para el motor Markdown
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#2563eb; color:white;">💼</div><div class="summary-details"><span class="summary-lbl">Programa académico</span><span class="summary-val">{programa}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#059669; color:white;">✓</div><div class="summary-details"><span class="summary-lbl">Estado asignado</span><span><b class="badge-doc" style="{badge_style}">{estado}</b></span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#7c3aed; color:white;">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas de la BD</span><span class="summary-val">{len(asig_seleccionadas)} seleccionadas</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#d97706; color:white;">🕒</div><div class="summary-details"><span class="summary-lbl">Horas Dedicación</span><span class="summary-val">{horas_dedicacion} horas</span></div></div>'
        
        html_sum_box += '<hr style="border:0; border-top:2px solid #2563eb; opacity:0.2; margin:20px 0;">'
        html_sum_box += '<div class="req-title">Estatus de campos obligatorios</div>'
        
        c_nom = '#00875a' if nombre_completo else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre_completo else "○"}</span> Nombre completo</div>'
        
        c_doc = '#00875a' if documento_id else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_doc};">{"●" if documento_id else "○"}</span> Documento</div>'
        
        c_asig = '#00875a' if asig_seleccionadas else '#ef4444'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> Cursos seleccionados</div>'
        
        html_sum_box += '<div class="checklist-item"><span class="check-icon" style="color:#00875a;">●</span> Horas dedicas (Mapeado)</div>'
        html_sum_box += '</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)