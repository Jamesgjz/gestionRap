import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA INTENSIDAD GRÁFICA EN AZULES CORPORATIVOS (Cero Rojo) ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }

/* Caja de Resumen: Azul Eléctrico e Institucional Vibrante */
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
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN DINÁMICA DE ASIGNATURAS REALES ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT alfa, nombre_materia FROM asignaturas")
        if db_asig:
            lista_asignaturas = [f"{str(item[0]).strip()} - {str(item[1]).strip()}" for item in db_asig if item[0] and item[1]]
    except Exception as e:
        st.sidebar.warning(f"Aviso de sincronización: {e}")
    
    if not lista_asignaturas:
        lista_asignaturas = [
            "ISOF V003 - Introducción a la Ingeniería de Software",
            "ISOF V013 - Desarrollo de Software I",
            "ISOF V023 - Estructuras de Datos y Algoritmos",
            "ISOF V033 - Análisis y Diseño de Sistemas"
        ]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo estudiante</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Formulario oficial parametrizado según las columnas de la tabla estudiantes de la base de datos.</div>', unsafe_allow_html=True)

    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES (Campos reales de la tabla estudiantes) ---
        st.markdown('<div class="form-section-title">1. Datos generales de matrícula</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            # Campo Real BD: id_banner
            id_banner = st.number_input("ID Banner (*id_banner) *", min_value=0, max_value=99999999, value=0, step=1)
            # Campo Real BD: estado_matriz
            estado_matriz = st.selectbox("Estado de matrícula (*estado_matriz) *", ["Matriculado", "No matriculado"])
        with g_col2:
            # Campo Real BD: nombre_completo
            nombre_completo = st.text_input("Nombre completo del estudiante *", placeholder="Ej. Alba Lucía Pinzón Gallego")

        # --- 2. ASIGNACIÓN ACADÉMICA (Campo real: alfa_asignatura) ---
        st.markdown('<div class="form-section-title">2. Vinculación curricular</div>', unsafe_allow_html=True)
        asig_seleccionadas = st.multiselect("Asignaturas RAP (*alfa_asignatura) *", options=lista_asignaturas, placeholder="Selecciona los códigos alfanuméricos")

        # --- 3. OBSERVACIONES (Campo real: observaciones) ---
        st.markdown('<div class="form-section-title">3. Observaciones del estudiante</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Notas adicionales (*observaciones)", max_chars=500, placeholder="Escribe apoyos requeridos o novedades académicas...")

        # --- BOTONERA DE ACCIÓN ---
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
            if nombre_completo and id_banner > 0 and asig_seleccionadas:
                codigos_alfa = [string.split(" - ")[0] for string in asig_seleccionadas]
                alfa_cadena = ", ".join(codigos_alfa)
                st.info(f"📘 Estudiante estructurado para inserción en Neon. Cursos: {alfa_cadena}")
            else:
                st.warning("⚠️ Por favor completa los campos obligatorios antes de guardar (*)")

    # --- BARRA LATERAL EN VIVO (CERO SANGRIAS DE EXTREMO IZQUIERDO PARA CONSERVAR EL DISEÑO) ---
    with col_sum:
        # Estilos adaptados en Azul Claro / Muted para cuando falten datos o esté no matriculado (Adiós Rojo)
        badge_style = "background-color: #10b981; color: white;" if estado_matriz == "Matriculado" else "background-color: #475569; color: white;"
        
        html_sum_box = '<div class="summary-box">'
        html_sum_box += '<div class="summary-title">Resumen de registro</div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">🆔</div><div class="summary-details"><span class="summary-lbl">ID Banner asignado</span><span class="summary-val">{id_banner if id_banner > 0 else "—"}</span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">✓</div><div class="summary-details"><span class="summary-lbl">Estado en matriz</span><span><b class="badge-est" style="{badge_style}">{estado_matriz}</b></span></div></div>'
        html_sum_box += f'<div class="summary-item"><div class="summary-icon">📚</div><div class="summary-details"><span class="summary-lbl">Asignaturas de la BD</span><span class="summary-val">{len(asig_seleccionadas)} seleccionadas</span></div></div>'
        html_sum_box += '<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin:20px 0;">'
        html_sum_box += '<div class="req-title">Validación de Campos Reales</div>'
        
        # Círculo blanco para completado, círculo translúcido para pendiente
        c_ban = '#ffffff' if id_banner > 0 else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_ban};">{"●" if id_banner > 0 else "○"}</span> id_banner</div>'
        
        c_nom = '#ffffff' if nombre_completo else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_nom};">{"●" if nombre_completo else "○"}</span> nombre_completo</div>'
        
        html_sum_box += '<div class="checklist-item"><span class="check-icon" style="color:#ffffff;">●</span> estado_matriz</div>'
        
        c_asig = '#ffffff' if asig_seleccionadas else 'rgba(255,255,255,0.4)'
        html_sum_box += f'<div class="checklist-item"><span class="check-icon" style="color:{c_asig};">{"●" if asig_seleccionadas else "○"}</span> alfa_asignatura</div>'
        html_sum_box += '</div>'
        
        st.markdown(html_sum_box, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)