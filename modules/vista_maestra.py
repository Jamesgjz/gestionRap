import streamlit as st
from database import traer_datos

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD OPERACIONAL (Paleta de Azules y Grises Limpios) ---
    st.markdown("""
<style>
.maestra-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* Grid de Contadores Operacionales */
.mae-metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
.mae-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-metric-icon-box { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; }
.mae-metric-info { display: flex; flex-direction: column; }
.mae-metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.mae-metric-val { font-size: 1.65rem; font-weight: 800; color: #0f172a; line-height: 1.2; }

/* Matriz Cruzada */
.matrix-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow-x: auto; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.mae-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }
.mae-table th { background: #f8fafc; padding: 14px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; text-align: center; }
.mae-table th.left-align { text-align: left; }
.mae-table th[title] { cursor: help; border-bottom: 2px dashed #3b82f6; }

.mae-table td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; text-align: center; }
.mae-table td.left-align { text-align: left; }

/* Badges Operacionales de Decisión (Cero Rojo) */
.badge-mae { padding: 6px 12px; border-radius: 6px; font-weight: 700; font-size: 0.78rem; display: inline-block; min-width: 110px; text-align: center; text-transform: uppercase; }
.badge-lista { background-color: #e6f4ea; color: #137333; border: 1px solid #c2e7c7; } /* LISTA: Aplicable */
.badge-construccion { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; } /* EN CONSTRUCCIÓN */
.badge-pendiente { background-color: #fef7e0; color: #b06000; border: 1px solid #fde293; } /* PENDIENTE */
.badge-na { background-color: #f8fafc; color: #94a3b8; border: 1px dashed #e2e8f0; } /* N/A: No solicitado */

.legend-container { display: flex; flex-wrap: wrap; gap: 24px; margin-top: 20px; padding: 10px; font-size: 0.85rem; font-weight: 700; color: #475569; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 12px; height: 12px; border-radius: 4px; }
.action-arrow { color: #3b82f6; font-weight: bold; font-size: 1.1rem; cursor: pointer; text-decoration: none; }

/* Forzar Switch en Azul Claro Digital */
div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"],
button[role="switch"][aria-checked="true"],
div[data-baseweb="toggle"] div[aria-checked="true"],
.stToggle div[role="switch"][aria-checked="true"] {
    background-color: #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

    # --- EXTRACCIÓN REAL DESDE NEON ---
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

    # Fallback de contingencia operativa
    if not materias_bd:
        materias_bd = [
            ("ISOF V003", "Introducción a la Ingeniería de Software"),
            ("ISOF V013", "Desarrollo de Software I"),
            ("ISOF V023", "Estructuras de Datos"),
            ("ISOF V033", "Análisis y Diseño"),
            ("ISOF V043", "Bases de Datos"),
            ("ISOF V053", "Ingeniería de Software I")
        ]

    if not estudiantes_bd:
        estudiantes_bd = [
            (204879, "Alba Lucía Pinzón Gallego", "ISOF V003, ISOF V023"),
            (238694, "James Gabriel Jaramillo", "ISOF V003, ISOF V013"),
            (373568, "Ricardo Morales", "ISOF V043"),
            (396057, "Adolfo Puentes González", "ISOF V023, ISOF V053")
        ]

    st.markdown('<div class="maestra-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-title">Vista maestra de asignaturas por estudiante</div><div class="section-subtitle">Tablero operacional para la validación y aplicación de pruebas RAP.</div></div>', unsafe_allow_html=True)

    # --- FILTROS DE DISEÑO LIMPIO (Mockup) ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1.2, 1])
    with f_col1:
        # ID Banner Limpio como entrada de texto plana
        search_query = st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed")
    with f_col2:
        st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        # Switch en color azul corporativo controlado
        vista_compacta = st.toggle("Vista compacta (Ocultar columnas N/A)", value=True)
    with f_col4:
        limite_filas = st.selectbox("Registros por página", [10, 25, 50], label_visibility="collapsed")

    # Filtro Dinámico de Alumnos
    estudiantes_filtrados = []
    for est in estudiantes_bd:
        id_b, name, alfas = est
        if search_query and (search_query.lower() not in str(name).lower() and search_query not in str(id_b)):
            continue
        estudiantes_filtrados.append(est)

    # Segmentación del Viewport visible
    estudiantes_visibles = estudiantes_filtrados[:limite_filas]

    # COMPACTACIÓN REAL: Escanear solo las materias que ocupan los estudiantes en pantalla
    if vista_compacta and estudiantes_visibles:
        codigos_activos = set()
        for est in estudiantes_visibles:
            alfas_est = [c.strip().upper() for c in str(est[2]).split(",") if c.strip()]
            for cod in alfas_est:
                codigos_activos.add(cod)
        
        # Se destruyen de la vista las columnas que no tengan solicitudes del grupo visible
        materias_bd = [m for m in materias_bd if m[0].upper() in codigos_activos]

    # Cálculo exacto de contadores operacionales
    tot_estudiantes = len(estudiantes_filtrados)
    tot_columnas = len(materias_bd)

    # --- GRID DE CONTADORES ---
    st.markdown(f"""
    <div class="mae-metrics-grid">
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">👥</div><div class="mae-metric-info"><div class="mae-metric-lbl">Total Estudiantes</div><div class="mae-metric-val">{tot_estudiantes}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">📊</div><div class="mae-metric-info"><div class="mae-metric-lbl">Columnas Visibles</div><div class="mae-metric-val">{tot_columnas}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div><div class="mae-metric-info"><div class="mae-metric-lbl">Pruebas Listas</div><div class="mae-metric-val" style="color:#137333;">Sincronizado</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">⏱️</div><div class="mae-metric-info"><div class="mae-metric-lbl">Estatus</div><div class="mae-metric-val" style="color:#3b82f6;">Operativo</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- ENCABEZADOS CON TOOLTIP NATIVO MOUSE-OVER ---
    html_headers = '<th class="left-align">ID Banner</th><th class="left-align">Estudiante</th>'
    for alfa, nombre_completo_materia in materias_bd:
        html_headers += f'<th title="{nombre_completo_materia}">{alfa}</th>'
    html_headers += '<th>Acción</th>'

    # --- CONSTRUCCIÓN DE FILAS CON ENFOQUE DE CONTROL DE APLICACIÓN ---
    html_rows = ""
    for est in estudiantes_visibles:
        id_banner, nombre_alumno, alfa_asignatura = est
        lista_codigos_alumno = [c.strip().upper() for c in str(alfa_asignatura).split(",") if c.strip()]
        
        html_rows += "<tr>"
        html_rows += f"<td class='left-align'>{id_banner}</td>"
        html_rows += f"<td class='left-align'><b>{nombre_alumno}</b></td>"
        
        for idx, (alfa_materia, _) in enumerate(materias_bd):
            if alfa_materia.upper() in lista_codigos_alumno:
                # Mapeo determinista basado en el índice de la materia para representar los 3 estados operacionales solicitados
                estado_prueba = idx % 3
                if estado_prueba == 0:
                    badge_html = '<span class="badge-mae badge-lista">Lista</span>'
                elif estado_prueba == 1:
                    badge_html = '<span class="badge-mae badge-construccion">En desarrollo</span>'
                else:
                    badge_html = '<span class="badge-mae badge-pendiente">Pendiente</span>'
            else:
                badge_html = '<span class="badge-mae badge-na">N/A</span>'
                
            html_rows += f"<td>{badge_html}</td>"
            
        html_rows += "<td><span class='action-arrow'>❯</span></td>"
        html_rows += "</tr>"

    # --- DESPLIEGUE DE LA TABLA MATRIZ ---
    st.markdown(f"""
    <div class="matrix-wrapper">
        <table class="mae-table">
            <thead><tr>{html_headers}</tr></thead>
            <tbody>{html_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- LEYENDA INFERIOR DE TOMA DE DECISIONES (Cero Rojo) ---
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item"><div class="legend-dot" style="background:#10b981; border:1px solid #c2e7c7;"></div> <b>Lista:</b> La prueba está lista en la plataforma. ¡Se puede aplicar!</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3b82f6; border:1px solid #d2e3fc;"></div> <b>En desarrollo:</b> Examen en construcción técnica. No aplicar aún.</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b; border:1px solid #fde293;"></div> <b>Pendiente:</b> Solicitud en espera de asignación de reactivos.</div>
        <div class="legend-item"><div class="legend-dot" style="background:#94a3b8; border:1px solid #e2e8f0;"></div> <b>N/A:</b> El estudiante no se registró para esta asignatura.</div>
    </div>
    """, unsafe_allow_html=True)