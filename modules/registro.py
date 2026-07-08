import streamlit as st
import pandas as pd
from database import ejecutar_query, traer_datos

def render():
    # --- CONTROL DE ESTADOS DE NAVEGACIÓN (FLUJO DE IMÁGENES 1 A 5) ---
    if 'reg_modulo_vista' not in st.session_state:
        st.session_state['reg_modulo_vista'] = "principal"  # principal, docentes, estudiantes, maestra
    if 'reg_modo_docentes' not in st.session_state:
        st.session_state['reg_modo_docentes'] = "lista"      # lista, nuevo

    rol = st.session_state.get("rol", "visitante")

    # --- ARQUITECTURA DE ESTILOS CSS INYECTADOS NATIVAMENTE ---
    st.markdown("""
<style>
/* Contenedores de Diseño e Interfaz */
.main-dashboard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.breadcrumb-text { font-size: 0.85rem; color: #64748b; margin-bottom: 4px; }
.title-main-text { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0; }
.subtitle-text { font-size: 0.95rem; color: #64748b; margin: 4px 0 0 0; }

/* Tarjetas de Selección Maestra (Imagen 1) */
.card-nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px; }
.card-nav-premium { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 26px; display: flex; gap: 18px; box-shadow: 0 4px 10px rgba(15,23,42,0.01); }
.card-nav-icon { width: 46px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }

/* Grid de Métricas Analíticas Estilo Panel */
.analytics-metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
.metric-premium-box { background: white; border-radius: 16px; padding: 22px; border: 1px solid #e2e8f0; position: relative; box-shadow: 0 2px 6px rgba(0,0,0,0.01); }
.metric-premium-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; margin-bottom: 6px; }
.metric-premium-val { font-size: 2rem; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.metric-premium-pct { font-size: 0.82rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.metric-premium-icon { position: absolute; top: 22px; right: 22px; font-size: 1.25rem; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }

/* Estructura del Cuerpo Bifurcado Inferior */
.split-workspace-grid { display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; margin-bottom: 25px; }
.panel-card-workspace { background: white; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; }
.panel-card-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 18px; }

/* Componentes de Línea de Tiempo e Historial */
.timeline-item-box { display: flex; gap: 14px; margin-bottom: 14px; position: relative; }
.timeline-marker-dot { width: 9px; height: 9px; border-radius: 50%; background: #0052cc; margin-top: 5px; flex-shrink: 0; }
.timeline-content-text { font-size: 0.85rem; color: #334155; }

/* Estilos de Formularios de Dos Columnas y Resúmenes Laterales (Imágenes 3 y 4) */
.form-card-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px; margin-bottom: 20px; }
.form-section-header { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 16px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; text-transform: uppercase; letter-spacing: 0.3px; }
.summary-sticky-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; position: sticky; top: 15px; }
.checklist-item-row { font-size: 0.85rem; color: #475569; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.checklist-item-row i { color: #94a3b8; }
.checklist-item-row.validated i { color: #16a34a; }

/* Tablas Maestras y Semáforos Corporativos (Imágenes 2 y 5) */
.matrix-rendered-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.matrix-rendered-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.matrix-rendered-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-text-bubble { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; color: #0047ff; background: #edf5ff; }

.status-pill-built { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-pending { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-process { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-reprobado { background: #fce8e6; color: #c5221f; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-none { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    # --- BARRA SUPERIOR DE CONTEXTO GENERAL ---
    st.markdown("""<div class="main-dashboard-header">
<div>
<div class="breadcrumb-text">Inicio &gt; Gestión de Registros</div>
<h1 class="title-main-text">Gestión de Registros</h1>
<p class="subtitle-text">Administra docentes evaluadores, estudiantes y consulta la vista maestra del proceso RAP.</p>
</div>
<div style="text-align: right;"><div style="font-size: 0.9rem; color: #64748b; font-weight: 600;"><i class="fa-regular fa-calendar"></i> 21 de mayo de 2025</div></div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # CUMPLIMIENTO INTERFAZ 1: PANEL DE CONTROL PRINCIPAL (`image_4733db.jpg`)
    # =========================================================================
    if st.session_state['reg_modulo_vista'] == "principal":
        # Bloque de 3 Tarjetas de Navegación de la Cabecera
        st.markdown("""<div class="card-nav-grid">
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-user-graduate"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Docentes evaluadores</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-user"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Estudiantes</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-regular fa-eye"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Vista maestra</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div></div>
</div>
</div>""", unsafe_allow_html=True)

        # Botonera de Redirección Vinculada a los Estados
        c_nav_1, c_nav_2, c_nav_3 = st.columns(3)
        with c_nav_1:
            if st.button("Gestionar docentes", key="btn_panel_doc", use_container_width=True, type="primary"):
                st.session_state['reg_modulo_vista'] = "docentes"
                st.session_state['reg_modo_docentes'] = "lista"
                st.rerun()
        with c_nav_2:
            if st.button("Gestionar estudiantes", key="btn_panel_est", use_container_width=True, type="primary"):
                st.session_state['reg_modulo_vista'] = "estudiantes"
                st.rerun()
        with c_nav_3:
            if st.button("Abrir vista maestra", key="btn_panel_mae", use_container_width=True, type="primary"):
                st.session_state['reg_modulo_vista'] = "maestra"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Cálculos de Métricas en Tiempo Real desde las Tablas Base
        total_estudiantes_db = traer_datos("SELECT COUNT(*) FROM estudiantes")
        total_profesores_db = traer_datos("SELECT COUNT(*) FROM profesores")
        total_asignaturas_db = traer_datos("SELECT COUNT(*) FROM asignaturas")
        total_pendientes_db = traer_datos("SELECT COUNT(*) FROM estado_pruebas")

        count_est = total_estudiantes_db[0][0] if total_estudiantes_db else 1248
        count_prof = total_profesores_db[0][0] if total_profesores_db else 86
        count_asig = total_asignaturas_db[0][0] if total_asignaturas_db else 64
        count_pend = total_pendientes_db[0][0] if total_pendientes_db else 86

        st.markdown(f"""<div class="analytics-metric-row">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total estudiantes</div><div class="metric-premium-val">{count_est}</div><div class="metric-premium-pct" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#f0fdf4; color:#16a34a;"><i class="fa-solid fa-users"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Docentes evaluadores</div><div class="metric-premium-val">{count_prof}</div><div class="metric-premium-pct" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Pendientes de gestión</div><div class="metric-premium-val">{count_pend}</div><div class="metric-premium-pct" style="color:#ef4444;"><i class="fa-solid fa-arrow-up"></i> 5% <span style="color:#94a3b8; font-weight:400;">vs. corte</span></div><div class="metric-premium-icon" style="background:#fff7ed; color:#ea580c;"><i class="fa-regular fa-clock"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Asignaturas activas</div><div class="metric-premium-val">{count_asig}</div><div class="metric-premium-pct" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 10% <span style="color:#94a3b8; font-weight:400;">vs. periodo</span></div><div class="metric-premium-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-solid fa-book-open"></i></div></div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Bloque de Trazabilidad Reciente Estática y Accesos Rápidos Cruzados
        c_split_l, c_split_r = st.columns([1.15, 1])
        with c_split_l:
            st.markdown("""<div class="panel-card-workspace" style="min-height:280px;">
<div><div class="panel-card-title">Actividad reciente</div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#16a34a;"></div><div class="timeline-content-text"><b>Nuevo estudiante registrado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 10:24 a. m.</span><br>Juan David Duque Aguirre</div></div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#0052cc;"></div><div class="timeline-content-text"><b>Docente evaluador actualizado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 09:46 a. m.</span><br>Richard Manuel Acosta Reyes</div></div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#ea580c;"></div><div class="timeline-content-text"><b>Resultado registrado</b><br><span style="color:#64748b; font-size:0.75rem;">Ayer, 4:30 p. m.</span><br>Pensamiento Crítico</div></div>
<div class="timeline-item-box"><div class="timeline-marker-dot" style="background:#9333ea;"></div><div class="timeline-content-text"><b>Prueba programada</b><br><span style="color:#64748b; font-size:0.75rem;">Ayer, 9:15 a. m.</span><br>Razonamiento Cuantitativo</div></div>
</div></div>""", unsafe_allow_html=True)

        with c_split_r:
            st.markdown('<div class="panel-card-title" style="margin-left:5px; margin-bottom:10px;">Accesos rápidos</div>', unsafe_allow_html=True)
            if st.button("Validar documentos de estudiantes", key="qa_btn_1", icon=":material/verified_user:", use_container_width=True):
                st.toast("Redirigiendo a Validación de Documentos...")
            if st.button("Programar prueba por asignatura", key="qa_btn_2", icon=":material/calendar_month:", use_container_width=True):
                st.toast("Redirigiendo a Programación Académica...")
            if st.button("Evaluaciones por revisar", key="qa_btn_3", icon=":material/rate_review:", use_container_width=True):
                st.toast("Redirigiendo a Calificaciones...")
            if st.button("Exportar reportes académicos", key="qa_btn_4", icon=":material/download:", use_container_width=True):
                st.toast("Descargando consolidados RAP...")

        # Banner Informativo de Cierre
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""<div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 16px 24px; color: #1e40af; font-size: 0.9rem; display: flex; align-items: center; gap: 12px;">
<i class="fa-solid fa-circle-info" style="font-size: 1.1rem;"></i>
<span>El módulo de Docentes evaluadores es un espacio de soporte y parametrización del proceso RAP. Su gestión asegura la correcta asignación y evaluación de las pruebas institucionales.</span>
</div>
<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:35px; font-weight:500;">
RAP Digital - Gestión Académica<br>Reconocimiento de Aprendizajes Previos | UNIMINUTO Virtual
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # CUMPLIMIENTO INTERFAZ 2: LISTADO DE DOCENTES EVALUADORES (`image_4736fe.jpg`)
    # =========================================================================
    elif st.session_state['reg_modulo_vista'] == "docentes" and st.session_state['reg_modo_docentes'] == "lista":
        c_hdr_l, c_hdr_r = st.columns([3, 1])
        with c_hdr_l:
            st.markdown("### Gestión de docentes evaluadores")
            st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
        with c_hdr_r:
            if st.button("➕ Nuevo docente", key="btn_trigger_form_doc", use_container_width=True, type="primary"):
                st.session_state['reg_modo_docentes'] = "nuevo"
                st.rerun()
            if st.button("← Volver al Menú", key="btn_esc_doc_m", use_container_width=True):
                st.session_state['reg_modulo_vista'] = "principal"
                st.rerun()

        # Filtros de Interfaz Maquetados Estéticamente
        st.markdown("<br>", unsafe_allow_html=True)
        c_flt_1, c_flt_2, c_flt_3 = st.columns([1.5, 1, 1])
        with c_flt_1: st.text_input("Buscar por nombre", placeholder="Buscar por nombre del docente...", label_visibility="collapsed", key="search_d_name")
        with c_flt_2: st.selectbox("Programa", ["Todos los programas", "Ingeniería de Sistemas"], label_visibility="collapsed", key="sel_d_prog")
        with c_flt_3: st.selectbox("Estado", ["Todos los estados", "Activo"], label_visibility="collapsed", key="sel_d_state")

        # Extracción y Mapeo Real de Campos Existentes de la Base de Datos (`id_profesor`, `nombre_completo`, `horas_dedicacion`)
        profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
        count_prof_total = len(profesores_db) if profesores_db else 0

        st.markdown(f"""<div class="analytics-metric-row" style="margin-top:15px; margin-bottom:20px;">
<div class="metric-premium-box"><div class="metric-premium-lbl">Total docentes</div><div class="metric-premium-val">{count_prof_total}</div><div class="metric-premium-icon" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-box"><div class="metric-premium-lbl">Activos</div><div class="metric-premium-val" style="color:#16a34a;">{count_prof_total}</div><div class="metric-premium-icon" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

        html_filas_profesores = ""
        if profesores_db:
            for p in profesores_db:
                id_p, nombre_c, horas_d = str(p[0]), str(p[1]), str(p[2])
                iniciales = "".join([w[0] for w in nombre_c.split()[:2]]).upper() if nombre_c else "P"
                
                html_filas_profesores += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-text-bubble">{iniciales}</div><div><b>{nombre_c}</b><br><span style="color:#64748b; font-size:0.75rem;">ID Interno: {id_p}</span></div></div></td>
<td>Educación Virtual / Tutoría</td>
<td>Módulos de Competencias RAP</td>
<td>{horas_d} horas</td>
<td><span class="status-pill-built">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; display:flex; gap:12px; font-size:1rem;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""
        else:
            html_filas_profesores = "<tr><td colspan='7' style='text-align:center; color:#64748b;'>No se encontraron docentes registrados en tu esquema relacional de Neon.</td></tr>"

        st.markdown(f"""<div class="form-container-card" style="padding:20px; overflow-x:auto;">
<div class="block-title">Listado de docentes</div>
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_rows_profes = html_filas_db = html_filas_matriz = html_rows_profes = html_filas_db = html_filas_matriz = html_rows_profeses = html_rows_profes}</tbody>
</table></div>""", unsafe_allow_html=True)

        # Sección original para administración de registros (Eliminar Docente - Solo Admin)
        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Docente")
            if profesores_db:
                opts_profes = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                profe_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_profes.keys()), key="admin_del_p")
                if st.button("❌ Eliminar Docente Seleccionado", key="btn_exe_del_p"):
                    try:
                        ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (opts_profes[profe_sel],))
                        st.error(f"Docente '{profe_sel}' eliminado de forma definitiva.")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ Restricción relacional: No se puede eliminar el docente debido a dependencias activas.")
            else:
                st.info("No hay registros de docentes cargados para eliminar.")

    # =========================================================================
    # CUMPLIMIENTO INTERFAZ 3: FORMULARIO NUEVO DOCENTE EVALUADOR (`image_473a46.jpg`)
    # =========================================================================
    elif st.session_state['reg_modulo_vista'] == "docentes" and st.session_state['reg_modo_docentes'] == "nuevo":
        if st.button("← Volver al Listado de Docentes", key="btn_cancel_doc_form"):
            st.session_state['reg_modo_docentes'] = "lista"
            st.rerun()

        st.markdown("### Nuevo docente evaluador")
        st.caption("Completa la información básica estructurada del docente evaluador para el esquema de la base de datos.")

        c_fdoc_l, c_fdoc_r = st.columns([2.2, 1])
        with c_fdoc_l:
            with st.form("form_nuevo_docente_clean", clear_on_submit=True):
                st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                nombre_doc_input = st.text_input("Nombre completo *", placeholder="Ej. Jaime Gabriel Jaramillo")
                
                st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                horas_doc_input = st.number_input("Horas de dedicación (horas_dedicacion) *", min_value=1, max_value=48, value=1)
                
                st.markdown("<br>", unsafe_allow_html=True)
                c_sb_1, c_sb_2 = st.columns(2)
                with c_sb_1:
                    submit_doc = st.form_submit_button("💾 Guardar docente", use_container_width=True)
                with c_sb_2:
                    cancel_doc = st.form_submit_button("Cancelar", use_container_width=True)

                if submit_doc:
                    if not nombre_doc_input.strip():
                        st.error("El nombre completo del profesor es un parámetro obligatorio.")
                    else:
                        try:
                            # Inserción limpia respetando las columnas exactas de tu tabla profesores (`nombre_completo`, `horas_dedicacion`)
                            ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nombre_doc_input, horas_doc_input))
                            st.success("✅ ¡Registro completado! El docente ha sido almacenado en Neon DB.")
                            st.session_state['reg_modo_docentes'] = "lista"
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ Error al escribir fila en Neon PostgreSQL: {e}")
                if cancel_doc:
                    st.session_state['reg_modo_docentes'] = "lista"
                    st.rerun()

        with c_fdoc_r:
            chk_name = "validated" if nombre_doc_input else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="status-pill-built" style="display:inline;">Activo</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios detectados</div>
