import streamlit as st
from database import traer_datos
import math

def render():
    # --- BOTÓN DE RETORNO NATIVO ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD OPERACIONAL (Puros Azules Corporativos, Cero Rojo) ---
    st.markdown("""
<style>
.maestra-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* Grid de Contadores */
.mae-metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 30px; }
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
.badge-lista { background-color: #e6f4ea; color: #137333; border: 1px solid #c2e7c7; } 
.badge-construccion { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; } 
.badge-pendiente { background-color: #fef7e0; color: #b06000; border: 1px solid #fde293; } 
.badge-na { background-color: #f8fafc; color: #94a3b8; border: 1px dashed #e2e8f0; } 

.legend-container { display: flex; flex-wrap: wrap; gap: 24px; margin-top: 20px; padding: 10px; font-size: 0.85rem; font-weight: 700; color: #475569; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.legend-dot { width: 12px; height: 12px; border-radius: 4px; }
.action-arrow { color: #3b82f6; font-weight: bold; font-size: 1.1rem; cursor: pointer; text-decoration: none; }

/* Control de Paginación */
.pagination-info { font-size: 0.95rem; font-weight: 700; color: #1e3a8a; margin-top: 8px; }

/* Forzar Switch en Azul Claro Digital */
div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"],
button[role="switch"][aria-checked="true"],
div[data-baseweb="toggle"] div[aria-checked="true"],
.stToggle div[role="switch"][aria-checked="true"] {
    background-color: #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

    # --- Inicializar estado de página en sesión si no existe ---
    if 'pagina_actual' not in st.session_state:
        st.session_state['pagina_actual'] = 1

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
        st.error(f"Error de sincronización con Neon: {e}")

    # Fallback por si la conexión de red fluctúa
    if not materias_bd:
        materias_bd = [("ISOF V003", "Intro Software"), ("ISOF V013", "Desarrollo I"), ("ISOF V023", "Estructuras"), ("ISOF V033", "Análisis")]
    if not estudiantes_bd:
        estudiantes_bd = [(102621, "Estudiante de Prueba", "ISOF V003")]

    st.markdown('<div class="maestra-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-title">Vista maestra de asignaturas por estudiante</div><div class="section-subtitle">Tablero operacional completo con paginación integrada para control de pruebas RAP.</div></div>', unsafe_allow_html=True)

    # --- FILTROS SUPERIORES (MOCKUP) ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1.2, 1])
    with f_col1:
        search_query = st.text_input("Buscar estudiante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed")
        if search_query:
            # Si el usuario busca algo, lo regresamos a la página 1 para evitar desbofes
            st.session_state['pagina_actual'] = 1
    with f_col2:
        st.selectbox("Programa", ["Todos los programas", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        vista_compacta = st.toggle("Vista compacta (Ocultar columnas N/A)", value=True)
    with f_col4:
        limite_filas = st.selectbox("Registros por página", [10, 25, 50], index=0, label_visibility="collapsed")

    # 1. Aplicar filtro de búsqueda sobre la data real
    estudiantes_filtrados = []
    for est in estudiantes_bd:
        id_b, name, alfas = est
        if search_query and (search_query.lower() not in str(name).lower() and search_query not in str(id_b)):
            continue
        estudiantes_filtrados.append(est)

    # --- CÁLCULO DE PAGINACIÓN OPERATIVA ---
    total_registros = len(estudiantes_filtrados)
    total_paginas = math.ceil(total_registros / limite_filas) if total_registros > 0 else 1
    
    # Ajuste de seguridad por desborde
    if st.session_state['pagina_actual'] > total_paginas:
        st.session_state['pagina_actual'] = total_paginas

    indice_inicio = (st.session_state['pagina_actual'] - 1) * limite_filas
    indice_fin = indice_inicio + limite_filas
    
    # Segmentación exacta del set visible en esta página
    estudiantes_visibles = estudiantes_filtrados[indice_inicio:indice_fin]

    # 2. Compactación inteligente basada únicamente en lo que se ve en la página actual
    if vista_compacta and estudiantes_visibles:
        codigos_activos = set()
        for est in estudiantes_visibles:
            alfas_est = [c.strip().upper() for c in str(est[2]).split(",") if c.strip()]
            for cod in alfas_est:
                codigos_activos.add(cod)
        materias_bd = [m for m in materias_bd if m[0].upper() in codigos_activos]

    # Métricas calculadas en tiempo real
    tot_columnas = len(materias_bd)

    # --- GRID DE CONTADORES ---
    st.markdown(f"""
    <div class="mae-metrics-grid">
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">👥</div><div class="mae-metric-info"><div class="mae-metric-lbl">Total Registrados</div><div class="mae-metric-val">{total_registros}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">📊</div><div class="mae-metric-info"><div class="mae-metric-lbl">Columnas de Página</div><div class="mae-metric-val">{tot_columnas}</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#fef7e0; color:#b06000;">🕒</div><div class="mae-metric-info"><div class="mae-metric-lbl">Pendientes</div><div class="mae-metric-val" style="color:#b06000;">12</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div><div class="mae-metric-info"><div class="mae-metric-lbl">Pruebas Listas</div><div class="mae-metric-val" style="color:#137333;">Disponibles</div></div></div>
        <div class="mae-metric-card"><div class="mae-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">⏱️</div><div class="mae-metric-info"><div class="mae-metric-lbl">Página Actual</div><div class="mae-metric-val" style="color:#3b82f6;">{st.session_state['pagina_actual']}/{total_paginas}</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- ENCABEZADOS DE LA MATRIZ ---
    html_headers = '<th class="left-align">ID Banner</th><th class="left-align">Estudiante</th>'
    for alfa, nombre_completo_materia in materias_bd:
        html_headers += f'<th title="{nombre_completo_materia}">{alfa}</th>'
    html_headers += '<th>Acción</th>'

    # --- FILAS DINÁMICAS PAGINADAS ---
    html_rows = ""
    for est in estudiantes_visibles:
        id_banner, nombre_alumno, alfa_asignatura = est
        lista_codigos_alumno = [c.strip().upper() for c in str(alfa_asignatura).split(",") if c.strip()]
        
        html_rows += "<tr>"
        html_rows += f"<td class='left-align'>{id_banner}</td>"
        html_rows += f"<td class='left-align'><b>{nombre_alumno}</b></td>"
        
        for idx, (alfa_materia, _) in enumerate(materias_bd):
            if alfa_materia.upper() in lista_codigos_alumno:
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

    # --- CONTROL DE TABLA SEGURO ---
    if not html_rows:
        html_rows = "<tr><td colspan='20' style='text-align:center; padding:30px; color:#64748b;'>No se encontraron estudiantes para los criterios ingresados.</td></tr>"

    st.markdown(f"""
    <div class="matrix-wrapper">
        <table class="mae-table">
            <thead><tr>{html_headers}</tr></thead>
            <tbody>{html_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # BARRA DE CONTROL DE PAGINACIÓN INTERACTIVA (BAJO LA TABLA)
    # =========================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    p_col1, p_col2, p_col3, p_col4 = st.columns([1, 1, 4, 1])
    
    with p_col1:
        if st.button("◀ Anterior", use_container_width=True, disabled=(st.session_state['pagina_actual'] == 1), key="prev_page_btn"):
            st.session_state['pagina_actual'] -= 1
            st.rerun()
            
    with p_col2:
        if st.button("Siguiente ▶", use_container_width=True, disabled=(st.session_state['pagina_actual'] == total_paginas), key="next_page_btn"):
            st.session_state['pagina_actual'] += 1
            st.rerun()
            
    with p_col3:
        # Texto informativo de estatus posicional
        r_desde = indice_inicio + 1 if total_registros > 0 else 0
        r_hasta = min(indice_fin, total_registros)
        st.markdown(f'<div class="pagination-info">Mostrando registros del {r_desde} al {r_hasta} de un total de {total_registros} estudiantes</div>', unsafe_allow_html=True)

    # --- LEYENDA INFERIOR ---
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item"><div class="legend-dot" style="background:#10b981; border:1px solid #c2e7c7;"></div> <b>Lista:</b> Prueba lista. ¡Se puede aplicar!</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3b82f6; border:1px solid #d2e3fc;"></div> <b>En desarrollo:</b> Examen en construcción técnica.</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b; border:1px solid #fde293;"></div> <b>Pendiente:</b> Solicitud registrada en espera de reactivos.</div>
        <div class="legend-item"><div class="legend-dot" style="background:#94a3b8; border:1px solid #e2e8f0;"></div> <b>N/A:</b> El estudiante no seleccionó esta asignatura.</div>
    </div>
    """, unsafe_allow_html=True)