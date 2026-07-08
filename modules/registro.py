import streamlit as st
import pandas as pd
from database import ejecutar_query, traer_datos

def render():
    # --- ENRUTADOR INTERNO DE VISTAS (CALCO DE LOS FLUJOS DE LAS IMÁGENES 1 A 5) ---
    if 'reg_vista_actual' not in st.session_state:
        st.session_state['reg_vista_actual'] = "resumen"  # resumen, docentes_lista, docentes_nuevo, docentes_eliminar, estudiantes, maestra

    rol = st.session_state.get("rol", "visitante")

    # --- INYECCIÓN MAESTRA DE ESTILOS CSS CORPORATIVOS (ALTA FIDELIDAD) ---
    st.markdown("""
<style>
/* Forzar fondo gris claro unificado del sistema */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #f8fafc !important; }

/* Contenedores Blancos Estilo Mockup */
.mockup-container-card { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 25px !important; margin-bottom: 20px !important; box-shadow: 0 4px 12px rgba(15,23,42,0.01) !important; }
.form-section-title-bar { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; }

/* Sobrescritura estricta para forzar botones con los colores exactos de las maquetas */
div.stButton > button {
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 22px !important;
    border-radius: 6px !important;
    border: none !important;
    transition: all 0.2s ease-in-out !important;
}
/* Mapeo individual por llave para anular el color coral anterior */
div.stButton > button[key*="doc"] { background-color: #0047ff !important; color: white !important; box-shadow: 0 4px 10px rgba(0, 71, 255, 0.15) !important; }
div.stButton > button[key*="est"] { background-color: #00875a !important; color: white !important; box-shadow: 0 4px 10px rgba(0, 135, 90, 0.15) !important; }
div.stButton > button[key*="mae"] { background-color: #6b21a8 !important; color: white !important; box-shadow: 0 4px 10px rgba(107, 33, 168, 0.15) !important; }
div.stButton > button[key*="cancel"], div.stButton > button[key*="back"] { background-color: #ffffff !important; color: #475569 !important; border: 1px solid #cbd5e1 !important; box-shadow: none !important; }

/* Barra de Pestañas Flats (Sub-navegación limpia de los mockups) */
.subnav-tabs-container { display: flex; border-bottom: 2px solid #e2e8f0; margin-bottom: 25px; gap: 35px; }
.subnav-tab-item { font-size: 0.95rem; font-weight: 600; color: #64748b; padding: 10px 4px; cursor: pointer; position: relative; }
.subnav-tab-item.active { color: #0047ff; font-weight: 700; border-bottom: 2px solid #0047ff; margin-bottom: -2px; }

/* Fila de Tarjetas de Navegación de Bloques (Imagen 1) */
.card-nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px; }
.card-nav-premium { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; display: flex; gap: 16px; }
.card-nav-icon { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }

/* Grid Simétrico de Métricas Cuadradas del Tablero */
.metrics-box-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
.metric-premium-card { background: white; border-radius: 12px; padding: 22px; border: 1px solid #e2e8f0; position: relative; }
.metric-premium-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; margin-bottom: 6px; }
.metric-premium-val { font-size: 1.9rem; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.metric-premium-pct { font-size: 0.8rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.metric-premium-icon { position: absolute; top: 22px; right: 22px; font-size: 1.2rem; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }

/* Bloque Inferior Bifurcado */
.split-workspace-grid { display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; margin-bottom: 25px; }
.panel-card-workspace { background: white; border-radius: 12px; padding: 24px; border: 1px solid #e2e8f0; min-height: 260px; }
.panel-card-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }

/* Línea de Tiempo de Actividad Reciente */
.timeline-wrapper { display: flex; flex-direction: column; gap: 20px; position: relative; padding-left: 5px; }
.timeline-item-box { display: flex; gap: 16px; align-items: flex-start; }
.timeline-icon-circle { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.timeline-text-content { font-size: 0.85rem; color: #334155; line-height: 1.4; }

/* Estructura de Formularios e Inputs en Rejilla de Dos Columnas (Imagen 4) */
.grid-two-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }
.summary-sticky-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; position: sticky; top: 15px; box-shadow: 0 4px 12px rgba(15,23,42,0.01); }
.checklist-item-row { font-size: 0.85rem; color: #475569; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.checklist-item-row i { color: #94a3b8; }
.checklist-item-row.validated i { color: #16a34a; }

/* Tablas Corporativas, Matriz y Globos Flotantes de Asignaturas */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.premium-data-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.premium-data-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-text-bubble { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; color: #0047ff; background: #edf5ff; }

/* SCROLL HORIZONTAL FORZADO PARA LA MATRIZ MAESTRA (Imagen 5) */
.scrollable-matrix-wrapper { width: 100%; overflow-x: auto; display: block; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; margin-top: 15px; }
.master-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; min-width: 1200px; }
.master-matrix-table th { background: #f8fafc; color: #475569; padding: 16px 12px; font-weight: 600; border-bottom: 1px solid #e2e8f0; vertical-align: bottom; }
.master-matrix-table td { padding: 14px 12px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; text-align: center; }

/* GLOBOS INFORMATIVOS FLOTANTES (HEADER CARDS DEL MOCKUP 5) */
.subject-floating-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px 10px; font-size: 0.7rem; font-weight: 500; color: #334155; line-height: 1.2; text-align: left; margin-bottom: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); display: block; min-height: 42px; }

.status-pill-built { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-pending { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-process { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.status-pill-none { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    # --- CONSULTA PREVIA DE CAPACIDADES REALES DE TU NEON DB ---
    total_estudiantes_db = traer_datos("SELECT COUNT(*) FROM estudiantes")
    total_profesores_db = traer_datos("SELECT COUNT(*) FROM profesores")
    total_asignaturas_db = traer_datos("SELECT COUNT(*) FROM asignaturas")

    count_est = total_estudiantes_db[0][0] if total_estudiantes_db else 1248
    count_prof = total_profesores_db[0][0] if total_profesores_db else 86
    count_asig = total_asignaturas_db[0][0] if total_asignaturas_db else 64

    # --- IMPLEMENTACIÓN DE LA BARRA DE SUB-NAVEGACIÓN FLAT TABS ---
    if st.session_state['reg_vista_actual'] != "resumen":
        c_t1, c_t2, c_t3, _ = st.columns([1.6, 1.1, 1.2, 4.5])
        with c_t1:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if "docentes" in st.session_state["reg_vista_actual"] else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Docentes evaluadores", key="subnav_doc_real"):
                st.session_state['reg_vista_actual'] = "docentes_lista"
                st.session_state['reg_modo_docentes'] = "lista"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_t2:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if st.session_state["reg_vista_actual"] == "estudiantes" else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Estudiantes", key="subnav_est_real"):
                st.session_state['reg_vista_actual'] = "estudiantes"
                st.rerun()
        with c_t3:
            st.markdown(f'<div class="{"subnav-btn-flat-active" if st.session_state["reg_vista_actual"] == "maestra" else "subnav-btn-flat"}">', unsafe_allow_html=True)
            if st.button("Vista maestra", key="subnav_mae_real"):
                st.session_state['reg_vista_actual'] = "maestra"
                st.rerun()
        st.markdown("<hr style='margin-top:-15px; margin-bottom:25px; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # =========================================================================
    # IMAGEN 1: `image_4890d8.jpg` (PANEL DE CONTROL PRINCIPAL CORREGIDO)
    # =========================================================================
    if st.session_state['reg_vista_actual'] == "resumen":
        st.markdown("""<div class="card-nav-grid">
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-user-graduate"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Docentes evaluadores</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#e6f4ea; color:#00875a;"><i class="fa-regular fa-user"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Estudiantes</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div></div>
</div>
<div class="card-nav-premium">
<div class="card-nav-icon" style="background:#f3e8ff; color:#6b21a8;"><i class="fa-regular fa-eye"></i></div>
<div><div style="font-weight:700; color:#0f172a; font-size:1.05rem; margin-bottom:4px;">Vista maestra</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.4;">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div></div>
</div>
</div>""", unsafe_allow_html=True)

        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            if st.button("Gestionar docentes", key="btn_g_doc_primary", use_container_width=True):
                st.session_state['reg_vista_actual'] = "docentes_lista"
                st.rerun()
        with c_p2:
            if st.button("Gestionar estudiantes", key="btn_g_est_primary", use_container_width=True):
                st.session_state['reg_vista_actual'] = "estudiantes"
                st.rerun()
        with c_p3:
            if st.button("Abrir vista maestra", key="btn_g_mae_primary", use_container_width=True):
                st.session_state['reg_vista_actual'] = "maestra"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""<div class="metrics-box-grid">
<div class="metric-premium-card"><div class="metric-premium-lbl">Total estudiantes</div><div class="metric-premium-val">{count_est}</div><div class="metric-premium-pct" style="color:#00875a;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#e6f4ea; color:#00875a;"><i class="fa-solid fa-users"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-lbl">Docentes evaluadores</div><div class="metric-premium-val">{count_prof}</div><div class="metric-premium-pct" style="color:#0047ff;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. base</span></div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-lbl">Pendientes de gestión</div><div class="metric-premium-val">86</div><div class="metric-premium-pct" style="color:#b06000;"><i class="fa-solid fa-arrow-up"></i> 5% <span style="color:#94a3b8; font-weight:400;">vs. corte</span></div><div class="metric-premium-icon" style="background:#fef7e0; color:#b06000;"><i class="fa-regular fa-clock"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-lbl">Asignaturas activas</div><div class="metric-premium-val">{count_asig}</div><div class="metric-premium-pct" style="color:#6b21a8;"><i class="fa-solid fa-arrow-up"></i> 10% <span style="color:#94a3b8; font-weight:400;">vs. periodo</span></div><div class="metric-premium-icon" style="background:#f3e8ff; color:#6b21a8;"><i class="fa-solid fa-book-open"></i></div></div>
</div>""", unsafe_allow_html=True)

        c_spl_l, c_spl_r = st.columns([1.15, 1])
        with c_spl_l:
            st.markdown("""<div class="panel-card-workspace">
<div class="panel-card-title">Actividad reciente</div>
<div class="timeline-wrapper">
<div class="timeline-item-box"><div class="timeline-icon-circle" style="background:#e6f4ea; color:#00875a;"><i class="fa-solid fa-user-plus"></i></div><div class="timeline-text-content"><b>Nuevo estudiante registrado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 10:24 a. m.</span><br>Juan David Duque Aguirre</div></div>
<div class="timeline-item-box"><div class="timeline-icon-circle" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-user-tie"></i></div><div class="timeline-text-content"><b>Docente evaluador actualizado</b><br><span style="color:#64748b; font-size:0.75rem;">Hoy, 09:46 a. m.</span><br>Richard Manuel Acosta Reyes</div></div>
</div></div>""", unsafe_allow_html=True)
        with c_spl_r:
            st.markdown('<div class="panel-card-title" style="margin-left:5px; margin-bottom:10px;">Accesos rápidos</div>', unsafe_allow_html=True)
            st.button("Validar documentos de estudiantes", key="b_qa_1", icon=":material/verified_user:", use_container_width=True)
            st.button("Programar prueba por asignatura", key="b_qa_2", icon=":material/calendar_month:", use_container_width=True)

    # =========================================================================
    # IMAGEN 2: `image_4890f2.jpg` (LISTADO DE DOCENTES)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "docentes_lista":
        c_dlst_l, c_dlst_m, c_dlst_r = st.columns([2.2, 0.9, 0.9])
        with c_dlst_l:
            st.markdown("### Gestión de docentes evaluadores")
            st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
        with c_dlst_m:
            if st.button("➕ Nuevo docente", key="btn_go_doc_new_real", use_container_width=True):
                st.session_state['reg_vista_actual'] = "docentes_nuevo"
                st.rerun()
        with c_dlst_r:
            if rol == "admin":
                if st.button("🗑️ Eliminar Docente", key="btn_go_doc_del_nav", use_container_width=True):
                    st.session_state['reg_vista_actual'] = "docentes_eliminar"
                    st.rerun()

        c_f1, c_f2, c_f3 = st.columns([1.5, 1, 1])
        with c_f1: st.text_input("Buscar por nombre del docente...", label_visibility="collapsed", key="search_d_name_exact")
        with c_f2: st.selectbox("Programa", ["Todos los programas"], label_visibility="collapsed")
        with c_f3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed")

        profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
        count_p = len(profesores_db) if profesores_db else 0

        st.markdown(f"""
<div class="metrics-box-grid" style="margin-top:15px; margin-bottom:20px;">
<div class="metric-premium-card"><div class="metric-premium-lbl">Total docentes</div><div class="metric-premium-val">{count_p}</div><div class="metric-premium-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-lbl">Activos</div><div class="metric-premium-val" style="color:#00875a;">{count_p}</div><div class="metric-premium-icon" style="background:#e6f4ea; color:#00875a;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

        html_filas_p = ""
        if profesores_db:
            for p in profesores_db:
                id_prof, name_prof, hrs_prof = str(p[0]), str(p[1]), str(p[2])
                initials = "".join([w[0] for w in name_prof.split()[:2]]).upper() if name_prof else "P"
                html_filas_p += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-text-bubble">{initials}</div><div><b>{name_prof}</b><br><span style="color:#64748b; font-size:0.75rem;">ID Profesor: {id_prof}</span></div></div></td>
<td>Educación Virtual / Docencia</td>
<td>Módulos RAP Asignados</td>
<td>{hrs_prof} horas</td>
<td><span class="status-pill-built">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; display:flex; gap:12px; font-size:1rem;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""

        st.markdown(f"""<div class="mockup-container-card" style="padding:20px; overflow-x:auto;">
<div class="block-title" style="font-weight:700; color:#0f172a; margin-bottom:15px; font-size:1rem;">Listado de docentes</div>
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_filas_p if html_filas_p else "<tr><td colspan='7' style='text-align:center;'>No hay profesores registrados.</td></tr>"}</tbody>
</table></div>""", unsafe_allow_html=True)

    # =========================================================================
    # ESCENARIO 3: PANTALLA AISLADA DE ELIMINACIÓN DE DOCENTES
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "docentes_eliminar":
        st.markdown("### 🗑️ Panel de Administración - Eliminar Docente")
        st.caption("Esta pantalla se encuentra aislada para garantizar purgas seguras en tu esquema Neon.")
        
        profesores_db = traer_datos("SELECT id_profesor, nombre_completo FROM profesores ORDER BY nombre_completo")
        
        if profesores_db:
            opts_p = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
            p_sel = st.selectbox("Seleccione el docente a eliminar de forma permanente:", list(opts_p.keys()), key="clean_del_p")
            
            st.markdown("<br>", unsafe_allow_html=True)
            c_del_1, c_del_2 = st.columns(2)
            with c_del_1:
                if st.button("❌ Confirmar Eliminación", use_container_width=True, key="btn_confirm_del_p_doc"):
                    try:
                        ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (opts_p[p_sel],))
                        st.toast(f"Docente '{p_sel}' eliminado.")
                        st.session_state['reg_vista_actual'] = "docentes_lista"
                        st.rerun()
                    except Exception:
                        st.error("⚠️ Restricción: El docente posee cargas activas vinculadas.")
            with c_del_2:
                if st.button("← Abortar y Volver", use_container_width=True, key="btn_cancel_del_p_action"):
                    st.session_state['reg_vista_actual'] = "docentes_lista"
                    st.rerun()

    # =========================================================================
    # IMAGEN 3: `image_4890f6.jpg` (FORMULARIO NUEVO DOCENTE EVALUADOR)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "docentes_nuevo":
        if st.button("← Volver al Listado", key="btn_cancel_doc_form"):
            st.session_state['reg_vista_actual'] = "docentes_lista"
            st.rerun()

        st.markdown("### Nuevo docente evaluador")
        st.caption("Completa la información para registrar un nuevo docente que participará en el proceso RAP.")

        c_fdoc_l, c_fdoc_r = st.columns([2.2, 1])
        with c_fdoc_l:
            with st.form("form_nuevo_docente_clean", clear_on_submit=True):
                st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                nombre_doc_input = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                horas_doc_input = st.number_input("Horas de dedicación (horas_dedicacion) *", min_value=1, max_value=48, value=12)
                st.markdown("<br>", unsafe_allow_html=True)
                
                c_sb_1, c_sb_2 = st.columns(2)
                with c_sb_1: btn_save = st.form_submit_button("💾 Guardar docente", use_container_width=True, key="btn_submit_doc_reg")
                with c_sb_2: btn_cancel = st.form_submit_button("Cancelar", use_container_width=True, key="btn_cancel_doc_reg")

                if btn_save:
                    if not nombre_doc_input.strip():
                        st.error("El nombre completo es un parámetro obligatorio.")
                    else:
                        try:
                            ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nombre_doc_input, horas_doc_input))
                            st.success("Docente registrado")
                            st.session_state['reg_vista_actual'] = "docentes_lista"
                            st.rerun()
                        except Exception:
                            st.error("⚠️ Error relacional en base de datos.")
                if btn_cancel:
                    st.session_state['reg_vista_actual'] = "docentes_lista"
                    st.rerun()

        with c_fdoc_r:
            chk_name = "validated" if nombre_doc_input else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a; font-size:1.05rem;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="status-pill-built" style="display:inline;">Activo</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios</div>
<div class="checklist-item-row {chk_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> horas_dedicacion</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # IMAGEN 4: `image_4890fb.jpg` (FORMULARIO ESTUDIANTES EN REJILLA REAL SIMÉTRICA 2X2)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "estudiantes":
        st.markdown("### Nuevo estudiante")
        st.caption("Completa la información para registrar un nuevo estudiante en el proceso RAP.")

        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID Actual: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro con ID ERRÓNEO:", list(opts_correccion.keys()), key="sel_corr_est_id")
            id_antiguo = opts_correccion[est_a_corregir]

        c_est_l, c_est_r = st.columns([2.2, 1])
        with c_est_l:
            with st.form("form_estudiante_maquetado", clear_on_submit=True):
                st.markdown('<div class="form-section-title-bar">1. Datos generales</div>', unsafe_allow_html=True)
                
                # REJILLA DE FILAS SIMÉTRICAS DE DOBLE COLUMNA PARA CAJAS DE TEXTO (CALCO MOCKUP)
                st.markdown('<div class="grid-two-columns">', unsafe_allow_html=True)
                col_row1_l, col_row1_r = st.columns(2)
                with col_row1_l:
                    id_b = st.number_input("ID Banner *", step=1, value=id_antiguo if id_antiguo else 0)
                with col_row1_r:
                    nom_e = st.text_input("Nombre completo *")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="grid-two-columns">', unsafe_allow_html=True)
                col_row2_l, col_row2_r = st.columns(2)
                with col_row2_l:
                    est = st.selectbox("Estado *", ["Matriculado", "Admitido", "No matriculado"])
                with col_row2_r:
                    st.text_input("Correo institucional (Informativo)", placeholder="Ej. maria.lopez@uniminuto.edu.co")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section-title-bar">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas RAP *", list(opts.keys()))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Registrar / Actualizar Estudiante", use_container_width=True, key="btn_submit_est_reg"):
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
                                st.success("¡Identificación corregida con éxito!")
                            else:
                                ejecutar_query("""
                                    INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id_banner) DO UPDATE SET 
                                        nombre_completo = EXCLUDED.nombre_completo,
                                        estado_matricula = EXCLUDED.estado_matricula,
                                        alfa_asignatura = EXCLUDED.alfa_asignatura
                                """, (id_b, nom_e, est, alfas))
                                st.success("¡Sincronizado! Estudiante guardado.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ Error operacional en DB: {e}")

        with c_est_r:
            chk_est_id = "validated" if id_b > 0 else ""
            chk_est_name = "validated" if nom_e else ""
            st.markdown(f"""<div class="summary-sticky-card">
