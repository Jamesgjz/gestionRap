from html import escape

import streamlit as st
from database import DatabaseError, ejecutar_query, traer_datos
from modules.programas_datos import listar_programas, preparar_esquema

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver a Gestión de Docentes", key="back_to_docs"):
        st.session_state['reg_vista'] = "docentes"
        st.rerun()

    if not preparar_esquema():
        return

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

    version = st.session_state.setdefault("form_version", 0)
    programas = [nombre for _, nombre in listar_programas()]
    rows = traer_datos("SELECT DISTINCT nombre_materia FROM asignaturas ORDER BY nombre_materia")
    lista_asignaturas = [nombre.strip() for (nombre,) in rows if nombre]
    if not lista_asignaturas:
        st.warning("No hay asignaturas disponibles en el catálogo.")

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
            nombre_completo = st.text_input("Nombre completo del docente *", placeholder="Ej. María Fernanda López Gómez", key=f"teacher_nombre_completo_{version}")
        with g_col2:
            if programas:
                programa = st.selectbox("Programa / Área *", programas, key=f"teacher_programa_{version}")
            else:
                programa = st.text_input("Programa / Área *", max_chars=120, key=f"teacher_programa_{version}")

        # --- 2. ASIGNACIÓN ACADÉMICA (Mapeado a horas_dedicacion y asignaturas) ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            asig_seleccionadas = st.multiselect("Asignaturas RAP a dictar *", options=lista_asignaturas, placeholder="Selecciona los cursos", key=f"teacher_asig_seleccionadas_{version}")
        with a_col2:
            # Campo Real BD: horas_dedicacion
            horas_dedicacion = st.number_input("Horas de dedicación asignadas *", min_value=0, max_value=100, value=4, step=1, key=f"teacher_horas_dedicacion_{version}")

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Notas del proceso</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Observaciones adicionales", max_chars=500, placeholder="Anotaciones de soporte académico...", key=f"teacher_observaciones_{version}")

        # --- ACCIONES ---
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1, 0.8, 2])
        with b_col1:
            st.markdown('<div class="btn-guardar">', unsafe_allow_html=True)
            btn_save = st.button("📥 Guardar docente", width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="btn-cancelar">', unsafe_allow_html=True)
            if st.button("Cancelar", width="stretch"):
                st.session_state['reg_vista'] = "docentes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col3:
            btn_another = st.button("Guardar y crear otro", width="stretch")

        if btn_save or btn_another:
            if not nombre_completo.strip() or not programa.strip() or not asig_seleccionadas:
                st.warning("Completa los campos obligatorios.")
            else:
                try:
                    ejecutar_query(
                        """INSERT INTO profesores (nombre_completo, programa, asignaturas, horas_dedicacion, observaciones)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (nombre_completo.strip(), programa.strip(), ", ".join(asig_seleccionadas),
                         horas_dedicacion, observaciones.strip()),
                    )
                except DatabaseError:
                    st.error("No se pudo guardar el docente. Revisa los datos e intenta de nuevo.")
                else:
                    st.session_state["registro_guardado"] = "Se guardó el docente."
                    if btn_another:
                        st.session_state["form_version"] += 1
                    else:
                        st.session_state["reg_vista"] = "docentes"
                    st.rerun()

    # --- BARRA LATERAL EN VIVO (CERO SANGRIAS PARA DESPLEGAR EL HTML) ---
    with col_sum:
        # Concatenación directa sin espacios al inicio de cada línea para el motor Markdown
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">💻</div><div class="summary-details"><span class="summary-lbl">Programa académico</span><span class="summary-val">{escape(programa)}</span></div></div>'
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