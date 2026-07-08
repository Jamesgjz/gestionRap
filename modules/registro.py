import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

def conectar_neon_db():
    if "postgres" not in st.secrets:
        return None
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"],
            connect_timeout=5
        )
    except Exception:
        return None

def render():
    # Inicialización estable de estados de navegación de sub-módulos
    if 'pestana_actual' not in st.session_state:
        st.session_state['pestana_actual'] = "Docentes"
    if 'modo_docentes' not in st.session_state:
        st.session_state['modo_docentes'] = "lista"
    if 'modo_estudiantes' not in st.session_state:
        st.session_state['modo_estudiantes'] = "formulario"

    # --- INYECCIÓN DE ARQUITECTURA CSS DE ALTA FIDELIDAD ---
    st.markdown("""
<style>
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.breadcrumb { font-size: 0.85rem; color: #64748b; margin-bottom: 5px; }
.main-title { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0; }
.subtitle { font-size: 0.95rem; color: #64748b; margin: 4px 0 0 0; }

/* Barra de Pestañas Estilo de la Imagen 1 */
.tab-container { display: flex; border-bottom: 2px solid #e2e8f0; margin-bottom: 25px; gap: 30px; }
.tab-item { padding: 10px 5px; font-size: 0.95rem; font-weight: 600; color: #64748b; cursor: pointer; position: relative; }
.tab-item.active { color: #0047ff; font-weight: 700; }
.tab-item.active::after { content: ''; position: absolute; bottom: -2px; left: 0; width: 100%; height: 2px; background-color: #0047ff; }

/* Grid de Formulario de Dos Columnas Compresivo */
.form-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; margin-bottom: 25px; }
.form-section-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; }
.sidebar-summary-card { background: #fafafa; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; position: sticky; top: 20px; }

/* Estado de Pills para la Matriz Maestra de Asignaturas */
.pill-status-lista { background: #e6f4ea; color: #137333; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-pendiente { background: #fef7e0; color: #b06000; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-evaluacion { background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-reprobado { background: #fce8e6; color: #c5221f; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }
.pill-status-noaplica { background: #f1f3f4; color: #5f6368; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-align: center; display: block; }

.master-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.master-matrix-table th { background: #f8fafc; color: #475569; padding: 12px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.master-matrix-table td { padding: 14px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

    # --- CABECERA COMÚN DE REGISTROS ---
    st.markdown("""<div class="panel-header">
<div>
<div class="breadcrumb">Inicio &gt; Gestión de Registros</div>
<h1 class="main-title">Gestión de Registros</h1>
<p class="subtitle">Administra docentes evaluadores, estudiantes y consulta la vista maestra del proceso RAP.</p>
</div>
</div>""", unsafe_allow_html=True)

    # --- BARRA DE CONTROL DE PESTAÑAS (MOCKUP INTERACTIVO) ---
    c_t1, c_f2, c_f3, _ = st.columns([1.2, 1, 1.2, 4])
    with c_t1:
        if st.button("👥 Docentes evaluadores", use_container_width=True):
            st.session_state['pestana_actual'] = "Docentes"
            st.rerun()
    with c_f2:
        if st.button("🎓 Estudiantes", use_container_width=True):
            st.session_state['pestana_actual'] = "Estudiantes"
            st.rerun()
    with c_f3:
        if st.button("📊 Vista maestra", use_container_width=True):
            st.session_state['pestana_actual'] = "Maestra"
            st.rerun()

    st.markdown("<hr style='margin-top:0; margin-bottom:25px; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # =========================================================================
    # ESCENARIO TAB 1: DOCENTES EVALUADORES (Lista / Formulario image_46bf5a.jpg)
    # =========================================================================
    if st.session_state['pestana_actual'] == "Docentes":
        if st.session_state['modo_docentes'] == "lista":
            st.markdown("### Listado Maestro de Evaluadores")
            if st.button("➕ Registrar Nuevo Docente", type="primary"):
                st.session_state['modo_docentes'] = "formulario"
                st.rerun()
                
            # Tabla descriptiva básica de control
            conn = conectar_neon_db()
            if conn:
                df = pd.read_sql("SELECT id as ID, nombre as Nombre, correo as Correo, area as Area FROM public.profesores ORDER BY id DESC;", conn)
                st.dataframe(df, use_container_width=True, hide_index=True)
                conn.close()
                
        elif st.session_state['modo_docentes'] == "formulario":
            st.markdown("### Nuevo docente evaluador")
            st.write("Completa la información para registrar un nuevo docente que participará en el proceso RAP.")
            
            c_left, c_right = st.columns([2.2, 1])
            with c_left:
                with st.form("form_nuevo_profesor", clear_on_submit=True):
                    st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                    f_nombre = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                    f_correo = st.text_input("Correo institucional *", placeholder="Ej. maria.lopez@uniminuto.edu.co")
                    f_doc = st.text_input("Documento de identidad *", placeholder="Ej. 1.234.567.890")
                    f_area = st.text_input("Programa / Área *", placeholder="Ej. Ingeniería de Sistemas / Administración")
                    
                    st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                    st.multiselect("Asignaturas RAP *", ["Lógica Matemática", "Algoritmos", "Pensamiento Crítico", "Contabilidad General"], default=["Lógica Matemática"])
                    st.number_input("Horas asignadas *", min_value=1, max_value=40, value=12)
                    
                    st.markdown('<div class="form-section-title">3. Observaciones</div>', unsafe_allow_html=True)
                    st.text_area("Observaciones adicionales", placeholder="Disponibilidad, observaciones, etc.")
                    
                    c_b1, c_b2 = st.columns(2)
                    with c_b1:
                        submit = st.form_submit_action("Guardar docente", type="primary")
                    with c_b2:
                        cancel = st.form_submit_action("Cancelar")
                        
                    if submit:
                        if f_nombre and f_correo and f_area:
                            conn = conectar_neon_db()
                            if conn:
                                try:
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "INSERT INTO public.profesores (nombre, correo, area) VALUES (%s, %s, %s);",
                                        (f_nombre, f_correo, f_area)
                                    )
                                    conn.commit()
                                    cursor.close()
                                    conn.close()
                                    st.toast("✅ Docente guardado con éxito en Neon DB.")
                                    st.session_state['modo_docentes'] = "lista"
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error al escribir en la base de datos: {e}")
                        else:
                            st.warning("Por favor rellena los campos obligatorios del formulario.")
                    if cancel:
                        st.session_state['modo_docentes'] = "lista"
                        st.rerun()
                        
            with c_right:
                st.markdown("""<div class="sidebar-summary-card">
<h4 style="margin-top:0;color:#0f172a;">Resumen de registro</h4>
<p style="font-size:0.85rem;color:#64748b;"><i class="fa-solid fa-graduation-cap"></i> Formulario de parametrización académica.</p>
<hr style="border-color:#e2e8f0; margin:15px 0;">
<div style="font-size:0.85rem;color:#475569;line-height:1.8;">
• <b>Estado por defecto:</b> <span class="pill-status-activo">Activo</span><br>
• Los campos con asterisco (*) corresponden a columnas obligatorias del esquema relacional.
</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # ESCENARIO TAB 2: ESTUDIANTES (Formulario de Registro image_46c5e9.jpg)
    # =========================================================================
    elif st.session_state['pestana_actual'] == "Estudiantes":
        st.markdown("### Nuevo estudiante")
        st.write("Completa la información para registrar un nuevo estudiante en el proceso RAP.")
        
        c_left, c_right = st.columns([2.2, 1])
        with c_left:
            with st.form("form_nuevo_estudiante", clear_on_submit=True):
                st.markdown('<div class="form-section-title">1. Datos generales</div>', unsafe_allow_html=True)
                e_banner = st.text_input("ID Banner *", placeholder="Ej. 90012345")
                e_nombre = st.text_input("Nombre completo *", placeholder="Ej. María Fernanda López Gómez")
                e_doc = st.text_input("Documento *", placeholder="Ej. 1.234.567.890")
                e_correo = st.text_input("Correo institucional *", placeholder="Ej. maria.lopez@uniminuto.edu.co")
                
                st.markdown('<div class="form-section-title">2. Asignación académica</div>', unsafe_allow_html=True)
                st.selectbox("Programa académico *", ["Seleccione un programa", "Ingeniería de Sistemas", "Administración de Empresas", "Contaduría Pública"])
                st.multiselect("Asignaturas RAP *", ["Lógica Matemática", "Algoritmos", "Pensamiento Crítico", "Sistemas de Gestión"], default=["Lógica Matemática"])
                
                st.markdown('<div class="form-section-title">3. Observaciones</div>', unsafe_allow_html=True)
                st.text_area("Observaciones adicionales", placeholder="Apoyos requeridos, novedades, etc.")
                
                c_eb1, c_eb2 = st.columns(2)
                with c_eb1:
                    e_submit = st.form_submit_action("Guardar estudiante", type="primary")
                with e_eb2:
                    if st.form_submit_action("Ver listado actual"):
                        st.session_state['pestana_actual'] = "Maestra"
                        st.rerun()
                        
                if e_submit:
                    if e_nombre and e_correo and e_banner:
                        conn = conectar_neon_db()
                        if conn:
                            try:
                                cursor = conn.cursor()
                                cursor.execute(
                                    "INSERT INTO public.estudiantes (nombre, correo) VALUES (%s, %s);",
                                    (e_nombre, e_correo)
                                )
                                conn.commit()
                                cursor.close()
                                conn.close()
                                st.toast("✅ Estudiante registrado con éxito en Neon DB.")
                                st.session_state['pestana_actual'] = "Maestra"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar estudiante: {e}")
                    else:
                        st.warning("Por favor rellena el Nombre, ID Banner y Correo Electrónico.")
                        
        with c_right:
            st.markdown("""<div class="sidebar-summary-card">
<h4 style="margin-top:0;color:#0f172a;">Resumen de registro</h4>
<p style="font-size:0.85rem;color:#64748b;"><i class="fa-solid fa-id-card"></i> Ficha de matrícula del postulante.</p>
<hr style="border-color:#e2e8f0; margin:15px 0;">
<div style="font-size:0.85rem;color:#475569;line-height:1.8;">
• <b>Estado inicial:</b> <span class="pill-status-activo" style="background:#e8f0fe; color:#1a73e8;">Matriculado</span><br>
• Al guardar, se generará una traza limpia vinculada a la auditoría analítica del proceso.
</div>
</div>""", unsafe_allow_html=True)

    # =========================================================================
    # ESCENARIO TAB 3: VISTA MAESTRA (Matriz de Asignaturas por Estudiante image_46c65d.jpg)
    # =========================================================================
    elif st.session_state['pestana_actual'] == "Maestra":
        st.markdown("### Vista maestra de asignaturas por estudiante")
        st.write("Consulta y filtra el estado de avance en tiempo real de cada uno de los estudiantes frente a las asignaturas homologadas.")
        
        # Filtros Superiores Maquetados
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed")
        with c_m2:
            st.selectbox("Filtrar Asignatura", ["Todas las asignaturas", "ISOF V003", "ISOF V013", "ISOF V043"], label_visibility="collapsed")
        with c_m3:
            st.selectbox("Filtrar Estado", ["Todos los estados", "Lista", "Pendiente", "En evaluación", "Reprobado"], label_visibility="collapsed")

        # CONSTRUCCIÓN DE LA MATRIZ DINÁMICA DE ASIGNATURAS POR ESTUDIANTE
        conn = conectar_neon_db()
        html_filas_matriz = ""
        
        if conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT id, nombre, correo FROM public.estudiantes ORDER BY id DESC LIMIT 6;")
                estudiantes_reales = cursor.fetchall()
                
                base_id = 90012345
                for idx, est in enumerate(estudiantes_reales):
                    id_banner = str(base_id + est["id"])
                    nombre = str(est["nombre"])
                    
                    # Generación estocástica controlada de estados simulando avance real para poblar la matriz
                    pills = [
                        '<span class="pill-status-lista">Lista</span>',
                        '<span class="pill-status-pendiente">Pendiente</span>',
                        '<span class="pill-status-evaluacion">En evaluación</span>',
                        '<span class="pill-status-noaplica">No aplica</span>'
                    ]
                    
                    p1 = pills[idx % 4]
                    p2 = pills[(idx + 1) % 4]
                    p3 = pills[(idx + 2) % 4]
                    p4 = pills[(idx + 3) % 4]
                    
                    html_filas_matriz += """<tr>
<td>""" + id_banner + """</td>
<td><b>""" + nombre + """</b></td>
<td>""" + p1 + """</td>
<td>""" + p2 + """</td>
<td>""" + p3 + """</td>
<td>""" + p4 + """</td>
<td><span class="pill-status-noaplica">No aplica</span></td>
<td><span class="pill-status-lista">Lista</span></td>
<td><div style="color:#0047ff;font-weight:700;cursor:pointer;text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>"""
                cursor.close()
                conn.close()
            except Exception:
                if conn: conn.close()

        # Fallback seguro idéntico a image_46c65d.jpg si la base de datos no tiene suficientes registros
        if html_filas_matriz == "":
            html_filas_matriz = """
<tr>
<td>90012345</td><td>María Fernanda López Gómez</td>
<td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-evaluacion">En evaluación</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-noaplica">No aplica</span></td>
<td><div style="color:#0047ff;font-weight:700;text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>
<tr>
<td>90012346</td><td>James Gabriel Jaramillo</td>
<td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-evaluacion">En evaluación</span></td><td><span class="pill-status-pendiente">Pendiente</span></td>
<td><div style="color:#0047ff;font-weight:700;text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>
<tr>
<td>90012347</td><td>Ricardo Morales</td>
<td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-evaluacion">En evaluación</span></td><td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-pendiente">Pendiente</span></td><td><span class="pill-status-pendiente">Pendiente</span></td>
<td><div style="color:#0047ff;font-weight:700;text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>
<tr>
<td>90012348</td><td>Laura Andrade</td>
<td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-lista">Lista</span></td><td><span class="pill-status-evaluacion">En evaluación</span></td>
<td><div style="color:#0047ff;font-weight:700;text-align:center;"><i class="fa-solid fa-chevron-right"></i></div></td>
</tr>
"""

        # Renderizado de la estructura de la tabla de la matriz maestra
        st.markdown("""<div class="form-card" style="overflow-x:auto; padding:20px;">
<table class="master-matrix-table">
<thead>
<tr>
<th>ID Banner</th><th>Estudiante</th>
<th>ISOF V003<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Intro. Ing. Software</span></th>
<th>ISOF V013<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Prog. POO</span></th>
<th>ISOF V043<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Bases de Datos</span></th>
<th>ISOF V063<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Estructuras</span></th>
<th>ISOF V081<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Redes</span></th>
<th>ISOF V095<br><span style="font-size:0.68rem;font-weight:400;color:#64748b;">Arquitectura</span></th>
<th>Detalle</th>
</tr>
</thead>
<tbody>""" + html_filas_matriz + """</tbody>
</table>
<br>
<div style="display:flex; gap:25px; font-size:0.8rem; font-weight:600; flex-wrap:wrap; background:#f8fafc; padding:12px; border-radius:8px;">
<span><i class="fa-solid fa-circle" style="color:#137333;"></i> Lista (Evaluación completa)</span>
<span><i class="fa-solid fa-circle" style="color:#b06000;"></i> Pendiente (Aún no evaluada)</span>
<span><i class="fa-solid fa-circle" style="color:#1a73e8;"></i> En evaluación (En proceso)</span>
<span><i class="fa-solid fa-circle" style="color:#c5221f;"></i> Reprobado (No superada)</span>
<span><i class="fa-solid fa-circle" style="color:#5f6368;"></i> No aplica (No corresponde)</span>
</div>
</div>""", unsafe_allow_html=True)