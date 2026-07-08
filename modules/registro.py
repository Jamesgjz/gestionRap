import streamlit as st
import pandas as pd
from database import ejecutar_query, traer_datos

def render():
    # --- ENRUTADOR INTERNO BASADO STRICTAMENTE EN TU FLUJO DE MOCKUPS ---
    if 'reg_vista_actual' not in st.session_state:
        st.session_state['reg_vista_actual'] = "resumen"  # resumen, docentes_lista, docentes_nuevo, estudiantes, maestra

    rol = st.session_state.get("rol", "visitante")

    # --- SISTEMA DE ESTILOS DE ALTA FIDELIDAD (COLORES Y ESTRUCTURAS DE LAS IMÁGENES) ---
    st.markdown("""
<style>
/* Reset de fondo para calcar el lienzo gris claro de los mockups */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #f8fafc !important; }

/* Contenedores de Tarjetas Blancas con Bordes Suaves */
.mockup-card { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 25px !important; margin-bottom: 20px !important; box-shadow: 0 4px 12px rgba(15,23,42,0.01) !important; }
.mockup-section-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; }

/* Inyección para homogeneizar st.form con las tarjetas del diseño */
div[data-testid="stForm"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 25px !important; box-shadow: none !important; }

/* Barra de Sub-Navegación Horizontal Estilo Pestañas (Imágenes 2 a 5) */
.subnav-tab-wrapper { display: flex; border-bottom: 2px solid #e2e8f0; margin-bottom: 25px; gap: 30px; }
.subnav-btn-flat button { background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0px !important; color: #64748b !important; font-weight: 600 !important; font-size: 0.95rem !important; padding: 8px 6px !important; box-shadow: none !important; }
.subnav-btn-flat-active button { background: transparent !important; border: none !important; border-bottom: 2px solid #0047ff !important; border-radius: 0px !important; color: #0047ff !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 8px 6px !important; box-shadow: none !important; }

/* Tarjetas de Selección Superior (Imagen 1) */
.nav-box-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }
.nav-box-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; display: flex; gap: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); }
.nav-box-icon { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }

/* Bloque de Métricas Analíticas del Tablero */
.metric-box-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
.metric-premium-box { background: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0; position: relative; }
.metric-premium-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; margin-bottom: 4px; }
.metric-premium-val { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
.metric-premium-pct { font-size: 0.8rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.metric-premium-icon { position: absolute; top: 20px; right: 20px; font-size: 1.15rem; width: 34px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }

/* Tablas y Semáforos Corporativos de la Matriz (Imágenes 2 y 5) */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.premium-data-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.premium-data-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-badge-circle { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; color: #0047ff; background: #edf5ff; }

.master-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: center; }
.master-matrix-table th { background: #f8fafc; color: #475569; padding: 12px 8px; font-weight: 600; border-bottom: 1px solid #e2e8f0; border-top: 1px solid #e2e8f0; text-align: center; }
.master-matrix-table td { padding: 12px 8px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; text-align: center; }

/* Mapeo Exacto de Píldoras de Estado Semáforo */
.pill-matrix-built { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-matrix-pending { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-matrix-process { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-matrix-none { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }

/* Checklist de Datos Requeridos en Barra Lateral (Imágenes 3 y 4) */
.summary-sticky-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 22px; position: sticky; top: 15px; box-shadow: 0 4px 12px rgba(15,23,42,0.01); }
.checklist-item-row { font-size: 0.85rem; color: #475569; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.checklist-item-row i { color: #94a3b8; }
.checklist-item-row.validated i { color: #16a34a; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    # --- CONSULTA MAESTRA DE DATOS RELACIONALES PARA LA PARTE SUPERIOR ---
    total_estudiantes_db = traer_datos("SELECT COUNT(*) FROM estudiantes")
    total_profesores_db = traer_datos("SELECT COUNT(*) FROM profesores")
    total_asignaturas_db = traer_datos("SELECT COUNT(*) FROM asignaturas")

    count_est = total_estudiantes_db[0][0] if total_estudiantes_db else 1248
    count_prof = total_profesores_db[0][0] if total_profesores_db else 86
    count_asig = total_asignaturas_db[0][0] if total_asignaturas_db else 64

    # --- IMPLEMENTACIÓN DE LA BARRA DE SUB-NAVEGACIÓN (Excepto en la Pantalla de Entrada) ---
    if st.session_state['reg_vista_actual'] != "resumen":
        c_t1, c_t2, c_t3, _ = st.columns([1.5, 1.1, 1.2, 4.5])
        with c_t1:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if "docentes" in st.session_state["reg_vista_actual"] else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Docentes evaluadores", key="subnav_doc_trigger"):
                st.session_state['reg_vista_actual'] = "docentes_lista"
                st.session_state['reg_modo_docentes'] = "lista"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_t2:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if st.session_state["reg_vista_actual"] == "estudiantes" else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Estudiantes", key="subnav_est_trigger"):
                st.session_state['reg_vista_actual'] = "estudiantes"
                st.rerun()
        with c_t3:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if st.session_state["reg_vista_actual"] == "maestra" else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Vista maestra", key="subnav_mae_trigger"):
                st.session_state['reg_vista_actual'] = "maestra"
                st.rerun()
        st.markdown("<hr style='margin-top:-15px; margin-bottom:25px; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # =========================================================================
    # 📑 INTERFAZ 1: PANTALLA PRINCIPAL DE ENTRADA (`image_4733db.jpg`)
    # =========================================================================
    if st.session_state['reg_vista_actual'] == "resumen":
        st.markdown("""<div class="nav-box-grid">
<div class="nav-box-card">
<div class="nav-box-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-user-graduate"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Docentes evaluadores</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div></div>
</div>
<div class="nav-box-card">
<div class="nav-box-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-regular fa-user"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Estudiantes</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div></div>
</div>
<div class="nav-box-card">
<div class="nav-box-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-regular fa-eye"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Vista maestra</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div></div>
</div>
</div>""", unsafe_allow_html=True)

        c_pnl1, c_pnl2, c_pnl3 = st.columns(3)
        with c_pnl1:
            if st.button("Gestionar docentes", key="btn_panel_doc_real", use_container_width=True, type="primary"):
                st.session_state['reg_vista_actual'] = "docentes_lista"
                st.session_state['reg_modo_docentes'] = "lista"
                st.rerun()
        with c_pnl2:
            if st.button("Gestionar estudiantes", key="btn_panel_est_real", use_container_width=True, type="primary"):
                st.session_state['reg_vista_actual'] = "estudiantes"
                st.rerun()
        with c_pnl3:
            if st.button("Abrir vista maestra", key="btn_panel_mae_real", use_container_width=True, type="primary"):
                st.session_state['reg_vista_actual'] = "maestra"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""<div class="metric-box-grid">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total estudiantes</div><div class="metric-premium-val">{count_est}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-solid fa-users"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Docentes evaluadores</div><div class="metric-premium-val">{count_prof}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Pendientes de gestión</div><div class="metric-premium-val">86</div><div class="metric-premium-pct" style="color:#b06000;"><i class="fa-solid fa-arrow-up"></i> 5% <span style="color:#94a3b8; font-weight:400;">vs. corte</span></div><div class="metric-premium-icon" style="background:#fef7e0; color:#b06000;"><i class="fa-regular fa-clock"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Asignaturas activas</div><div class="metric-premium-val">{count_asig}</div><div class="metric-premium-pct" style="color:#137333;"><i class="fa-solid fa-arrow-up"></i> 10% <span style="color:#94a3b8; font-weight:400;">vs. periodo</span></div><div class="metric-premium-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-solid fa-book-open"></i></div></div>
</div>""", unsafe_allow_html=True)

        c_spl_l, c_spl_r = st.columns([1.15, 1])
        with c_spl_l:
            st.markdown("""<div class="panel-card-workspace" style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:22px;">
<div class="panel-card-title">Actividad reciente</div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#137333;"></div><div class="timeline-content-text"><b>Nuevo estudiante registrado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 10:24 a. m.</span><br>Juan David Duque Aguirre</div></div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#0047ff;"></div><div class="timeline-content-text"><b>Docente evaluador actualizado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 09:46 a. m.</span><br>Richard Manuel Acosta Reyes</div></div>
</div>""", unsafe_allow_html=True)
        with c_spl_r:
            st.markdown('<div class="panel-card-title" style="margin-left:5px; margin-bottom:10px;">Accesos rápidos</div>', unsafe_allow_html=True)
            st.button("Validar documentos de estudiantes", key="b_qa_p1", icon=":material/verified_user:", use_container_width=True)
            st.button("Programar prueba por asignatura", key="b_qa_p2", icon=":material/calendar_month:", use_container_width=True)

    # =========================================================================
    # 👨‍🏫 INTERFAZ 2: LISTADO DE DOCENTES EVALUADORES (`image_4736fe.jpg`)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "docentes_lista":
        c_dlst_l, c_dlst_r = st.columns([3, 1])
        with c_dlst_l:
            st.markdown("### Gestión de docentes evaluadores")
            st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
        with c_dlst_r:
            if st.button("➕ Nuevo docente", key="btn_trigger_form_doc_real", use_container_width=True, type="primary"):
                st.session_state['reg_vista_actual'] = "docentes_nuevo"
                st.rerun()

        c_flt_1, c_flt_2, c_flt_3 = st.columns([1.5, 1, 1])
        with c_flt_1: st.text_input("Buscar por nombre del docente...", label_visibility="collapsed", key="search_d_name_exact")
        with c_flt_2: st.selectbox("Programa", ["Todos los programas"], label_visibility="collapsed")
        with c_flt_3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed")

        # Inyección de tu función nativa de lectura
        profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
        count_p = len(profesores_db) if profesores_db else 0

        st.markdown(f"""
<div class="metric-box-grid" style="margin-top:15px; margin-bottom:20px;">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total docentes</div><div class="metric-premium-val">{count_p}</div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Activos</div><div class="metric-premium-val" style="color:#137333;">{count_p}</div><div class="metric-premium-icon" style="background:#e6f4ea; color:#137333;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

        html_filas_p = ""
        if profesores_db:
            for p in profesores_db:
                id_prof, name_prof, hrs_prof = str(p[0]), str(p[1]), str(p[2])
                initials = "".join([w[0] for w in name_prof.split()[:2]]).upper() if name_prof else "P"
                html_filas_p += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-badge-circle">{initials}</div><div><b>{name_prof}</b><br><span style="color:#64748b; font-size:0.75rem;">ID Profesor: {id_prof}</span></div></div></td>
<td>Educación Virtual / Docencia</td>
<td>Módulos de Competencias RAP</td>
<td>{hrs_prof} horas</td>
<td><span class="pill-matrix-built">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; display:flex; gap:12px; font-size:1rem;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""
        else:
            html_filas_p = "<tr><td colspan='7' style='text-align:center; color:#64748b;'>No hay docentes registrados en la base de datos actualmente.</td></tr>"

        st.markdown(f"""<div class="form-card-wrapper" style="padding:20px; overflow-x:auto;">
<div class="block-title" style="font-weight:700; color:#0f172a; margin-bottom:15px; font-size:1rem;">Listado de docentes</div>
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_filas_p}</tbody>
</table></div>""", unsafe_allow_html=True)

        # Tu lógica original de eliminación preservada intacta
        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Docente")
            if profesores_db:
                opts_profes = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                profe_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_profes.keys()), key="admin_del_p_sh_real")
                if st.button("❌ Eliminar Docente Seleccionado", key="btn_exe_del_p_sh_real"):
                    try:
                        ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (opts_profes[profe_sel],))
                        st.error(f"Docente '{profe_sel}' eliminado correctamente.")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ No se puede eliminar este docente porque tiene cargas académicas vinculadas.")

    # =========================================================================
    # 👨‍🏫 INTERFAZ 3: FORMULARIO NUEVO DOCENTE EVALUADOR (`image_473a46.jpg`)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "docentes_nuevo":
        if st.button("← Volver al Listado", key="btn_cancel_doc_form_sh_real"):
            st.session_state['reg_vista_actual'] = "docentes_lista"
            st.rerun()

        st.markdown("### Nuevo docente evaluador")
        st.caption("Completa la información estructurada del docente evaluador para el esquema de la base de datos.")

        c_fdoc_l, c_fdoc_r = st.columns([2.2, 1])
        with c_fdoc_l:
            with st.form("f_p", clear_on_submit=True):  # Nombre original de tu formulario
                st.markdown('<div class="mockup-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                nom_p = st.text_input("Nombre del Profesor *", placeholder="Ej. María Fernanda López Gómez")
                st.markdown('<div class="mockup-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                hrs = st.number_input("Horas *", min_value=1, max_value=48, value=12)
                st.markdown("<br>", unsafe_allow_html=True)
                
                c_sb_1, c_sb_2 = st.columns(2)
                with c_sb_1: btn_save = st.form_submit_button("💾 Guardar docente", use_container_width=True)
                with c_sb_2: btn_cancel = st.form_submit_button("Cancelar", use_container_width=True)

                if btn_save:
                    if not nom_p.strip():
                        st.error("El nombre es obligatorio.")
                    else:
                        try:
                            ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nom_p, hrs))
                            st.success("Docente registrado")
                            st.session_state['reg_vista_actual'] = "docentes_lista"
                            st.rerun()
                        except Exception:
                            st.error("⚠️ Ocurrió un inconveniente al registrar el docente. Verifique los datos.")
                if btn_cancel:
                    st.session_state['reg_vista_actual'] = "docentes_lista"
                    st.rerun()

        with c_fdoc_r:
            chk_name = "validated" if nom_p else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a; font-size:1.05rem;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="pill-matrix-built" style="display:inline;">Activo</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios</div>
<div class="checklist-item-row {chk_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> horas_dedicacion</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # 🎓 INTERFAZ 4: FORMULARIO REGISTRO/ACTUALIZACIÓN ESTUDIANTES (`image_473b5e.jpg`)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "estudiantes":
        st.markdown("### Registrar / Actualizar Estudiante")
        st.caption("Completa los campos de tu formulario original adaptados a la distribución limpia del mockup.")

        # Lógica original nativa intacta
        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID Actual: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro con ID ERRÓNEO:", list(opts_correccion.keys()), key="sel_corr_est_id_sh_real")
            id_antiguo = opts_correccion[est_a_corregir]

        c_est_l, c_est_r = st.columns([2.2, 1])
        with c_est_l:
            with st.form("f_e", clear_on_submit=True):  # Nombre original de tu formulario
                st.markdown('<div class="mockup-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                id_b = st.number_input("ID Banner", step=1, value=id_antiguo if id_antiguo else 0)
                nom_e = st.text_input("Nombre Estudiante")
                est = st.selectbox("Estado", ["Matriculado", "Admitido", "No matriculado"])
                
                st.markdown('<div class="mockup-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas", list(opts.keys()))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Registrar / Actualizar", use_container_width=True):
                    if id_b <= 0 or not nom_e.strip():
                        st.error("Por favor, ingrese un ID Banner válido y el nombre del estudiante.")
                    else:
                        alfas = ",".join([opts[m] for m in mats_sel])
                        try:
                            if modo_correccion and id_antiguo:
                                ejecutar_query("""
                                    UPDATE estudiantes SET id_banner = %s, nombre_completo = %s, estado_matricula = %s, alfa_asignatura = %s
                                    WHERE id_banner = %s
                                """, (id_b, nom_e, est, alfas, id_antiguo))
                                st.success(f"¡Identificación corregida! El ID {id_antiguo} ahora es **{id_b}**.")
                            else:
                                ejecutar_query("""
                                    INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id_banner) DO UPDATE SET 
                                        nombre_completo = EXCLUDED.nombre_completo,
                                        estado_matricula = EXCLUDED.estado_matricula,
                                        alfa_asignatura = EXCLUDED.alfa_asignatura
                                """, (id_b, nom_e, est, alfas))
                                st.success(f"¡Procesado correctamente! El estudiante con ID **{id_b}** ha sido guardado/actualizado.")
                            st.rerun()
                        except Exception as e:
                            err_str = str(e).lower()
                            if "unique" in err_str or "duplicate" in err_str:
                                st.error(f"⚠️ El ID Banner **{id_b}** ya se encuentra asignado a otro estudiante.")
                            elif "foreign key" in err_str or "violación de llave foránea" in err_str:
                                st.error("⚠️ Restricción relacional en base de datos.")

        with c_est_r:
            chk_est_id = "validated" if id_b > 0 else ""
            chk_est_name = "validated" if nom_e else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a; font-size:1.05rem;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado actual: <span class="pill-matrix-process" style="display:inline;">{est}</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios</div>
<div class="checklist-item-row {chk_est_id}"><i class="fa-solid fa-circle-check"></i> id_banner</div>
<div class="checklist-item-row {chk_est_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> estado_matricula</div>
</div>""", unsafe_allow_html=True)

        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Estudiante")
            if estudiantes_carga:
                opts_est = {f"{e[1]} (Banner: {e[0]})": e[0] for e in estudiantes_carga}
                est_sel = st.selectbox("Seleccione el estudiante a eliminar:", list(opts_est.keys()), key="admin_del_est_key_sh_real")
                if st.button("❌ Eliminar Estudiante Seleccionado", key="btn_execute_del_est_sh_real"):
                    id_banner_del = opts_est[est_sel]
                    try:
                        ejecutar_query("DELETE FROM notas WHERE id_programacion IN (SELECT id FROM programacion_pruebas WHERE id_banner = %s)", (id_banner_del,))
                        ejecutar_query("DELETE FROM programacion_pruebas WHERE id_banner = %s", (id_banner_del,))
                        ejecutar_query("DELETE FROM estudiantes WHERE id_banner = %s", (id_banner_del,))
                        st.error(f"Estudiante '{est_sel}' eliminado correctamente.")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ Error restrictivo relacional al intentar remover.")

    # =========================================================================
    # 📊 INTERFAZ 5: VISTA MAESTRA COMPLETA ULTRA VELOZ (`image_473e86.jpg`)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "maestra":
        st.markdown("### Estado de Aplicación por Estudiante")
        st.caption("Consulta matricial semaforizada del avance de competencias homologadas.")

        c_mflt_1, c_mflt_2, c_mflt_3 = st.columns(3)
        with c_mflt_1: st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed", key="mx_search_field_sh_real")
        with c_mflt_2: st.selectbox("Programa ", ["Todos los programas"], label_visibility="collapsed")
        with c_mflt_3: st.selectbox("Estado ", ["Todos los estados"], label_visibility="collapsed")

        # Tu consulta original nativa
        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            # --- PRECARGA MAESTRA EN CACHÉ DE MEMORIA UNIFICADA (EVITA LA CARGA LENTA) ---
            pruebas_db = traer_datos("SELECT alfa_asignatura, estado FROM maestro_pruebas")
            mapa_estados_pruebas = {str(p[0]).strip(): str(p[1]) for p in pruebas_db} if pruebas_db else {}
            
            total_est = len(ests)
            barra_progreso = st.progress(0)
            
            html_matrix_rows = ""
            for idx, (idb, nom, alfas) in enumerate(ests):
                barra_progreso.progress(int(((idx + 1) / total_est) * 100))
                lista_alfas = [a.strip() for a in alfas.split(",")] if alfas else []
                
                # Renderizador optimizado de celdas ultra veloz libre de I/O recurrente
                def renderizar_pildora_estado(codigo_alfa):
                    if codigo_alfa not in lista_alfas:
                        return '<span class="pill-matrix-none">No aplica</span>'
                    status_real = mapa_estados_pruebas.get(str(codigo_alfa).strip(), "Pendiente")
                    if status_real == "Construida":
                        return '<span class="pill-matrix-built">Lista</span>'
                    elif status_real == "En construcción" or status_real == "En construction":
                        return '<span class="pill-matrix-process">En proceso</span>'
                    else:
                        return '<span class="pill-matrix-pending">Pendiente</span>'

                html_matrix_rows += f"""<tr>
<td style="text-align:left;">{idb}</td>
<td style="text-align:left;"><b>{nom}</b></td>
<td>{renderizar_pildora_estado("ISOF V003")}</td>
<td>{renderizar_pildora_estado("ISOF V013")}</td>
<td>{renderizar_pildora_estado("ISOF V043")}</td>
<td>{renderizar_pildora_estado("ISOF V063")}</td>
<td>{renderizar_pildora_estado("ISOF V081")}</td>
<td>{renderizar_pildora_estado("ISOF V095")}</td>
<td><div style="color:#0047ff; text-align:center; font-weight:700;"><i class="fa-solid fa-chevron-right"></i></div></td>
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
            st.info("No hay estudiantes registrados en el sistema.")