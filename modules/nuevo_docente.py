import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver a Gestión de Docentes", key="back_to_docs"):
        st.session_state['reg_vista'] = "docentes"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD CON COLORES VIVOS Y REFORZADOS ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }

/* Títulos de sección */
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen con Color e Identidad Reforzada */
.summary-box { 
    background: #f8fafc; 
    border: 2px solid #cbd5e1; 
    border-radius: 16px; 
    padding: 25px; 
    box-shadow: 0 4px 12px rgba(15,23,42,0.05); 
    position: sticky; 
    top: 20px; 
}
.summary-title { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-bottom: 22px; text-transform: uppercase; letter-spacing: 0.5px; }
.summary-item { display: flex; align-items: center; margin-bottom: 18px; background: white; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; }

/* Iconos con fondos vivos y de alta saturación gráfica */
.summary-icon { width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-right: 14px; flex-shrink: 0; }
.summary-details { display: flex; flex-direction: column; }
.summary-lbl { font-size: 0.8rem; color: #475569; font-weight: 700; margin-bottom: 2px; }
.summary-val { font-size: 1rem; font-weight: 800; color: #0f172a; }

/* Checklist de requeridos */
.req-title { font-size: 1rem; font-weight: 800; color: #0f172a; margin-top: 25px; margin-bottom: 14px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.95rem; color: #1e293b; font-weight: 600; }
.check-icon { margin-right: 12px; font-size: 1.1rem; }

/* Badges estilizados */
.badge-doc { padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; }

/* Botones de acción */
.btn-guardar button { background-color: #0047ff !important; color: white !important; font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,47,255,0.15); }
.btn-guardar button:hover { background-color: #0036d6 !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

    # --- CONSULTA DE ASIGNATURAS ALMACENADAS ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT nombre FROM asignaturas")
        if db_asig:
            lista_asignaturas = [str(item[0]) for item in db_asig]
    except Exception as e:
        st.sidebar.warning(f"Aviso de asignaturas: {e}")
    
    if not lista_asignaturas:
        lista_asignaturas = ["Lógica Matemática", "Algoritmos", "Pensamiento Crítico", "Matemáticas I", "Estadística", "Contabilidad General"]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo docente evaluador</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Completa la información para registrar a un nuevo docente que participará en el proceso RAP.</div>', unsafe_allow_html=True)

    # Grid principal del formulario
    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES ---
        st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            nombre = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
            documento = st.text_input("Documento *", placeholder="Ej. 1.234.567.890")
            # Ajuste de programa: Ingeniería de Software como opción inicial predeterminada
            programa = st.selectbox("Programa / Área *", ["Ingeniería de Software", "Ingeniería de Sistemas", "Administración de Empresas", "Contaduría Pública", "Psicología", "Derecho"])
        with g_col2:
            correo = st.text_input("Correo institucional *", placeholder="Ej. maria.lopez@uniminuto.edu.co")
            telefono = st.text_input("Teléfono *", placeholder="Ej. 300 123 4567")
            estado = st.selectbox("Estado *", ["Activo", "En revisión", "Sin asignación", "Inactivo"])

        # --- 2. ASIGNACIÓN ACADÉMICA ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            asig_seleccionadas = st.multiselect("Asignaturas RAP *", options=lista_asignaturas, placeholder="Selecciona las asignaturas")
            perfil = st.selectbox("Perfil / rol *", ["Docente evaluador", "Docente constructor", "Coordinador RAP"])
        with a_col2:
            horas = st.number_input("Horas asignadas *", min_value=0, max_value=100, value=12, step=1)
            modalidad = st.selectbox("Modalidad de participación *", ["Virtual", "Presencial", "Híbrida"])

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Observaciones</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Observaciones adicionales", max_chars=500, placeholder="Ej. Información adicional relevante sobre el docente, disponibilidad, observaciones, etc.")
        st.markdown(f'<p style="text-align:right; color:#64748b; font-size:0.85rem; margin-top:-10px;">{len(observaciones)}/500</p>', unsafe_allow_html=True)

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
            if nombre and correo and documento:
                st.success(f"🎉 ¡Docente {nombre} estructurado para guardado con éxito!")
            else:
                st.error("❌ Completa los campos obligatorios marcados con (*)")

    # --- BARRA LATERAL DERECHA (RENDERIZADO LIGADO AL MARGEN IZQUIERDO SIN SANGRIAS) ---
    with col_sum:
        badge_style = "background-color: #10b981; color: white;" if estado == "Activo" else "background-color: #f59e0b; color: white;"
        
        # Construcción directa en una sola línea por bloque para blindar el Markdown de Streamlit
        html_sum_box = f'<div class="summary-box">'
        html_sum_box += f'<div class="summary-title">Resumen de registro</div>'
        
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#dbeafe; color:#2563eb;">💼</div><div class="summary-details"><span class="summary-lbl">Programa / Área</span><span class="summary-val">{programa}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#d1fae5; color:#059669;">✓</div><div class="summary-details"><span class="summary-lbl">Estado</span><span><b class="badge-doc" style="{badge_style}">{estado}</b></span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#f3e8ff; color:#7c3aed;">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas seleccionadas</span><span class="summary-val">{len(asig_seleccionadas)}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon" style="background:#fef3c7; color:#d97706;">🕒</div><div class="summary-details"><span class="summary-lbl">Horas asignadas</span><span class="summary-val">{horas} horas</span></div></div>'
        
        html_sum_box += f'<hr style="border:0; border-top:2px solid #cbd5e1; margin:20px 0;">'
        html_sum_box += f'<div class="req-title">Datos requeridos</div>'
        
        c_nom = '#00875a' if nombre else '#94a3b8'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre else "○"}</span> Nombre completo</div>'
        
        c_cor = '#00875a' if '@' in correo else '#94a3b8'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_cor};">{"●" if "@" in correo else "○"}</span> Correo institucional</div>'
        
        c_doc = '#00875a' if documento else '#94a3b8'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_doc};">{"●" if documento else "○"}</span> Documento</div>'
        
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:#00875a;">●</span> Programa / Área</div>'
        
        c_asig = '#00875a' if asig_seleccionadas else '#94a3b8'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> Asignaturas RAP</div>'
        
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:#00875a;">●</span> Horas asignadas</div>'
        html_sum_box += f'</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)