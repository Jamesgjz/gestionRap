import streamlit as st
import pandas as pd
from database import ejecutar_query, traer_datos

def render():
    # --- INYECCIÓN DE LA PALETA DE COLORES Y DISEÑO EXACTO DE LOS MOCKUPS ---
    st.markdown("""
<style>
/* Reset Estructural del Lienzo de Trabajo */
[data-testid="stHeader"], [data-testid="stToolbar"] { background-color: transparent !important; }
html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* Estilización de las Pestañas Superiores (Calco de las Imágenes) */
div[data-testid="stTabs"] { border-bottom: 2px solid #e2e8f0 !important; margin-bottom: 25px !important; gap: 10px !important; }
button[data-baseweb="tab"] {
    color: #64748b !important;
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    background-color: transparent !important;
    border: none !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}
button[aria-selected="true"] {
    color: #0047ff !important;
    border-bottom: 2px solid #0047ff !important;
    font-weight: 700 !important;
}

/* Contenedores de Tarjetas Blancas Premium */
.form-card-wrapper { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; padding: 28px !important; margin-bottom: 25px !important; box-shadow: 0 4px 12px rgba(15,23,42,0.01) !important; }
.form-section-header { font-size: 1.02rem; font-weight: 700; color: #0f172a; margin-bottom: 18px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; }
.summary-sticky-card { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; padding: 24px !important; box-shadow: 0 4px 12px rgba(15,23,42,0.01) !important; }

/* Bloques de Navegación de la Cabecera (Imagen 1) */
.card-nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }
.card-nav-premium { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px; display: flex; gap: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); }
.card-nav-icon { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0; }

/* Indicadores de Métricas Cuadradas del Tablero */
.analytics-metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
.metric-premium-box { background: #ffffff; border-radius: 14px; padding: 20px; border: 1px solid #e2e8f0; position: relative; }
.metric-premium-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; margin-bottom: 4px; }
.metric-premium-val { font-size: 1.9rem; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.metric-premium-pct { font-size: 0.8rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.metric-premium-icon { position: absolute; top: 20px; right: 20px; font-size: 1.2rem; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }

/* Tablas Corporativas y Semáforos (Imágenes 2 y 5) */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.premium-data-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.premium-data-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-text-bubble { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; color: #0047ff; background: #edf5ff; }

.master-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: center; }
.master-matrix-table th { background: #f8fafc; color: #475569; padding: 12px 8px; font-weight: 600; border-bottom: 1px solid #e2e8f0; border-top: 1px solid #e2e8f0; text-align: center; }
.master-matrix-table td { padding: 12px 8px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; text-align: center; }

/* Píldoras de Estado Con Alineación y Colores Exactos */
.status-pill-built { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-pending { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-process { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-reprobado { background: #fce8e6; color: #c5221f; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-none { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }

/* Checklist de Requisitos Formulario */
.checklist-item-row { font-size: 0.85rem; color: #475569; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.checklist-item-row i { color: #94a3b8; }
.checklist-item-row.validated i { color: #16a34a; }
</style>
""", unsafe_allow_html=True)

    # Inicialización estable de sub-estados para manejar los saltos de formularios
    if 'reg_modo_docentes' not in st.session_state:
        st.session_state['reg_modo_docentes'] = "lista"

    # Creación de Pestañas Principales en base a los nombres de tus Mockups
    t_resumen, t_docentes, t_estudiantes, t_maestra = st.tabs([
        "📋 Resumen general", "Docentes evaluadores", "Estudiantes", "Vista maestra"
    ])

    # --- CONSULTA PREVIA DE CAPACIDADES DESDE LA DB ---
    total_estudiantes_db = traer_datos("SELECT COUNT(*) FROM estudiantes")
    total_profesores_db = traer_datos("SELECT COUNT(*) FROM profesores")
    total_asignaturas_db = traer_datos("SELECT COUNT(*) FROM asignaturas")

    count_est = total_estudiantes_db[0][0] if total_estudiantes_db else 1248
    count_prof = total_profesores_db[0][0] if total_profesores_db else 86
    count_asig = total_asignaturas_db[0][0] if total_asignaturas_db else 64

    # =========================================================================
    # 📑 PESTAÑA 1: RESUMEN GENERAL (`image_4733db.jpg`)
    # =========================================================================
    with t_resumen:
        st.markdown("""<div class="card-nav-grid">
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-user-graduate"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Docentes evaluadores</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-regular fa-user"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Estudiantes</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-regular fa-eye"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Vista maestra</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div></div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="analytics-metric-row">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total estudiantes</div><div class="metric-premium-val">{count_est}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-solid fa-users"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Docentes evaluadores</div><div class="metric-premium-val">{count_prof}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Pendientes de gestión</div><div class="metric-premium-val">86</div><div class="metric-premium-pct" style="color:#b06000;"><i class="fa-solid fa-arrow-up"></i> 5% <span style="color:#94a3b8; font-weight:400;">vs. corte</span></div><div class="metric-premium-icon" style="background:#fef7e0; color:#b06000;"><i class="fa-regular fa-clock"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Asignaturas activas</div><div class="metric-premium-val">{count_asig}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 10% <span style="color:#94a3b8; font-weight:400;">vs. periodo</span></div><div class="metric-premium-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-solid fa-book-open"></i></div></div>
</div>""", unsafe_allow_html=True)

        c_spl_l, c_spl_r = st.columns([1.15, 1])
        with c_spl_l:
            st.markdown("""<div class="panel-card-workspace" style="min-height:250px; background:white; border:1px solid #e2e8f0; border-radius:14px; padding:20px;">
<div class="panel-card-title">Actividad reciente</div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#137333;"></div><div class="timeline-content-text"><b>Nuevo estudiante registrado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 10:24 a. m.</span><br>Juan David Duque Aguirre</div></div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#0047ff;"></div><div class="timeline-content-text"><b>Docente evaluador actualizado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 09:46 a. m.</span><br>Richard Manuel Acosta Reyes</div></div>
</div>""", unsafe_allow_html=True)
        with c_spl_r:
            st.markdown('<div class="panel-card-title" style="margin-left:5px; margin-bottom:10px;">Accesos rápidos</div>', unsafe_allow_html=True)
            st.button("Validar documentos de estudiantes", key="b_qa_1", icon=":material/verified_user:", use_container_width=True)
            st.button("Programar prueba por asignatura", key="b_qa_2", icon=":material/calendar_month:", use_container_width=True)

    # =========================================================================
    # 👨‍🏫 PESTAÑA 2: DOCENTES EVALUADORES (`image_4736fe.jpg` y `image_473a46.jpg`)
    # =========================================================================
    with t_docentes:
        if st.session_state['reg_modo_docentes'] == "lista":
            c_hdr_l, c_hdr_r = st.columns([3, 1])
            with c_hdr_l:
                st.markdown("### Gestión de docentes evaluadores")
                st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
            with c_hdr_r:
                if st.button("➕ Nuevo docente", key="btn_to_new_doc", use_container_width=True, type="primary"):
                    st.session_state['reg_modo_docentes'] = "nuevo"
                    st.rerun()

            c_flt_1, c_flt_2, c_flt_3 = st.columns([1.5, 1, 1])
            with c_flt_1: st.text_input("Buscar por nombre del docente...", label_visibility="collapsed", key="search_d_name_real")
            with c_flt_2: st.selectbox("Programa", ["Todos los programas"], label_visibility="collapsed", key="sel_d_prog_real")
            with c_flt_3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed", key="sel_d_state_real")

            profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
            count_p = len(profesores_db) if profesores_db else 0

            st.markdown(f"""
<div class="analytics-metric-row" style="margin-top:15px; margin-bottom:20px;">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total docentes</div><div class="metric-premium-val">{count_p}</div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Activos</div><div class="metric-premium-val" style="color:#137333;">{count_p}</div><div class="metric-premium-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

            html_filas_p = ""
            if profesores_db:
                for p in profesores_db:
                    id_p, name_p, hrs_p = str(p[0]), str(p[1]), str(p[2])
                    initials = "".join([w[0] for w in name_p.split()[:2]]).upper() if name_p else "P"
                    html_filas_p += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-text-bubble">{initials}</div><div><b>{name_p}</b><br><span style="color:#64748b; font-size:0.75rem;">ID Profesor: {id_p}</span></div></div></td>
<td>Educación Virtual / Docencia</td>
<td>Módulos RAP Asignados</td>
<td>{hrs_p} horas</td>
<td><span class="status-pill-built">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; display:flex; gap:12px; font-size:1rem;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""
            else:
                html_filas_p = "<tr><td colspan='7' style='text-align:center; color:#64748b;'>No hay profesores cargados en el sistema relacional.</td></tr>"

            st.markdown(f"""<div class="form-card-wrapper" style="padding:20px; overflow-x:auto;">
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_filas_p}</tbody>
</table></div>""", unsafe_allow_html=True)

            if rol == "admin":
                st.divider()
                if profesores_db:
                    opts_p = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                    p_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_p.keys()), key="del_prof_select")
                    if st.button("❌ Eliminar Docente Seleccionado", type="secondary"):
                        ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (opts_p[p_sel],))
                        st.error("Registro de docente eliminado.")
                        st.rerun()

        elif st.session_state['reg_modo_docentes'] == "nuevo":
            if st.button("← Volver al Listado", key="btn_cancel_doc_form_real"):
                st.session_state['reg_modo_docentes'] = "lista"
                st.rerun()

            st.markdown("### Nuevo docente evaluador")
            st.caption("Completa la información estructurada para registrar un nuevo docente evaluador en el proceso RAP.")

            c_f_l, c_f_r = st.columns([2.2, 1])
            with c_f_l:
                with st.form("form_nuevo_docente_clean", clear_on_submit=True):
                    st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                    nombre_doc = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                    st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                    horas_doc = st.number_input("Horas de dedicación (horas_dedicacion) *", min_value=1, max_value=48, value=12)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    cb_1, cb_2 = st.columns(2)
                    with cb_1: b_save = st.form_submit_button("💾 Guardar docente", use_container_width=True)
                    with cb_2: b_cancel = st.form_submit_button("Cancelar", use_container_width=True)

                    if b_save:
                        if not nombre_doc.strip():
                            st.error("El nombre completo es un parámetro obligatorio del esquema.")
                        else:
                            try:
                                ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nombre_doc, horas_doc))
                                st.success("✅ Docente registrado de forma exitosa.")
                                st.session_state['reg_modo_docentes'] = "lista"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error operacional: {e}")
                    if b_cancel:
                        st.session_state['reg_modo_docentes'] = "lista"
                        st.rerun()

            with c_f_r:
                chk_name = "validated" if nombre_doc else ""
                st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="status-pill-built" style="display:inline;">Activo</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios</div>
<div class="checklist-item-row {chk_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> horas_dedicacion</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # 🎓 PESTAÑA 3: FORMULARIO DE ESTUDIANTES (`image_473b5e.jpg`)
    # =========================================================================
    with t_estudiantes:
        st.markdown("### Registrar / Actualizar Estudiante")
        st.caption("Completa los campos de matrícula definidos en tu base de datos para procesar el expediente RAP.")

        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?", key="chk_corr_est")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID Actual: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro con ID ERRÓNEO:", list(opts_correccion.keys()), key="sel_corr_est_id_real")
            id_antiguo = opts_correccion[est_a_corregir]

        c_est_l, c_est_r = st.columns([2.2, 1])
        with c_est_l:
            with st.form("form_estudiante_maquetado_real", clear_on_submit=True):
                st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                id_b = st.number_input("ID Banner (id_banner) *", step=1, value=id_antiguo if id_antiguo else 0)
                nom_e = st.text_input("Nombre completo (nombre_completo) *", placeholder="Ej. María Fernanda López Gómez")
                est = st.selectbox("Estado de matrícula (estado_matricula) *", ["Matriculado", "Admitido", "No matriculado"])
                
                st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas RAP (alfa_asignatura) *", list(opts.keys()))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Registrar / Actualizar Estudiante", type="primary", use_container_width=True):
                    if id_b <= 0 or not nom_e.strip():
                        st.error("Por favor, ingrese un ID Banner válido y el nombre completo.")
                    else:
                        alfas = ",".join([opts[m] for m in mats_sel])
                        try:
                            if modo_correccion and id_antiguo:
                                ejecutar_query("""
                                    UPDATE estudiantes SET id_banner = %s, nombre_completo = %s, estado_matricula = %s, alfa_asignatura = %s
                                    WHERE id_banner = %s
                                """, (id_b, nom_e, est, alfas, id_antiguo))
                                st.success("¡Identificación Banner corregida con éxito!")
                            else:
                                ejecutar_query("""
                                    INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id_banner) DO UPDATE SET 
                                        nombre_completo = EXCLUDED.nombre_completo,
                                        estado_matricula = EXCLUDED.estado_matricula,
                                        alfa_asignatura = EXCLUDED.alfa_asignatura
                                """, (id_b, nom_e, est, alfas))
                                st.success("Estudiante sincronizado con éxito.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error relacional en DB: {e}")

        with c_est_r:
            chk_est_id = "validated" if id_b > 0 else ""
            chk_est_name = "validated" if nom_e else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado actual: <span class="status-pill-process" style="display:inline; background:#e8f0fe; color:#1a73e8;">{est}</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos requeridos de la tabla</div>
<div class="checklist-item-row {chk_est_id}"><i class="fa-solid fa-circle-check"></i> id_banner</div>
<div class="checklist-item-row {chk_est_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> estado_matricula</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # 📊 PESTAÑA 4: VISTA MAESTRA (MATRIZ SEMÁFORO ULTRA VELOZ - `image_473e86.jpg`)
    # =========================================================================
    with t_maestra:
        st.markdown("### Vista maestra de asignaturas por estudiante")
        st.caption("Sincronización matricial de estados homologados en tiempo real.")

        c_mflt_1, c_mflt_2, c_mflt_3 = st.columns(3)
        with c_mflt_1: st.text_input("Buscar por nombre o ID Banner...", label_visibility="collapsed", key="mx_search_field_real")
        with c_mflt_2: st.selectbox("Programa ", ["Todos los programas"], label_visibility="collapsed")
        with c_mflt_3: st.selectbox("Estado ", ["Todos los estados"], label_visibility="collapsed")

        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            # --- PRECARGA MAESTRA EN CACHÉ DE MEMORIA (EVITA LA CARGA LENTA EN PANTALLA) ---
            pruebas_db = traer_datos("SELECT alfa_asignatura, estado FROM maestro_pruebas")
            mapa_estados_pruebas = {str(p[0]).strip(): str(p[1]) for p in pruebas_db} if pruebas_db else {}
            
            total_est = len(ests)
            barra_progreso = st.progress(0)
            
            html_matrix_rows = ""
            for idx, (idb, nom, alfas) in enumerate(ests):
                barra_progreso.progress(int(((idx + 1) / total_est) * 100))
                lista_alfas = [a.strip() for a in alfas.split(",")] if alfas else []
                
                def renderizar_pildora_estado(codigo_alfa):
                    if codigo_alfa not in lista_alfas:
                        return '<span class="status-pill-none">No aplica</span>'
                    status_real = mapa_estados_pruebas.get(str(codigo_alfa).strip(), "Pendiente")
                    if status_real == "Construida":
                        return '<span class="status-pill-built">Lista</span>'
                    elif status_real == "En construction" or status_real == "En construcción":
                        return '<span class="status-pill-process">En proceso</span>'
                    else:
                        return '<span class="status-pill-pending">Pendiente</span>'

                html_matrix_rows += f"""<tr>