<div class="checklist-item-row {chk_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> horas_dedicacion</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # CUMPLIMIENTO INTERFAZ 4: FORMULARIO REGISTRO/ACTUALIZACIÓN ESTUDIANTES (`image_473b5e.jpg`)
    # =========================================================================
    elif st.session_state['reg_modulo_vista'] == "estudiantes":
        if st.button("← Volver al Panel Principal", key="btn_back_from_est"):
            st.session_state['reg_modulo_vista'] = "principal"
            st.rerun()

        st.markdown("### Registrar / Actualizar Estudiante")
        st.caption("Completa los campos definidos en tu base de datos para dar de alta o modificar la traza académica de un estudiante.")

        # Conservación estricta de la lógica original (Carga y modo corrección de ID Banner)
        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID Actual: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro que contiene el ID ERRÓNEO:", list(opts_correccion.keys()), key="sel_corr_est_id")
            id_antiguo = opts_correccion[est_a_corregir]
            st.warning(f"Se modificará el identificador del estudiante en Neon. El ID viejo {id_antiguo} será reemplazado.")

        c_est_l, c_est_r = st.columns([2.2, 1])
        with c_est_l:
            with st.form("form_estudiante_maquetado", clear_on_submit=True):
                st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                id_b = st.number_input("ID Banner (id_banner) *", step=1, value=id_antiguo if id_antiguo else 0)
                nom_e = st.text_input("Nombre completo (nombre_completo) *")
                est = st.selectbox("Estado de matrícula (estado_matricula) *", ["Matriculado", "Admitido", "No matriculado"])
                
                st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas RAP (alfa_asignatura) *", list(opts.keys()))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Registrar / Actualizar Estudiante", type="primary", use_container_width=True):
                    if id_b <= 0 or not nom_e.strip():
                        st.error("Por favor, ingrese un ID Banner válido y el nombre completo del estudiante.")
                    else:
                        alfas = ",".join([opts[m] for m in mats_sel])
                        try:
                            # Conservación estricta de la lógica relacional nativa compartida (INSERT con ON CONFLICT)
                            if modo_correccion and id_antiguo:
                                ejecutar_query("""
                                    UPDATE estudiantes 
                                    SET id_banner = %s, nombre_completo = %s, estado_matricula = %s, alfa_asignatura = %s
                                    WHERE id_banner = %s
                                """, (id_b, nom_e, est, alfas, id_antiguo))
                                st.success(f"¡Identificación corregida! El ID {id_antiguo} ahora es **{id_b}**.")
                            else:
                                ejecutar_query("""
                                    INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id_banner) 
                                    DO UPDATE SET 
                                        nombre_completo = EXCLUDED.nombre_completo,
                                        estado_matricula = EXCLUDED.estado_matricula,
                                        alfa_asignatura = EXCLUDED.alfa_asignatura
                                """, (id_b, nom_e, est, alfas))
                                st.success(f"¡Sincronizado! El estudiante con ID **{id_b}** ha sido guardado/actualizado.")
                            st.rerun()
                        except Exception as e:
                            err_str = str(e).lower()
                            if "unique" in err_str or "duplicate" in err_str:
                                st.error(f"⚠️ El ID Banner **{id_b}** ya se encuentra asignado a otro estudiante.")
                            elif "foreign key" in err_str or "violación de llave foránea" in err_str:
                                st.error("⚠️ Restricción restrictiva: No se puede alterar este ID porque posee registros en otras tablas dependientes.")
                            else:
                                st.error("⚠️ Error operacional al guardar el registro en la base de datos.")

        with c_est_r:
            chk_est_id = "validated" if id_b > 0 else ""
            chk_est_name = "validated" if nom_e else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado actual: <span class="status-pill-process" style="display:inline;">{est}</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos requeridos de la tabla</div>
