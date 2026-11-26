from html import escape

import streamlit as st
from errors import DatabaseError
from modules.participantes_datos import guardar_participantes, preparar_participante
from modules.programas_datos import catalogo_asignaturas, preparar_esquema, selector_programa
from rutas import enlace, ir_a


def render():
    enlace("registro", label="← Volver al Panel Principal")

    if not preparar_esquema():
        return

    # --- CSS DE ALTA INTENSIDAD GRÁFICA EN AZULES CORPORATIVOS ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen: Azul Eléctrico Institucional */
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

/* Checklist lateral */
.req-title { font-size: 1.1rem; font-weight: 800; color: white !important; margin-top: 25px; margin-bottom: 14px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.95rem; color: #f8fafc !important; font-weight: 700; }
.check-icon { margin-right: 12px; font-size: 1.1rem; }
.badge-est { padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; }

/* Botones inferiores con el Azul Claro Digital */
.btn-guardar button { background-color: #3b82f6 !important; color: white !important; font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 6px rgba(59,130,246,0.2); }
.btn-guardar button:hover { background-color: #2563eb !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f1f5f9 !important; }

/* =========================================================================
   BLINDAJE DE ALTA ESPECIFICIDAD ANTI-ROJO PARA MULTISELECT
   ========================================================================= */
/* Intercepta y cambia de forma agresiva cualquier pastilla seleccionada dentro del multiselect */
.stMultiSelect div[data-baseweb="tag"],
.stMultiSelect span[data-baseweb="tag"],
div[data-testid="stMultiSelect"] span,
div[data-baseweb="tag"] {
    background-color: #3b82f6 !important; /* Fuerza el azul digital de registro */
    background: #3b82f6 !important;
    color: white !important;
}

/* Fuerza el color del texto y del icono de cerrar dentro de las pastillas */
div[data-baseweb="tag"] span,
div[data-baseweb="tag"] svg {
    color: white !important;
    fill: white !important;
}

/* Fuerza el color azul del borde interactivo del input al hacer foco */
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"]:focus-within,
.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

    version = st.session_state.setdefault("form_version", 0)
    st.markdown('<div class="form-title">Nuevo participante</div>', unsafe_allow_html=True)
    programa_id = selector_programa(key=f"student_programa_{version}")
    catalogo = {codigo: nombre or codigo for codigo, nombre in catalogo_asignaturas(programa_id)}
    if not catalogo:
        st.warning("No hay asignaturas vinculadas. Revisa el catálogo del programa.")

    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES ---
        st.markdown('<div class="form-section-title">1. Datos generales de matrícula</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            id_banner = st.text_input("ID Banner (*id_banner) *", placeholder="Ej. 90012345", key=f"student_id_banner_{version}")
            estado_matriz = st.selectbox("Estado de matrícula (*estado_matriz) *", ["Matriculado", "No matriculado"], key=f"student_estado_matriz_{version}")
        with g_col2:
            nombre_completo = st.text_input("Nombre completo del participante *", placeholder="Ej. Alba Lucía Pinzón Gallego", key=f"student_nombre_completo_{version}")

        # --- 2. VINCULACIÓN CURRICULAR ---
        st.markdown('<div class="form-section-title">2. Vinculación curricular</div>', unsafe_allow_html=True)
        asig_seleccionadas = st.multiselect("Asignaturas RAP (*alfa_asignatura) *", options=list(catalogo), format_func=lambda codigo: f"{codigo} - {catalogo[codigo]}", placeholder="Selecciona los códigos alfanuméricos", key=f"student_asig_seleccionadas_{version}_{programa_id}")

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Observaciones del participante</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Notas adicionales (*observaciones)", max_chars=500, placeholder="Escribe apoyos requeridos o novedades académicas...", key=f"student_observaciones_{version}")

        # --- BOTONERA DE ACCIÓN ---
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1, 0.8, 2])
        with b_col1:
            st.markdown('<div class="btn-guardar">', unsafe_allow_html=True)
            btn_save = st.button("📥 Guardar participante", width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="btn-cancelar">', unsafe_allow_html=True)
            if st.button("Cancelar", width="stretch"):
                ir_a("registro")
            st.markdown('</div>', unsafe_allow_html=True)
        with b_col3:
            btn_another = st.button("Guardar y crear otro", width="stretch")

        if btn_save or btn_another:
            try:
                registro = preparar_participante(id_banner, nombre_completo, estado_matriz,
                                                 asig_seleccionadas, observaciones, catalogo)
                insertados, _ = guardar_participantes([registro], programa_id)
            except ValueError as exc:
                st.warning(str(exc))
            except DatabaseError:
                st.error("No se pudo guardar el participante. Revisa los datos e intenta de nuevo.")
            else:
                if not insertados:
                    st.warning("El ID Banner ya está registrado.")
                else:
                    st.session_state["registro_guardado"] = "Se guardó el participante."
                    if btn_another:
                        st.session_state["form_version"] += 1
                    else:
                        ir_a("vista-maestra")
                    st.rerun()

    # --- BARRA LATERAL EN VIVO (CERO SANGRIAS) ---
    with col_sum:
        badge_style = "background-color: #10b981; color: white;" if estado_matriz == "Matriculado" else "background-color: #475569; color: white;"
        
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">🆔</div><div class="summary-details"><span class="summary-lbl">ID Banner asignado</span><span class="summary-val">{escape(id_banner) if id_banner else "—"}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">✓</div><div class="summary-details"><span class="summary-lbl">Estado en matriz</span><span><b class="badge-est" style="{badge_style}">{estado_matriz}</b></span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas de la BD</span><span class="summary-val">{len(asig_seleccionadas)} seleccionadas</span></div></div>'
        html_sum_box += '<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin:20px 0;">'
        html_sum_box += '<div class="req-title">Validación de Campos Reales</div>'
        
        c_ban = '#ffffff' if id_banner else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_ban};">{"●" if id_banner else "○"}</span> id_banner</div>'
        
        c_nom = '#ffffff' if nombre_completo else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre_completo else "○"}</span> nombre_completo</div>'
        
        html_sum_box += '<div class="checklist-item"><span class="check-icon" style="color:#ffffff;">●</span> estado_matriz</div>'
        
        c_asig = '#ffffff' if asig_seleccionadas else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> alfa_asignatura</div>'
        html_sum_box += '</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)