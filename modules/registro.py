import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    # --- INYECCIÓN DE CAPA ESTÉTICA PREMIUM E INMUNIDAD MARMDOWN ---
    st.markdown("""
<style>
/* Estilos del contenedor de formularios en secciones */
.form-container-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px; margin-bottom: 20px; }
.form-section-header { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 18px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; text-transform: uppercase; letter-spacing: 0.3px; }
.sidebar-summary-box { background: #fdfdfd; border: 1px solid #e2e8f0; border-radius: 16px; padding: 22px; position: sticky; top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); }

/* Matriz Maestra y Listados de Docentes */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.premium-data-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.premium-data-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-profile-circle { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; color: #0047ff; background: #edf5ff; }

/* Semáforos y Pills del Tablero Maestro */
.pill-status-built { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-pending { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-none { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    st.title("📝 Gestión de Registros")
    
    rol = st.session_state.get("role", st.session_state.get("rol", "visitante"))
    
    # Manejo de sub-navegación interactiva para alternar entre Lista y Formulario en la pestaña Docentes
    if "sub_modo_docentes" not in st.session_state:
        st.session_state["sub_modo_docentes"] = "lista"

    t1, t2, t3 = st.tabs(["👨‍🏫 Docentes", "🎓 Estudiantes", "🔍 Vista Maestro"])
    
    # =========================================================================
    # TAB 1: REGISTRO / LISTADO DE DOCENTES (Imagen 1 y Formulario de la Imagen)
    # =========================================================================
    with t1:
        if st.session_state["sub_modo_docentes"] == "lista":
            c_top_l, c_top_r = st.columns([3, 1])
            with c_top_l:
                st.subheader("Gestión de docentes evaluadores")
                st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
            with c_top_r:
                if st.button("➕ Nuevo docente", key="btn_go_form_doc", use_container_width=True, type="primary"):
                    st.session_state["sub_modo_docentes"] = "formulario"
                    st.rerun()

            # Obtención real de registros mediante tu módulo nativo
            profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
            
            # Tarjetas de KPI resumidas de la vista
            total_p = len(profesores_db) if profesores_db else 0
            st.markdown(f"""
<div class="metrics-row" style="margin-bottom:20px;">
<div class="metric-premium-card"><div class="metric-premium-title">Total docentes</div><div class="metric-premium-value">{total_p}</div><div class="metric-icon-box" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-title">Activos</div><div class="metric-premium-value" style="color:#16a34a;">{total_p}</div><div class="metric-icon-box" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

            html_rows_profes = ""
            if profesores_db:
                for p in profesores_db:
                    id_prof = str(p[0])
                    nombre = str(p[1])
                    horas = str(p[2])
                    iniciales = "".join([w[0] for w in nombre.split()[:2]]).upper() if nombre else "P"
                    
                    html_rows_profes += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-profile-circle">{iniciales}</div><div><b>{nombre}</b><br><span style="color:#64748b; font-size:0.75rem;">ID: {id_prof}</span></div></div></td>
<td>Docencia Virtual / Tutoría</td>
<td>Módulos de Competencias RAP</td>
<td>{horas} horas</td>
<td><span class="pill-status-built">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; font-size:1rem; display:flex; gap:10px;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""

            if html_rows_profes == "":
                html_rows_profes = "<tr><td colspan='7' style='text-align:center; color:#64748b;'>No hay docentes registrados en la base de datos actualmente.</td></tr>"

            st.markdown(f"""<div class="form-container-card" style="padding:20px; overflow-x:auto;">
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_rows_profes}</tbody>
</table></div>""", unsafe_allow_html=True)

            # Control de eliminación original preservado intacto (Solo Admin)
            if rol == "admin":
                st.divider()
                st.subheader("🗑️ Eliminar Docente")
                if profesores_db:
                    opts_profes = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                    profe_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_profes.keys()), key="del_fe")
                    if st.button("❌ Eliminar Docente Seleccionado"):
                        id_profe_del = opts_profes[profe_sel]
                        try:
                            ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (id_profe_del,))
                            st.error(f"Docente '{profe_sel}' eliminado correctamente.")
                            st.rerun()
                        except Exception:
                            st.error("⚠️ No se puede eliminar este docente porque tiene cargas académicas o actividades vinculadas en el sistema.")
                else:
                    st.info("No hay docentes registrados para eliminar.")

        elif st.session_state["sub_modo_docentes"] == "formulario":
            if st.button("← Volver al Listado Maestro", key="back_to_list_doc"):
                st.session_state["sub_modo_docentes"] = "lista"
                st.rerun()

            st.subheader("Nuevo docente evaluador")
            st.caption("Completa la información para registrar un nuevo docente que participará en el proceso RAP.")

            col_form, col_summary = st.columns([2.2, 1])
            with col_form:
                with st.form("f_p", clear_on_submit=True):
                    st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                    nom_p = st.text_input("Nombre completo del Profesor *", placeholder="Ej. Jaime Gabriel Jaramillo")
                    
                    st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                    hrs = st.number_input("Horas de dedicación *", min_value=1, max_value=48, value=1)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    c_submit_1, c_submit_2 = st.columns(2)
                    with c_submit_1:
                        btn_save = st.form_submit_button("💾 Guardar docente")
                    with c_submit_2:
                        btn_cancel = st.form_submit_button("Cancelar")

                    if btn_save:
                        if not nom_p.strip():
                            st.error("El nombre del profesor no puede quedar vacío.")
                        else:
                            try:
                                ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nom_p, hrs))
                                st.success("Docente registrado con éxito en la base de datos.")
                                st.session_state["sub_modo_docentes"] = "lista"
                                st.rerun()
                            except Exception:
                                st.error("⚠️ Ocurrió un inconveniente al registrar el docente. Verifique los tipos de datos.")
                    if btn_cancel:
                        st.session_state["sub_modo_docentes"] = "lista"
                        st.rerun()

            with col_summary:
                st.markdown("""<div class="sidebar-summary-box">
<h4 style="margin-top:0;color:#0f172a;">Resumen de registro</h4>
<p style="font-size:0.82rem;color:#64748b;"><i class="fa-solid fa-id-badge"></i> Formulario de control de carga académica.</p>
<hr style="border-color:#e2e8f0; margin:12px 0;">
<div style="font-size:0.82rem;color:#475569;line-height:1.8;">
• <b>Estado:</b> <span class="pill-status-built">Activo</span><br>
• Los parámetros ingresados impactarán el volumen consolidado del proceso RAP.
</div></div>""", unsafe_allow_html=True)

    # =========================================================================
    # TAB 2: REGISTRO / ACTUALIZACIÓN DE ESTUDIANTES (Formulario image_46c5e9.jpg)
    # =========================================================================
    with t2:
        st.subheader("Registrar / Actualizar Estudiante")
        st.caption("Completa la información para registrar o actualizar un estudiante en el proceso RAP.")
        
        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID Actual: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro que contiene el ID ERRÓNEO:", list(opts_correccion.keys()))
            id_antiguo = opts_correccion[est_a_corregir]
            st.warning(f"Se modificará el identificador del estudiante. El ID viejo {id_antiguo} será reemplazado por el nuevo ID que digite en el formulario inferior.")

        col_est_form, col_est_summary = st.columns([2.2, 1])
        with col_est_form:
            with st.form("f_e", clear_on_submit=True):
                st.markdown('<div class="form-section-header">1. Datos generales</div>', unsafe_allow_html=True)
                id_b = st.number_input("ID Banner *", step=1, value=id_antiguo if id_antiguo else 0)
                nom_e = st.text_input("Nombre completo del Estudiante *")
                est = st.selectbox("Estado de matrícula *", ["Matriculado", "Admitido", "No matriculado"])
                
                st.markdown('<div class="form-section-header">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas RAP homologadas *", list(opts.keys()))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Registrar / Actualizar Estudiante", type="primary"):
                    if id_b <= 0 or not nom_e.strip():
                        st.error("Por favor, ingrese un ID Banner válido y el nombre del estudiante.")
                    else:
                        alfas = ",".join([opts[m] for m in mats_sel])
                        try:
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
                                st.success(f"¡Procesado correctamente! El estudiante con ID **{id_b}** ha sido guardado.")
                            st.rerun()
                        except Exception as e:
                            err_str = str(e).lower()
                            if "unique" in err_str or "duplicate" in err_str:
                                st.error(f"⚠️ El ID Banner **{id_b}** ya se encuentra asignado a otro estudiante.")
                            elif "foreign key" in err_str or "violación de llave foránea" in err_str:
                                st.error("⚠️ No es posible alterar esta identificación porque tiene exámenes o calificaciones asociadas.")
                            else:
                                st.error("⚠️ No se pudo procesar la solicitud. Verifique los campos.")

        with col_est_summary:
            st.markdown("""<div class="sidebar-summary-box">
<h4 style="margin-top:0;color:#0f172a;">Resumen de registro</h4>
<p style="font-size:0.82rem;color:#64748b;"><i class="fa-solid fa-user-graduate"></i> Matrícula y control de asignaturas.</p>
<hr style="border-color:#e2e8f0; margin:12px 0;">
<div style="font-size:0.82rem;color:#475569;line-height:1.8;">
• <b>Estado:</b> <span class="pill-status-built" style="background:#e8f0fe; color:#1a73e8;">Matriculado</span><br>
• Al guardar, se sincronizará la traza completa de la matriz en la pestaña 'Vista Maestro'.
</div></div>""", unsafe_allow_html=True)

        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Estudiante")
            if estudiantes_carga:
                opts_est = {f"{e[1]} (Banner: {e[0]})": e[0] for e in estudiantes_carga}
                est_sel = st.selectbox("Seleccione el estudiante a eliminar:", list(opts_est.keys()), key="del_est")
                if st.button("❌ Eliminar Estudiante Seleccionado"):
                    id_banner_del = opts_est[est_sel]
                    try:
                        ejecutar_query("DELETE FROM notas WHERE id_programacion IN (SELECT id FROM programacion_pruebas WHERE id_banner = %s)", (id_banner_del,))
                        ejecutar_query("DELETE FROM programacion_pruebas WHERE id_banner = %s", (id_banner_del,))
                        ejecutar_query("DELETE FROM estudiantes WHERE id_banner = %s", (id_banner_del,))
                        st.error(f"Estudiante '{est_sel}' eliminado correctamente.")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ Ocurrió un error restrictivo en la base de datos al intentar eliminar el registro.")
            else:
                st.info("No hay estudiantes registrados para eliminar.")

    # =========================================================================
    # TAB 3: VISTA MAESTRO MATRICIAL DE ASIGNATURAS (Matriz Semáforo image_46c65d.jpg)
    # =========================================================================
    with t3:
        st.subheader("Estado de Aplicación por Estudiante")
        st.caption("Consulta la vista consolidada de avance de competencias frente a las asignaturas del programa.")
        
        # Filtros de cabecera maquetados estéticamente
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1: st.text_input("Buscar estudiante", placeholder="Ej. Nombre o ID Banner...", label_visibility="collapsed", key="m_search")
        with c_m2: st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed", key="m_prog")
        with c_m3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed", key="m_state")

        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            total_estudiantes = len(ests)
            barra_progreso = st.progress(0)
            
            html_rows_matrix = ""
            for indice, (idb, nom, alfas) in enumerate(ests):
                porcentaje = int(((indice + 1) / total_estudiantes) * 100)
                barra_progreso.progress(porcentaje)
                
                lista_alfas = alfas.split(",") if alfas else []
                
                # Mapeo y evaluación de estados reales por asignatura en tu DB para rellenar la matriz
                def evaluar_alfa(target_alfa):
                    if target_alfa not in lista_alfas:
                        return '<span class="pill-status-none">No aplica</span>'
                    
                    info_materia = traer_datos("""
                        SELECT m.estado FROM asignaturas a 
                        LEFT JOIN maestro_pruebas m ON a.alfa = m.alfa_asignatura 
                        WHERE a.alfa = %s
                    """, (target_alfa,))
                    
                    status = info_materia[0][0] if info_materia and info_materia[0][0] else "Pendiente"
                    if status == "Construida":
                        return '<span class="pill-status-built">Lista</span>'
                    elif status == "En construcción":
                        return '<span class="pill-status-evaluacion">En proceso</span>'
                    else:
                        return '<span class="pill-status-pending">Pendiente</span>'

                html_rows_matrix += f"""<tr>
<td>{idb}</td>
<td><b>{nom}</b></td>
<td>{evaluar_alfa("ISOF V003")}</td>
<td>{evaluar_alfa("ISOF V013")}</td>
<td>{evaluar_alfa("ISOF V043")}</td>
<td>{evaluar_alfa("ISOF V063")}</td>
<td>{evaluar_alfa("ISOF V081")}</td>
<td>{evaluar_alfa("ISOF V095")}</td>
<td><div style="color:#0047ff; text-align:center; font-weight:700;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""

            barra_progreso.empty()

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
<tbody>{html_rows_matrix}</tbody>
</table>
<br>
<div style="display:flex; gap:20px; font-size:0.8rem; font-weight:600; flex-wrap:wrap; background:#f8fafc; padding:12px; border-radius:8px;">
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Evaluación completa)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente (Aún no evaluada)</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En proceso (En evaluación)</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica (No corresponde)</span>
</div></div>""", unsafe_allow_html=True)
            st.success(f"Se cargaron {total_estudiantes} estudiantes con éxito.")
        else:
            st.info("No hay estudiantes registrados en el sistema.")