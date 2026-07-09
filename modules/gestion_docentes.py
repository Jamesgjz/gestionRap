import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO AL PANEL PRINCIPAL ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD (MOCKUP image_644b95.jpg) ---
    st.markdown("""
<style>
.docentes-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }

/* Encabezados */
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* Fila de Métricas Estilo Card de image_644b95.jpg */
.doc-metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.doc-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.doc-metric-icon-box { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-right: 16px; }
.doc-metric-info { display: flex; flex-direction: column; }
.doc-metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.doc-metric-val { font-size: 1.75rem; font-weight: 800; color: #0f172a; line-height: 1.2; }

/* Tabla Avanzada */
.table-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.doc-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
.doc-table th { background: #f8fafc; padding: 16px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; }
.doc-table td { padding: 16px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; }

/* Contenedor del Perfil del Docente (Avatar + Datos) */
.doc-profile-cell { display: flex; align-items: center; }
.doc-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 12px; flex-shrink: 0; }
.doc-info-text { display: flex; flex-direction: column; }
.doc-name { font-weight: 700; color: #0f172a; }
.doc-email { font-size: 0.8rem; color: #64748b; }

/* Badges de Estados */
.badge-doc { padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; display: inline-block; text-align: center; }
.badge-activo { background-color: #e6f4ea; color: #137333; }
.badge-revision { background-color: #e8f0fe; color: #1a73e8; }
.badge-sin-asignacion { background-color: #fef7e0; color: #b06000; }
.badge-inactivo { background-color: #f1f3f4; color: #5f6368; }

/* Banner Informativo Inferior */
.info-banner { background-color: #f0f4ff; border: 1px solid #d2e3fc; border-radius: 12px; padding: 20px; display: flex; align-items: start; margin-top: 30px; }
.info-banner-icon { font-size: 1.4rem; color: #0047ff; margin-right: 15px; margin-top: -2px; }
.info-banner-text { font-size: 0.95rem; color: #1e3a8a; line-height: 1.5; font-weight: 500; }

/* Estilo para los botones de Acción de la Tabla */
.action-icons { color: #0047ff; font-weight: 600; letter-spacing: 5px; cursor: pointer; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN DINÁMICA DE LA BASE DE DATOS ---
    tot_doc = 0
    tot_act = 0
    tot_asig = 0
    tot_pend = 0
    docentes_data = []

    try:
        # Conteos de métricas
        r_tot = traer_datos("SELECT COUNT(*) FROM profesores")
        if r_tot: tot_doc = r_tot[0][0]

        r_act = traer_datos("SELECT COUNT(*) FROM profesores WHERE estado = 'Activo'")
        if r_act: tot_act = r_act[0][0]

        r_asig = traer_datos("SELECT COUNT(*) FROM profesores WHERE horas_asignadas > 0")
        if r_asig: tot_asig = r_asig[0][0]

        r_pend = traer_datos("SELECT COUNT(*) FROM profesores WHERE estado = 'Pendiente' OR estado = 'En revisión'")
        if r_pend: tot_pend = r_pend[0][0]

        # Listado principal de la tabla
        docentes_data = traer_datos("SELECT nombre_completo, email, programa, asignaturas, horas_asignadas, estado, ultima_actualizacion FROM profesores")
    except Exception as e:
        st.sidebar.error(f"Error cargando Gestión Docente: {e}")

    st.markdown('<div class="docentes-container">', unsafe_allow_html=True)

    # --- ENCABEZADO DE SECCIÓN ---
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Gestión de docentes evaluadores</div>
        <div class="section-subtitle">Registra, actualiza y administra los docentes que participan en el proceso RAP.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- FILA DE COMPONENTES DE FILTRADO (FILAS NATIVAS) ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
    with f_col1:
        search_query = st.text_input("Buscar por nombre del docente...", key="doc_search_input", label_visibility="collapsed", placeholder="Buscar por nombre del docente...")
    with f_col2:
        st.selectbox("Programa", ["Todos los programas"], key="doc_filter_prog", label_visibility="collapsed")
    with f_col3:
        st.selectbox("Estado", ["Todos los estados"], key="doc_filter_status", label_visibility="collapsed")
    with f_col4:
        st.button("+ Nuevo docente", use_container_width=True, type="primary", key="new_doc_modal_btn")

    # --- GRID DE MÉTRICAS VISUALES ---
    st.markdown(f"""
    <div class="doc-metrics-grid">
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #e8f0fe; color: #1a73e8;">👥</div>
            <div class="doc-metric-info">
                <div class="doc-metric-lbl">Total docentes</div>
                <div class="doc-metric-val">{tot_doc}</div>
            </div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #e6f4ea; color: #137333;">✓</div>
            <div class="doc-metric-info">
                <div class="doc-metric-lbl">Activos</div>
                <div class="doc-metric-val" style="color: #137333;">{tot_act}</div>
            </div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #f3e8ff; color: #6b21a8;">📖</div>
            <div class="doc-metric-info">
                <div class="doc-metric-lbl">Con asignación</div>
                <div class="doc-metric-val" style="color: #6b21a8;">{tot_asig}</div>
            </div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #fef7e0; color: #b06000;">🕒</div>
            <div class="doc-metric-info">
                <div class="doc-metric-lbl">Pendientes</div>
                <div class="doc-metric-val" style="color: #b06000;">{tot_pend}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- CONSTRUCCIÓN DINÁMICA DE LAS FILAS DE LA TABLA ---
    html_table_rows = ""
    
    # Filtrado básico en memoria si se escribe en el buscador
    if docentes_data:
        for doc in docentes_data:
            nombre, email, programa, asignaturas, horas, estado, ultima_act = doc
            
            if search_query and search_query.lower() not in nombre.lower():
                continue
            
            # Generar Iniciales para el Avatar Circular
            partes = nombre.split()
            iniciales = "".join([p[0] for p in partes[:2]]).upper() if len(partes) >= 2 else nombre[:2].upper()
            
            # Asignar Paleta de Color del Avatar dinámicamente según iniciales
            bg_colors = ["#e8f0fe", "#e6f4ea", "#fef7e0", "#f3e8ff", "#fce8e6"]
            text_colors = ["#1a73e8", "#137333", "#b06000", "#6b21a8", "#c5221f"]
            idx = sum(ord(char) for char in iniciales) % len(bg_colors)
            avatar_bg = bg_colors[idx]
            avatar_txt = text_colors[idx]

            # Clasificación de Estilos de Estado de acuerdo a image_644b95.jpg
            estado_clean = estado.lower().strip()
            if "activo" in estado_clean:
                class_badge = "badge-activo"
            elif "revisión" in estado_clean or "revision" in estado_clean:
                class_badge = "badge-revision"
            elif "sin asignación" in estado_clean or "sin asignacion" in estado_clean:
                class_badge = "badge-sin-asignacion"
            else:
                class_badge = "badge-inactivo"

            html_table_rows += f"""
            <tr>
                <td>
                    <div class="doc-profile-cell">
                        <div class="doc-avatar" style="background: {avatar_bg}; color: {avatar_txt};">{iniciales}</div>
                        <div class="doc-info-text">
                            <span class="doc-name">{nombre}</span>
                            <span class="doc-email">{email}</span>
                        </div>
                    </div>
                </td>
                <td>{programa}</td>
                <td>{asignaturas if asignaturas else '<span style="color:#94a3b8;">Ninguna</span>'}</td>
                <td><b>{horas}</b> hrs</td>
                <td><span class="badge-doc {class_badge}">{estado}</span></td>
                <td>{ultima_act}</td>
                <td class="action-icons">👁️📝⋮</td>
            </tr>
            """
    else:
        html_table_rows = "<tr><td colspan='7' style='text-align:center; color:#64748b; padding:30px;'>No se encontraron registros de docentes evaluadores.</td></tr>"

    # --- RENDERIZADO DE LA TABLA ---
    st.markdown(f"""
    <h3 style="font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 20px; margin-bottom: 10px;">Listado de docentes</h3>
    <div class="table-wrapper">
        <table class="doc-table">
            <thead>
                <tr>
                    <th>Docente</th>
                    <th>Programa / Área</th>
                    <th>Asignaturas RAP</th>
                    <th>Horas asignadas</th>
                    <th>Estado</th>
                    <th>Última actualización</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {html_table_rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- BANNER INFORMATIVO INFERIOR ---
    st.markdown("""
    <div class="info-banner">
        <div class="info-banner-icon">ℹ️</div>
        <div class="info-banner-text">
            Este módulo permite la parametrización y soporte académico del proceso RAP. Asegúrate de mantener actualizada la información de los docentes y sus asignaciones para garantizar la correcta operación del proceso.
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)