import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    # --- INYECCIÓN DE ARQUITECTURA DE DISEÑO PREMIUM ---
    st.markdown("""
<style>
/* Estructura general de Cards y Formularios */
.premium-form-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; margin-bottom: 25px; }
.form-section-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.3px; }
.right-summary-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; position: sticky; top: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.01); }

/* Tabla e Iniciales estilo Avatar Bubble */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.premium-data-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.premium-data-table td { padding: 14px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
.avatar-bubble { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; color: #0047ff; background: #edf5ff; }

/* Semáforos e Indicadores de la Vista Maestra */
.matrix-pill-lista { background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.matrix-pill-pendiente { background: #fef7e0; color: #b06000; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.matrix-pill-proceso { background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.matrix-pill-noaplica { background: #f1f3f4; color: #5f6368; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }

/* Checklist de datos requeridos lateral */
.checklist-item { font-size: 0.85rem; color: #475569; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.checklist-item i { color: #94a3b8; }
.checklist-item.done i { color: #16a34a; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    # Inicialización estable de sub-estados para controlar las vistas de las imágenes compartidas
    if 'tab_registro_actual' not in st.session_state:
        st.session_state['tab_registro_actual'] = "Docentes"
    if 'view_docentes_modo' not in st.session_state:
        st.session_state['view_docentes_modo'] = "lista"

    rol = st.session_state.get("rol", "visitante")

    # --- BARRA DE NAVEGACIÓN SUPERIOR TIPO MOCKUP ---
    c_tb1, c_tb2, c_tb3, _ = st.columns([1.5, 1, 1.2, 4])
    with c_tb1:
        if st.button("Docentes evaluadores", use_container_width=True, type="primary" if st.session_state['tab_registro_actual'] == "Docentes" else "secondary"):
            st.session_state['tab_registro_actual'] = "Docentes"
            st.rerun()
    with c_tb2:
        if st.button("Estudiantes", use_container_width=True, type="primary" if st.session_state['tab_registro_actual'] == "Estudiantes" else "secondary"):
            st.session_state['tab_registro_actual'] = "Estudiantes"
            st.rerun()
    with c_tb3:
        if st.button("Vista maestra", use_container_width=True, type="primary" if st.session_state['tab_registro_actual'] == "Maestra" else "secondary"):
            st.session_state['tab_registro_actual'] = "Maestra"
            st.rerun()

    st.markdown("<hr style='margin-top:0; margin-bottom:25px; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # =========================================================================
    # CONFIGURACIÓN OPCIÓN 1: DOCENTES EVALUADORES
    # =========================================================================
    if st.session_state['tab_registro_actual'] == "Docentes":
        if st.session_state['view_docentes_modo'] == "lista":
            c_dl, c_dr = st.columns([3, 1])
            with c_dl:
                st.markdown("### Gestión de docentes evaluadores")
                st.caption("Registra, actualiza y administra los docentes que participan en el proceso RAP.")
            with c_dr:
                if st.button("➕ Nuevo docente", key="go_form_doc", use_container_width=True, type="primary"):
                    st.session_state['view_docentes_modo'] = "formulario"
                    st.rerun()

            # Extracción desde tu tabla real 'profesores'
            profesores_db = traer_datos("SELECT id_profesor, nombre_completo, horas_dedicacion FROM profesores ORDER BY nombre_completo")
            total_p = len(profesores_db) if profesores_db else 0
            
            st.markdown(f"""
<div class="metrics-row" style="margin-bottom:20px;">
<div class="metric-premium-card"><div class="metric-premium-title">Total docentes</div><div class="metric-premium-value">{total_p}</div><div class="metric-icon-box" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-id-badge"></i></div></div>
<div class="metric-premium-card"><div class="metric-premium-title">Activos</div><div class="metric-premium-value" style="color:#16a34a;">{total_p}</div><div class="metric-icon-box" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-circle-check"></i></div></div>
</div>""", unsafe_allow_html=True)

            html_rows = ""
            if profesores_db:
                for p in profesores_db:
                    id_p, nombre, horas = str(p[0]), str(p[1]), str(p[2])
                    iniciales = "".join([w[0] for w in nombre.split()[:2]]).upper() if nombre else "P"
                    html_rows += f"""<tr>
<td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar-bubble">{iniciales}</div><div><b>{nombre}</b><br><span style="color:#64748b; font-size:0.75rem;">ID Profesor: {id_p}</span></div></div></td>
<td>Administración / Ingeniería</td>
<td>Competencias Generales RAP</td>
<td>{horas} horas</td>
<td><span class="matrix-pill-lista">Activo</span></td>
<td>21/05/2025</td>
<td><div style="color:#1a73e8; display:flex; gap:12px;"><i class="fa-regular fa-eye"></i> <i class="fa-regular fa-pen-to-square"></i></div></td>
</tr>"""
            else:
                html_rows = "<tr><td colspan='7' style='text-align:center; color:#64748b;'>No hay docentes registrados en el sistema.</td></tr>"

            st.markdown(f"""<div class="premium-form-card" style="padding:20px; overflow-x:auto;">
<table class="premium-data-table">
<thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
<tbody>{html_rows}</tbody>
</table></div>""", unsafe_allow_html=True)

            if rol == "admin":
                st.divider()
                st.subheader("🗑️ Eliminar Docente")
                if profesores_db:
                    opts_profes = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                    profe_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_profes.keys()), key="del_fe_real")
                    if st.button("❌ Eliminar Docente Seleccionado"):
                        try:
                            ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (opts_profes[profe_sel],))
                            st.error(f"Docente '{profe_sel}' eliminado correctamente.")
                            st.rerun()
                        except Exception:
                            st.error("⚠️ Inconveniente restrictivo: El docente posee actividades asociadas.")

        elif st.session_state['view_docentes_modo'] == "formulario":
            if st.button("← Volver al Listado", key="back_doc_list"):
                st.session_state['view_docentes_modo'] = "lista"
                st.rerun()

            st.markdown("### Nuevo docente evaluador")
            st.caption("Completa la información básica para registrar un nuevo docente participante del proceso RAP.")

            col_l, col_r = st.columns([2.2, 1])
            with col_l:
                with st.form("f_p", clear_on_submit=True):
                    st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                    nom_p = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                    
                    st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                    hrs = st.number_input("Horas de dedicación asignadas *", min_value=1, max_value=48, value=1)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    c_b1, c_b2 = st.columns(2)
                    with c_b1:
                        btn_save = st.form_submit_button("💾 Guardar docente", use_container_width=True)
                    with c_b2:
                        btn_cancel = st.form_submit_button("Cancelar", use_container_width=True)

                    if btn_save:
                        if not nom_p.strip():
                            st.error("Por favor ingrese el nombre del docente.")
                        else:
                            try:
                                ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nom_p, hrs))
                                st.success("Docente registrado con éxito.")
                                st.session_state['view_docentes_modo'] = "lista"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                    if btn_cancel:
                        st.session_state['view_docentes_modo'] = "lista"
                        st.rerun()

            with col_r:
                # Checklist dinámico lateral basado en el texto digitado (Imagen 1)
                is_name = "done" if nom_p else ""
                st.markdown(f"""<div class="right-summary-card">
<h4 style="margin-top:0;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="matrix-pill-lista" style="display:inline;">Activo</span></span>
<hr style="border-color:#e2e8f0; margin:15px 0;">
<div class="block-title" style="font-size:0.85rem; margin-bottom:10px;">Datos requeridos</div>
<div class="checklist-item {is_name}"><i class="fa-solid fa-circle-check"></i> Nombre completo</div>
<div class="checklist-item done"><i class="fa-solid fa-circle-check"></i> Horas asignadas</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # CONFIGURACIÓN OPCIÓN 2: FORMULARIO ESTUDIANTES (Imagen 2)
    # =========================================================================
    elif st.session_state['tab_registro_actual'] == "Estudiantes":
        st.markdown("### Nuevo estudiante")
        st.caption("Completa la información obligatoria para registrar o actualizar un estudiante en la base de datos.")

        estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
        modo_correccion = st.checkbox("🔄 ¿Desea corregir un ID Banner que quedó mal digitado?")
        id_antiguo = None
        
        if modo_correccion and estudiantes_carga:
            opts_correccion = {f"{e[1]} (ID: {e[0]})": e[0] for e in estudiantes_carga}
            est_a_corregir = st.selectbox("Seleccione el registro con el ID ERRÓNEO:", list(opts_correccion.keys()))
            id_antiguo = opts_correccion[est_a_corregir]

        col_el, col_er = st.columns([2.2, 1])
        with col_el:
            with st.form("f_e", clear_on_submit=True):
                st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                id_b = st.number_input("ID Banner *", step=1, value=id_antiguo if id_antiguo else 0)
                nom_e = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                est = st.selectbox("Estado *", ["Matriculado", "Admitido", "No matriculado"])
                
                st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
                opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
                mats_sel = st.multiselect("Asignaturas RAP homologadas *", list(opts.keys()))
                
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
                                st.success("Identificación corregida con éxito.")
                            else:
                                ejecutar_query("""
                                    INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id_banner) DO UPDATE SET 
                                        nombre_completo = EXCLUDED.nombre_completo,
                                        estado_matricula = EXCLUDED.estado_matricula,
                                        alfa_asignatura = EXCLUDED.alfa_asignatura
                                """, (id_b, nom_e, est, alfas))
                                st.success("Estudiante procesado correctamente.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error relacional en DB: {e}")

        with col_er:
            is_id = "done" if id_b > 0 else ""
            is_name = "done" if nom_e else ""
            st.markdown(f"""<div class="right-summary-card">
<h4 style="margin-top:0;">Resumen de registro</h4>
<span style="font-size:0.85rem; color:#64748b;">Estado: <span class="matrix-pill-proceso" style="display:inline;">Matriculado</span></span>
<hr style="border-color:#e2e8f0; margin:15px 0;">
<div class="block-title" style="font-size:0.85rem; margin-bottom:10px;">Datos requeridos</div>
<div class="checklist-item {is_id}"><i class="fa-solid fa-circle-check"></i> ID Banner</div>
<div class="checklist-item {is_name}"><i class="fa-solid fa-circle-check"></i> Nombre completo</div>
<div class="checklist-item done"><i class="fa-solid fa-circle-check"></i> Asignaturas RAP</div>
</div>""", unsafe_allow_html=True)

        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Estudiante")
            if estudiantes_carga:
                opts_est = {f"{e[1]} (Banner: {e[0]})": e[0] for e in estudiantes_carga}
                est_sel = st.selectbox("Seleccione el estudiante a eliminar:", list(opts_est.keys()), key="del_est")
                if st.button("❌ Eliminar Estudiante Seleccionado"):
                    try:
                        id_del = opts_est[est_sel]
                        ejecutar_query("DELETE FROM notas WHERE id_programacion IN (SELECT id FROM programacion_pruebas WHERE id_banner = %s)", (id_del,))
                        ejecutar_query("DELETE FROM programacion_pruebas WHERE id_banner = %s", (id_del,))
                        ejecutar_query("DELETE FROM estudiantes WHERE id_banner = %s", (id_del,))
                        st.error("Registro eliminado.")
                        st.rerun()
                    except Exception:
                        st.error("Error de llaves foráneas en DB.")

    # =========================================================================
    # CONFIGURACIÓN OPCIÓN 3: VISTA MAESTRA (Matriz Semáforo de la Imagen 3)
    # =========================================================================
    elif st.session_state['tab_registro_actual'] == "Maestra":
        st.markdown("### Vista maestra de asignaturas por estudiante")
        st.caption("Filtra y consulta en tiempo real los semáforos de avance homologados por estudiante.")

        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1: st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed", key="v_search")
        with c_m2: st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed", key="v_prog")
        with c_m3: st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed", key="v_state")

        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            total_est = len(ests)
            barra_progreso = st.progress(0)
            
            html_matrix_rows = ""
            for idx, (idb, nom, alfas) in enumerate(ests):
                barra_progreso.progress(int(((idx + 1) / total_est) * 100))
                lista_alfas = alfas.split(",") if alfas else []
                
                # Función evaluadora conectada a las materias y estados de la DB
                def evaluar_estado_celda(cod_alfa):
                    if target_alfa := cod_alfa not in lista_alfas:
                        return '<span class="matrix-pill-noaplica">No aplica</span>'
                    
                    info = traer_datos("""
                        SELECT m.estado FROM asignaturas a 
                        LEFT JOIN maestro_pruebas m ON a.alfa = m.alfa_asignatura WHERE a.alfa = %s
                    """, (cod_alfa,))
                    
                    status = info[0][0] if info and info[0][0] else "Pendiente"
                    if status == "Construida":
                        return '<span class="matrix-pill-lista">Lista</span>'
                    elif status == "En construcción":
                        return '<span class="matrix-pill-proceso">En proceso</span>'
                    else:
                        return '<span class="matrix-pill-pendiente">Pendiente</span>'

                html_matrix_rows += f"""<tr>
<td>{idb}</td>
<td><b>{nom}</b></td>
<td>{evaluar_estado_celda("ISOF V003")}</td>
<td>{evaluar_estado_celda("ISOF V013")}</td>
<td>{evaluar_estado_celda("ISOF V043")}</td>
<td>{evaluar_estado_celda("ISOF V063")}</td>
<td>{evaluar_estado_celda("ISOF V081")}</td>
<td>{evaluar_estado_celda("ISOF V095")}</td>
<td><div style="color:#0047ff; text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""

            barra_progreso.empty()

            st.markdown(f"""<div class="premium-form-card" style="padding:20px; overflow-x:auto; margin-top:15px;">
<table class="master-matrix-table">
<thead><tr>
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
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Completo)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En proceso</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica</span>
</div></div>""", unsafe_allow_html=True)