<td style="text-align:left;">{idb}</td>
<td style="text-align:left;"><b>{nom}</b></td>
<td>{renderizar_pildora_estado("ISOF V003")}</td>
<td>{renderizar_pildora_estado("ISOF V013")}</td>
<td>{renderizar_pildora_estado("ISOF V043")}</td>
<td>{renderizar_pildora_estado("ISOF V063")}</td>
<td>{renderizar_pildora_estado("ISOF V081")}</td>
<td>{renderizar_pildora_estado("ISOF V095")}</td>
<td><div style="color:#0047ff; font-weight:700;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""

            barra_progreso.empty()

            st.markdown(f"""<div class="form-card-wrapper" style="padding:20px; overflow-x:auto; margin-top:15px;">
<table class="master-matrix-table">
<thead><tr>
<th style="text-align:left;">ID Banner</th><th style="text-align:left;">Estudiante</th>
<th>ISOF V003<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Intro. Software</span></th>
<th>ISOF V013<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Prog. POO</span></th>
<th>ISOF V043<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Bases de Datos</span></th>
<th>ISOF V063<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Estructuras</span></th>
<th>ISOF V081<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Redes</span></th>
<th>ISOF V095<br><span style="font-size:0.68rem; font-weight:400; color:#64748b;">Arquitectura</span></th>
<th>Detalle</th>
</tr></thead>
<tbody>{html_matrix_rows}</tbody>
</table>
<br>
<div style="display:flex; gap:20px; font-size:0.8rem; font-weight:600; flex-wrap:wrap; background:#f8fafc; padding:12px; border-radius:8px;">
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Completo)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En proceso</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica</span>
</div></div>""", unsafe_allow_html=True)
        else:
            st.info("No se registran estudiantes matriculados en el sistema.")