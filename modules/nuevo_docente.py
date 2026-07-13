import streamlit as st
from database import traer_datos
# Nota: Si tienes una función para ejecutar inserts en tu base de datos (ej. ejecutar_db), impórtala aquí.

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver a Gestión de Docentes", key="back_to_docs"):
        st.session_state['reg_vista'] = "docentes"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD (Mockup registro docente.png) ---
    st.markdown("""
<style>
.form-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.form-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.form-subtitle { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; }

/* Títulos de sección */
.form-section-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }

/* Barra Lateral de Resumen */
.summary-box { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); position: sticky; top: 20px; }
.summary-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }
.summary-item { display: flex; align-items: center; margin-bottom: 16px; }
.summary-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-right: 12px; }
.summary-details { display: flex; flex-direction: column; }
.summary-lbl { font-size: 0.8rem; color: #64748b; font-weight: 600; }
.summary-val { font-size: 0.95rem; font-weight: 700; color: #0f172a; }

/* Checklist de requeridos */
.req-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-top: 25px; margin-bottom: 12px; }
.checklist-item { display: flex; align-items: center; margin-bottom: 8px; font-size: 0.9rem; color: #475569; }
.check-icon { margin-right: 10px; font-weight: bold; }

/* Botones inferiores */
.btn-guardar button { background-color: #0047ff !important; color: white !important; font-weight: 700 !important; padding: 10px 22px !important; border-radius: 8px !important; border: none !important; }
.btn-guardar button:hover { background-color: #0036d6 !important; }
.btn-cancelar button { background-color: white !important; color: #475569 !important; font-weight: 600 !important; padding: 10px 22px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
.btn-cancelar button:hover { background-color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

    # --- CONSULTA DE ASIGNATURAS ALMACENADAS EN LA BD ---
    lista_asignaturas = []
    try:
        db_asig = traer_datos("SELECT nombre FROM asignaturas")
        if db_asig:
            lista_asignaturas = [str(item[0]) for item in db_asig]
    except Exception as e:
        st.sidebar.warning(f"Carga de asignaturas de BD pausada: {e}")
    
    # Fallback por si la tabla de asignaturas está vacía o no existe aún
    if not lista_asignaturas:
        lista_asignaturas = ["Lógica Matemática", "Algoritmos", "Pensamiento Crítico", "Matemáticas I", "Estadística", "Contabilidad General"]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Nuevo docente evaluador</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Completa la información para registrar a un nuevo docente que participará en el proceso RAP.</div>', unsafe_allow_html=True)

    # Split en 2 columnas: Formulario (Izquierda) y Resumen (Derecha)
    col_form, col_sum = st.columns([2.2, 1])

    with col_form:
        # --- 1. DATOS GENERALES ---
        st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            nombre = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
            documento = st.text_input("Documento *", placeholder="Ej. 1.234.567.890")
            programa = st.selectbox("Programa / Área *", ["Selecciona un programa o área", "Ingeniería de Sistemas", "Administración de Empresas", "Contaduría Pública", "Psicología", "Derecho"])
        with g_col2:
            correo = st.text_input("Correo institucional *", placeholder="Ej. maria.lopez@uniminuto.edu.co")
            telefono = st.text_input("Teléfono *", placeholder="Ej. 300 123 4567")
            estado = st.selectbox("Estado *", ["Activo", "En revisión", "Sin asignación", "Inactivo"])

        # --- 2. ASIGNACIÓN ACADÉMICA ---
        st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            # Multi-select alimentado dinámicamente de las asignaturas de la base de datos
            asig_seleccionadas = st.multiselect("Asignaturas RAP *", options=lista_asignaturas, placeholder="Selecciona las asignaturas")
            perfil = st.selectbox("Perfil / rol *", ["Docente evaluador", "Docente constructor", "Coordinador RAP"])
        with a_col2:
            horas = st.number_input("Horas asignadas *", min_value=0, max_value=100, value=12, step=1)
            modalidad = st.selectbox("Modalidad de participación *", ["Seleccione una modalidad", "Virtual", "Presencial", "Híbrida"])

        # --- 3. OBSERVACIONES ---
        st.markdown('<div class="form-section-title">3. Observaciones</div>', unsafe_allow_html=True)
        observaciones = st.text_area("Observaciones adicionales", max_chars=500, placeholder="Ej. Información adicional relevante sobre el docente, disponibilidad, observaciones, etc.")
        st.markdown(f'<p style="text-align:right; color:#64748b; font-size:0.85rem; margin-top:-10px;">{len(observaciones)}/500</p>', unsafe_allow_html=True)

        # --- ACCIONES DE FORMULARIO ---
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
            # Enlace simple de acción secundaria
            st.markdown('<p style="margin-top:10px;"><a href="#" style="color:#0047ff; font-weight:700; text-decoration:none;">Guardar y crear otro</a></p>', unsafe_allow_html=True)

        # Lógica de guardado simulada/estructurada
        if btn_save:
            if nombre and correo and documento and programa != "Selecciona un programa o área":
                st.success(f"🎉 ¡Docente {nombre} preparado para registro correctamente!")
                # Aquí colocarías tu lógica real: ejecutar_db("INSERT INTO profesores ...")
            else:
                st.error("❌ Por favor completa todos los campos obligatorios (*)")

    # --- BARRA LATERAL DERECHA: RESUMEN DINÁMICO EN TIEMPO REAL ---
    with col_sum:
        prog_display = programa if programa != "Selecciona un programa o área" else "—"
        badge_style = "background-color: #e6f4ea; color: #137333;" if estado == "Activo" else "background-color: #fef7e0; color: #b06000;"
        
        st.markdown(f"""
        <div class="summary-box">
            <div class="summary-title">Resumen de registro</div>
            
            <div class="summary-item">
                <div class="summary-icon" style="background:#e8f0fe; color:#1a73e8;">💼</div>
                <div class="summary-details">
                    <span class="summary-lbl">Programa / Área</span>
                    <span class="summary-val">{prog_display}</span>
                </div>
            </div>
            
            <div class="summary-item">
                <div class="summary-icon" style="background:#e6f4ea; color:#137333;">✓</div>
                <div class="summary-details">
                    <span class="summary-lbl">Estado</span>
                    <span class="badge-doc" style="{badge_style} padding:2px 8px; border-radius:10px; font-size:0.8rem; font-weight:700;">{estado}</span>
                </div>
            </div>
            
            <div class="summary-item">
                <div class="summary-icon" style="background:#f3e8ff; color:#6b21a8;">📚</div>
                <div class="summary-details">
                    <span class="summary-lbl">Asignaturas seleccionadas</span>
                    <span class="summary-val">{len(asig_seleccionadas)}</span>
                </div>
            </div>
            
            <div class="summary-item">
                <div class="summary-icon" style="background:#fef7e0; color:#b06000;">🕒</div>
                <div class="summary-details">
                    <span class="summary-lbl">Horas asignadas</span>
                    <span class="summary-val">{horas} horas</span>
                </div>
            </div>
            
            <hr style="border:0; border-top:1px solid #e2e8f0; margin:20px 0;">
            <div class="req-title">Datos requeridos</div>
            
            <div class="checklist-item">
                <span class="check-icon" style="color:{'#00875a' if nombre else '#94a3b8'};">{'●' if nombre else '○'}</span> Nombre completo
            </div>
            <div class="checklist-item">
                <span class="check-icon" style="color:{'#00875a' if '@' in correo else '#94a3b8'};">{'●' if '@' in correo else '○'}</span> Correo institucional
            </div>
            <div class="checklist-item">
                <span class="check-icon" style="color:{'#00875a' if documento else '#94a3b8'};">{'●' if documento else '○'}</span> Documento
            </div>
            <div class="checklist-item">
                <span class="check-icon" style="color:{'#00875a' if programa != 'Selecciona un programa o área' else '#94a3b8'};">{'●' if programa != 'Selecciona un programa o área' else '○'}</span> Programa / Área
            </div>
            <div class="checklist-item">
                <span class="check-icon" style="color:{'#00875a' if asig_seleccionadas else '#94a3b8'};">{'●' if asig_seleccionadas else '○'}</span> Asignaturas RAP
            </div>
            <div class="checklist-item">
                <span class="check-icon" style="color:#00875a;">●</span> Horas asignadas
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)