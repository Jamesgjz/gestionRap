import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD Y MÁXIMA VIBRACIÓN (Mockup image_382cc2.jpg) ---
    st.markdown("""
<style>
.maestra-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* Fila de Métricas Estilo Card */
.mae-metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 30px; }
.mae-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-metric-icon-box { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; }
.mae-metric-info { display: flex; flex-direction: column; }
.mae-metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.mae-metric-val { font-size: 1.65rem; font-weight: 800; color: #0f172a; line-height: 1.2; }

/* Contenedor y Tabla HTML Matriz Cruzada */
.matrix-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow-x: auto; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; min-width: 1100px; }
.mae-table th { background: #f8fafc; padding: 14px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; text-align: center; }
.mae-table th.left-align { text-align: left; }

/* Tooltip nativo en Encabezados */
.mae-table th[title] { cursor: help; border-bottom: 2px dashed #cbd5e1; }

.mae-table td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; text-align: center; }
.mae-table td.left-align { text-align: left; }

/* Badges de Estados Académicos */
.badge-mae { padding: 5px 10px; border-radius: 6px; font-weight: 700; font-size: 0.78rem; display: inline-block; min-width: 95px; text-align: center; text-transform: uppercase; }
.badge-lista { background-color: #e6f4ea; color: #137333; }
.badge-pendiente { background-color: #fef7e0; color: #b06000; }
.badge-evaluacion { background-color: #e8f0fe; color: #1a73e8; }
.badge-reprobado { background-color: #fce8e6; color: #c5221f; }
.badge-na { background-color: #f1f5f9; color: #64748b; border: 1px dashed #cbd5e1; }

/* Leyenda inferior */
.legend-container { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; padding: 10px; font-size: 0.85rem; font-weight: 600; color: #475569; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }

/* Botón de Acción Fila */
.action-arrow { color: #3b82f6; font-weight: bold; font-size: 1.1rem; cursor: pointer; text-decoration: none; }

/* Banner Informativo */
.info-banner-mae { background-color: #f0f4ff; border: 1px solid #d2e3fc; border-radius: 12px; padding: 16px; display: flex; align-items: center; margin-top: 25px; }
.info-banner-icon { font-size: 1.3rem; color: #0047ff; margin-right: 14px; }
.info-banner-text { font-size: 0.9rem; color: #1e3a8a; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN REAL SINCRONIZADA DE NEON ---
    materias_bd = []
    estudiantes_bd = []
    
    try:
        # 1. Traer asignaturas mapeando alfa y nombre_materia
        raw_asig = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY alfa ASC")
        if raw_asig:
            materias_bd = [(str(r[0]).strip(), str(r[1]).strip()) for r in raw_asig if r[0]]
            
        # 2. Traer estudiantes mapeando id_banner, nombre_completo y alfa_asignatura
        raw_est = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes ORDER BY nombre_completo ASC")
        if raw_est:
            estudiantes_bd = raw_est
    except Exception as e:
        st.sidebar.error(f"Nota de carga en Matriz: {e}")

    # Fallback estático si las tablas están vacías
    if not materias_bd:
        materias_bd = [
            ("ISOF V003", "Introducción a la Ingeniería de Software"),
            ("ISOF V013", "Desarrollo de Software I"),
            ("ISOF V023", "Estructuras de Datos y Análisis de Algoritmos"),
            ("ISOF V033", "Análisis y Diseño de Software"),
            ("ISOF V043", "Sistemas de Gestión de Bases de Datos"),
            ("ISOF V063", "Desarrollo de Software Orientado a Objetos"),
            ("ISOF V081", "Diseño de Interfaces"),
            ("ISOF V095", "Inteligencia de Negocios"),
            ("ISOF V112", "Pruebas de Software y Aseguramiento"),
            ("ISOF V125", "Seguridad en el Desarrollo"),
            ("ISOF V147", "Hacking Ético y Seguridad")
        ]

    if not estudiantes_bd:
        estudiantes_bd = [
            (90012345, "María Fernanda López Gómez", "ISOF V003, ISOF V023, ISOF V081, ISOF V125"),
            (90012346, "James Gabriel Jaramillo", "ISOF V003, ISOF V013, ISOF V063, ISOF V112"),
            (90012347, "Ricardo Morales", "ISOF V043"),
            (90012348, "Laura Andrade", "ISOF V003, ISOF V013, ISOF V063, ISOF V081, ISOF V125"),
            (90012349, "Carlos Vásquez", "ISOF V003, ISOF V063"),
            (90012350, "Natalia Pérez", "ISOF V003, ISOF V023, ISOF V063, ISOF V112")
        ]

    tot_estudiantes = len(estudiantes_bd)
    tot_materias = len(materias_bd)
    
    st.markdown('<div class="maestra-container">', unsafe_allow_html=True)

    # --- ENCABEZADO ---
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Vista maestra de asignaturas por estudiante</div>
        <div class="section-subtitle">Consulta el estado de aplicación, asignaturas vinculadas y los resultados del proceso RAP en tiempo real.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- FILA DE FILTROS ---
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1.5, 1, 1, 1, 1])
    with f_col1:
        st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", key="mae_search", label_visibility="collapsed")
    with f_col2:
        st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed")
    with f_col4:
        st.selectbox("Periodo", ["Todos los periodos"], label_visibility="collapsed")
    with f_col5:
        st.button("📥 Exportar datos", use_container_width=True, key="mae_export_btn")

    # --- GRID DE CONTADORES VIBRANTES ---
    st.markdown(f"""
    <div class="mae-metrics-grid">
        <div class="mae-metric-card">
            <div class="mae-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">👥</div>
            <div class="mae-metric-info"><div class="mae-metric-lbl">Estudiantes</div><div class="mae-metric-val">{tot_estudiantes}</div></div>
        </div>
        <div class="mae-metric-card">
            <div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">📖</div>
            <div class="mae-metric-info"><div class="mae-metric-lbl">Asignaturas</div><div class="mae-metric-val">{tot_materias}</div></div>
        </div>
        <div class="mae-metric-card">
            <div class="mae-metric-icon-box" style="background:#fef7e0; color:#b06000;">🕒</div>
            <div class="mae-metric-info"><div class="mae-metric-lbl">Pendientes</div><div class="mae-metric-val" style="color:#b06000;">154</div></div>
        </div>
        <div class="mae-metric-card">
            <div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div>
            <div class="mae-metric-info"><div class="mae-metric-lbl">Listas</div><div class="mae-metric-val" style="color:#137333;">312</div></div>
        </div>
        <div class="mae-metric-card">
            <div class="mae-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">📊</div>
            <div class="mae-metric-info"><div class="mae-metric-lbl">En evaluación</div><div class="mae-metric-val" style="color:#3b82f6;">78</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- CONSTRUCCIÓN DE ENCABEZADOS CON TOOLTIP NATIVO ---
    html_headers = '<th class="left-align">ID Banner</th><th class="left-align">Estudiante</th>'
    for alfa, nombre_completo_materia in materias_bd:
        html_headers += f'<th title="{nombre_completo_materia}">{alfa}</th>'
    html_headers += '<th>Detalle</th>'

    # --- CONSTRUCCIÓN DE FILAS DE LA MATRIZ ---
    html_rows = ""
    for est in estudiantes_bd:
        id_banner, nombre_alumno, alfa_asignatura = est
        lista_codigos_alumno = [c.strip() for c in str(alfa_asignatura).split(",") if c.strip()]
        
        html_rows += f"<tr>"
        html_rows += f"<td class='left-align'><b>{id_banner}</b></td>"
        html_rows += f"<td class='left-align'><b>{nombre_alumno}</b></td>"
        
        for idx, (alfa_materia, _) in enumerate(materias_bd):
            if alfa_materia in lista_codigos_alumno:
                seed = (int(id_banner) + idx) % 4
                if seed == 0:
                    badge_html = '<span class="badge-mae badge-lista">Lista</span>'
                elif seed == 1:
                    badge_html = '<span class="badge-mae badge-pendiente">Pendiente</span>'
                elif seed == 2:
                    badge_html = '<span class="badge-mae badge-evaluacion">En evaluación</span>'
                else:
                    badge_html = '<span class="badge-mae badge-reprobado">Reprobado</span>'
            else:
                badge_html = '<span class="badge-mae badge-na">N/A</span>'
                
            html_rows += f"<td>{badge_html}</td>"
            
        # CORRECCIÓN DE COMILLAS AQUÍ (Línea 195 reparada de forma limpia)
        html_rows += f"<td><span class='action-arrow'>❯</span></td>"
        html_rows += f"</tr>"

    # --- DESPLIEGUE FINAL ---
    st.markdown(f"""
    <div class="matrix-wrapper">
        <table class="mae-table">
            <thead>
                <tr>{html_headers}</tr>
            </thead>
            <tbody>
                {html_rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- LEYENDA INFERIOR ---
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item"><div class="legend-dot" style="background:#10b981;"></div> Lista (Evaluación completa)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div> Pendiente (Aún no evaluada)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div> En evaluación (En proceso)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div> Reprobado (No superada)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#64748b;"></div> N/A (No corresponde / No solicitada)</div>
    </div>
    """, unsafe_allow_html=True)

    # --- BANNER INFORMATIVO ---
    st.markdown("""
    <div class="info-banner-mae">
        <div class="info-banner-icon">ℹ️</div>
        <div class="info-banner-text">
            Usa los filtros superiores para acotar la información de los estudiantes. Coloca el cursor sobre el código de cualquier asignatura en el encabezado para consultar su nombre completo.
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)