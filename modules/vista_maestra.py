import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD Y CONTROL DE COLUMNAS ---
    st.markdown("""
<style>
.maestra-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

.mae-metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 30px; }
.mae-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-metric-icon-box { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; }
.mae-metric-info { display: flex; flex-direction: column; }
.mae-metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.mae-metric-val { font-size: 1.65rem; font-weight: 800; color: #0f172a; line-height: 1.2; }

.matrix-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow-x: auto; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }
.mae-table th { background: #f8fafc; padding: 14px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; text-align: center; }
.mae-table th.left-align { text-align: left; }
.mae-table th[title] { cursor: help; border-bottom: 2px dashed #cbd5e1; }

.mae-table td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; text-align: center; }
.mae-table td.left-align { text-align: left; }

.badge-mae { padding: 5px 10px; border-radius: 6px; font-weight: 700; font-size: 0.78rem; display: inline-block; min-width: 95px; text-align: center; text-transform: uppercase; }
.badge-lista { background-color: #e6f4ea; color: #137333; }
.badge-pendiente { background-color: #fef7e0; color: #b06000; }
.badge-evaluacion { background-color: #e8f0fe; color: #1a73e8; }
.badge-reprobado { background-color: #fce8e6; color: #c5221f; }
.badge-na { background-color: #f1f5f9; color: #64748b; border: 1px dashed #cbd5e1; }

.legend-container { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; padding: 10px; font-size: 0.85rem; font-weight: 600; color: #475569; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
.action-arrow { color: #3b82f6; font-weight: bold; font-size: 1.1rem; cursor: pointer; text-decoration: none; }

.info-banner-mae { background-color: #f0f4ff; border: 1px solid #d2e3fc; border-radius: 12px; padding: 16px; display: flex; align-items: center; margin-top: 25px; }
.info-banner-icon { font-size: 1.3rem; color: #0047ff; margin-right: 14px; }
.info-banner-text { font-size: 0.9rem; color: #1e3a8a; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN DE DATOS DE NEON ---
    materias_bd = []
    estudiantes_bd = []
    
    try:
        raw_asig = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY alfa ASC")
        if raw_asig:
            materias_bd = [(str(r[0]).strip(), str(r[1]).strip()) for r in raw_asig if r[0]]
            
        raw_est = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes ORDER BY nombre_completo ASC")
        if raw_est:
            estudiantes_bd = raw_est
    except Exception as e:
        st.sidebar.error(f"Nota de carga: {e}")

    # Fallback de datos
    if not materias_bd:
        materias_bd = [
            ("ISOF V003", "Introducción a la Ingeniería de Software"),
            ("ISOF V013", "Desarrollo de Software I"),
            ("ISOF V023", "Estructuras de Datos"),
            ("ISOF V033", "Análisis y Diseño"),
            ("ISOF V043", "Bases de Datos"),
            ("ISOF V063", "Programación Orientada a Objetos")
        ]

    if not estudiantes_bd:
        estudiantes_bd = [
            (90012345, "Alba Lucía Pinzón Gallego", "ISOF V003, ISOF V023"),
            (90012346, "James Gabriel Jaramillo", "ISOF V003, ISOF V013"),
            (90012347, "Ricardo Morales", "ISOF V043")
        ]

    st.markdown('<div class="maestra-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-title">Vista maestra de asignaturas</div><div class="section-subtitle">Matriz de seguimiento curricular optimizada.</div></div>', unsafe_allow_html=True)

    # --- FILTROS + IMPLEMENTACIÓN DEL MOCKUP COMPACTO ---
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1.5, 1, 1, 1, 1])
    with f_col1:
        search_query = st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID...", label_visibility="collapsed")
    with f_col2:
        st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        # AQUÍ LE DAMOS PROPÓSITO AL BOTÓN DEL MOCKUP: Switch de optimización horizontal
        vista_compacta = st.toggle("Vista compacta (Ocultar N/A)", value=True, help="Oculta automáticamente las columnas de materias que ningún estudiante filtrado tiene asignadas.")
    with f_col4:
        st.selectbox("Periodo", ["Todos los periodos"], label_visibility="collapsed")
    with f_col5:
        st.button("📥 Exportar", use_container_width=True)

    # Filtrado inicial de alumnos por texto de búsqueda
    estudiantes_filtrados = []
    for est in estudiantes_bd:
        id_b, name, alfas = est
        if search_query and (search_query.lower() not in name.lower() and search_query not in str(id_b)):
            continue
        estudiantes_filtrados.append(est)

    # =========================================================================
    # LÓGICA DE ALTA EFICIENCIA: Escaneo e Intercepción de Columnas Vivas
    # =========================================================================
    if vista_compacta:
        codigos_solicitados_en_pantalla = set()
        for est in estudiantes_filtrados:
            alfas_estudiante = [c.strip() for c in str(est[2]).split(",") if c.strip()]
            for cod in alfas_estudiante:
                codigos_solicitados_en_pantalla.add(cod)
        
        # Filtramos la lista de materias para conservar SOLO las que tengan solicitudes reales en pantalla
        materias_bd = [m for m in materias_bd if m[0] in codigos_solicitados_en_pantalla]

    # Redefinición de contadores basados en el set procesado
    tot_estudiantes = len(estudiantes_filtrados)
    tot_materias = len(materias_bd)

    # --- GRID DE CONTADORES ---
    st.markdown(f"""
    <div class="mae-metrics-grid">
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">👥</div><div class="mae-metric-info"><div class="mae-metric-lbl">Estudiantes</div><div class="mae-metric-val">{tot_estudiantes}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">📖</div><div class="mae-metric-info"><div class="mae-metric-lbl">Columnas Activas</div><div class="mae-metric-val">{tot_materias}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#fef7e0; color:#b06000;">🕒</div><div class="mae-metric-info"><div class="mae-metric-lbl">Pendientes</div><div class="mae-metric-val" style="color:#b06000;">12</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div><div class="mae-metric-info"><div class="mae-metric-lbl">Listas</div><div class="mae-metric-val" style="color:#137333;">45</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">📊</div><div class="mae-metric-info"><div class="mae-metric-lbl">En evaluación</div><div class="mae-metric-val" style="color:#3b82f6;">8</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- RENDERING DE ENCABEZADOS DINÁMICOS ---
    html_headers = '<th class="left-align">ID Banner</th><th class="left-align">Estudiante</th>'
    for alfa, nombre_completo_materia in materias_bd:
        html_headers += f'<th title="{nombre_completo_materia}">{alfa}</th>'
    html_headers += '<th>Detalle</th>'

    # --- RENDERING DE FILAS DINÁMICAS ---
    html_rows = ""
    for est in estudiantes_filtrados:
        id_banner, nombre_alumno, alfa_asignatura = est
        lista_codigos_alumno = [c.strip() for c in str(alfa_asignatura).split(",") if c.strip()]
        
        html_rows += "<tr>"
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
            
        html_rows += "<td><span class='action-arrow'>❯</span></td>"
        html_rows += "</tr>"

    # --- IMPRESIÓN DE LA TABLA INTELIGENTE ---
    st.markdown(f"""
    <div class="matrix-wrapper">
        <table class="mae-table">
            <thead><tr>{html_headers}</tr></thead>
            <tbody>{html_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- LEYENDA INFERIOR ---
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item"><div class="legend-dot" style="background:#10b981;"></div> Lista</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div> Pendiente</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div> En evaluación</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div> Reprobado</div>
        <div class="legend-item"><div class="legend-dot" style="background:#64748b;"></div> N/A (No corresponde)</div>
    </div>
    """, unsafe_allow_html=True)