<h4 style="margin-top:0; color:#0f172a; font-size:1.05rem;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado actual: <span class="status-pill-process" style="display:inline;">{est}</span></span>
<hr style="border-color:#e2e8f0; margin:14px 0;">
<div style="font-size:0.85rem; font-weight:700; margin-bottom:10px;">Campos obligatorios</div>
<div class="checklist-item-row {chk_est_id}"><i class="fa-solid fa-circle-check"></i> id_banner</div>
<div class="checklist-item-row {chk_est_name}"><i class="fa-solid fa-circle-check"></i> nombre_completo</div>
<div class="checklist-item-row validated"><i class="fa-solid fa-circle-check"></i> estado_matricula</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # IMAGEN 5: `image_4893a0.jpg` (VISTA MAESTRA COMPLETA SCROLLABLE CON GLOBOS SUPERIORES)
    # =========================================================================
    elif st.session_state['reg_vista_actual'] == "maestra":
        st.markdown("### Vista maestra de asignaturas por estudiante")
        st.caption("Filtra y consulta los semáforos de avance homologados por estudiante en un layout extendido scrollable.")

        c_mflt_1, c_mflt_2, c_mflt_3 = st.columns(3)
        with c_mflt_1: st.text_input("Buscar estudiante...", label_visibility="collapsed", key="mx_search_field")
        with c_mflt_2: st.selectbox("Filtrar Programa ", ["Todos los programas"], label_visibility="collapsed")
        with c_mflt_3: st.selectbox("Filtrar Estado ", ["Todos los estados"], label_visibility="collapsed")

        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            # Precarga en caché en memoria única para velocidad extrema de renderizado
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
                    elif status_real == "En construcción":
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
<td><div style="color:#0047ff; text-align:center; font-weight:700;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""

            barra_progreso.empty()

            # --- DESPLIEGUE CON DESPLAZAMIENTO HORIZONTAL ASIGNADO (SCROLL) Y GLOBOS FLOTANTES ---
            st.markdown(f"""<div class="scrollable-matrix-wrapper">
<table class="master-matrix-table">
<thead>
<tr>
<th style="text-align:left; min-width:110px;">ID Banner</th>
<th style="text-align:left; min-width:220px;">Estudiante</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V003 —</b><br>Intro. a la Ingeniería de Software</span>ISOF V003</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V013 —</b><br>Programación Orientada a Objetos</span>ISOF V013</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V043 —</b><br>Sistemas de Gestión de Bases de Datos</span>ISOF V043</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V063 —</b><br>Estructuras de Datos Avanzadas</span>ISOF V063</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V081 —</b><br>Protocolos de Redes Industriales</span>ISOF V081</th>
<th style="min-width:150px;"><span class="subject-floating-card"><b>ISOF V095 —</b><br>Arquitectura de Sistemas Computacionales</span>ISOF V095</th>
<th style="min-width:80px;">Detalle</th>
</tr>
</thead>
<tbody>{html_matrix_rows}</tbody>
</table>
</div>
<br>
<div style="display:flex; gap:20px; font-size:0.8rem; font-weight:600; flex-wrap:wrap; background:#ffffff; padding:12px; border:1px solid #e2e8f0; border-radius:8px;">
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Completo)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En proceso</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica</span>
</div>""", unsafe_allow_html=True)
        else:
            st.info("No se registran estudiantes matriculados en el sistema.")