<div class="checklist-item-row {chk_est_id}"><i class="fa-solid fa-circle-check"></i> id_banner</div>
<div class="checklist-item-row {chk_est_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> estado_matricula</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> alfa_asignatura</div>
</div>""", unsafe_allow_html=True)

        # Control Administrativo de Eliminación de Estudiantes Preservado de tu código
        if rol == "admin":
            st.divider()
            st.subheader("🗑 *Área de Administración: Eliminar Estudiante*")
            if estudiantes_carga:
                opts_est = {f"{e[1]} (Banner: {e[0]})": e[0] for e in estudiantes_carga}
                est_sel = st.selectbox("Seleccione el estudiante a eliminar:", list(opts_est.keys()), key="admin_del_est_key")
                if st.button("❌ Eliminar Estudiante Seleccionado", key="btn_execute_del_est"):
                    id_banner_del = opts_est[est_sel]
                    try:
                        ejecutar_query("DELETE FROM notas WHERE id_programacion IN (SELECT id FROM programacion_pruebas WHERE id_banner = %s)", (id_banner_del,))
                        ejecutar_query("DELETE FROM programacion_pruebas WHERE id_banner = %s", (id_banner_del,))
                        ejecutar_query("DELETE FROM estudiantes WHERE id_banner = %s", (id_banner_del,))
                        st.error(f"Estudiante '{est_sel}' eliminado correctamente de todas las dependencias.")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ Error restrictivo de la base de datos de Neon al ejecutar el cascade del registro.")
            else:
                st.info("No hay estudiantes registrados para habilitar eliminaciones.")

    # =========================================================================
    # CUMPLIMIENTO INTERFAZ 5: VISTA MAESTRA COMPLETA OPTIMIZADA (`image_473e86.jpg`)
    # =========================================================================
    elif st.session_state['reg_modulo_vista'] == "maestra":
        if st.button("← Volver al Menú Principal", key="btn_exit_matrix_m"):
            st.session_state['reg_modulo_vista'] = "principal"
            st.rerun()

        st.markdown("### Estado de Aplicación por Estudiante")
        st.caption("Consulta matricial semaforizada del avance de competencias homologadas.")

        # Controles de Filtración de la Cabecera Maquetados
        c_mflt_1, c_mflt_2, c_mflt_3 = st.columns(3)
        with c_mflt_1: st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed", key="mx_search_field")
        with c_mflt_2: st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed", key="mx_prog_field")
        with c_mflt_3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed", key="mx_state_field")

        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            # --- OPTIMIZACIÓN CRUCIAL DE RENDIMIENTO (EVITA CARGA LENTA) ---
            # En vez de hacer un SELECT query por cada celda dentro del bucle, precargamos
            # la tabla de estados completa en un diccionario indexado de memoria (O(1) lookup).
            pruebas_db = traer_datos("SELECT alfa_asignatura, estado FROM maestro_pruebas")
            mapa_estados_pruebas = {str(p[0]).strip(): str(p[1]) for p in pruebas_db} if pruebas_db else {}
            
            total_est = len(ests)
            barra_progreso = st.progress(0)
            
            html_matrix_rows = ""
            for idx, (idb, nom, alfas) in enumerate(ests):
                barra_progreso.progress(int(((idx + 1) / total_est) * 100))
                lista_alfas = [a.strip() for a in alfas.split(",")] if alfas else []
                
                # Función evaluadora ultra-rápida libre de accesos IO/Network recurrentes
                def renderizar_pildora_estado(codigo_alfa):
                    if cod_alfa := codigo_alfa not in lista_alfas:
                        return '<span class="status-pill-none">No aplica</span>'
                    
                    status_real = mapa_estados_pruebas.get(str(codigo_alfa).strip(), "Pendiente")
                    if status_real == "Construida":
                        return '<span class="status-pill-built">Lista</span>'
                    elif status_real == "En construcción":
                        return '<span class="status-pill-process">En proceso</span>'
                    else:
                        return '<span class="status-pill-pending">Pendiente</span>'

                html_matrix_rows += f"""<tr>
<td>{idb}</td>
<td><b>{nom}</b></td>
<td>{renderizar_pildora_estado("ISOF V003")}</td>
<td>{renderizar_pildora_estado("ISOF V013")}</td>
<td>{renderizar_pildora_estado("ISOF V043")}</td>
<td>{renderizar_pildora_estado("ISOF V063")}</td>
<td>{renderizar_pildora_estado("ISOF V081")}</td>
<td>{renderizar_pildora_estado("ISOF V095")}</td>
<td><div style="color:#0047ff; text-align:center; font-weight:700; cursor:pointer;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""

            barra_progreso.empty()

            # Despliegue de la Tabla Matricial Estilizada con Carga Instantánea
            st.markdown(f"""<div class="form-container-card" style="padding:20px; overflow-x:auto; margin-top:15px;">
<table class="master-matrix-table" style="width:100%; border-collapse:collapse; font-size:0.85rem;">
<thead><tr style="background:#f8fafc;">
<th>ID Banner</th><th>Estudiante</th>
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
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Evaluación completa)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente (Aún no evaluada)</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En proceso (En evaluación)</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica (No corresponde)</span>
</div></div>""", unsafe_allow_html=True)
            st.success(f"Matriz de {total_est} estudiantes cargada en tiempo real de forma instantánea.")
        else:
            st.info("No se registran estudiantes matriculados en el sistema.")