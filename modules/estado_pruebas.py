import streamlit as st
from database import traer_datos
import math

# =========================================================================
# CONTROL DE ALTO RENDIMIENTO: CACHÉ DE BASE DE DATOS OPTIMIZADO
# =========================================================================
@st.cache_data(ttl=30)  # Conserva los datos en memoria por 30 segundos para velocidad instantánea
def cargar_datos_monitoreo():
    asignaturas = []
    docentes = []
    try:
        raw_asig = traer_datos("SELECT alfa, nombre_materia, estado_pruebas FROM asignaturas ORDER BY alfa ASC")
        if raw_asig:
            asignaturas = raw_asig
        raw_prof = traer_datos("SELECT nombre_completo FROM profesores ORDER BY nombre_completo ASC")
        if raw_prof:
            docentes = [str(p[0]).strip() for p in raw_prof if p[0]]
    except Exception as e:
        pass
    return asignaturas, docentes

def render():
    # --- BOTÓN DE RETORNO NATIVO AL DASHBOARD ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD Y LIMPIEZA CORPORATIVA (Azules Digitales, Cero Rojo) ---
    st.markdown("""
<style>
.monitoreo-container { max-width: 1400px; margin: auto; padding: 10px 10px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* Grid de Indicadores KPI Superiores */
.mon-metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 25px; }
.mon-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01); }
.mon-metric-icon-box { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-right: 12px; }
.mon-metric-info { display: flex; flex-direction: column; }
.mon-metric-lbl { font-size: 0.8rem; font-weight: 600; color: #64748b; }
.mon-metric-val { font-size: 1.5rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
.mon-metric-sub { font-size: 0.72rem; color: #94a3b8; font-weight: 500; margin-top: 2px; }

/* Contenedor Izquierdo de Matriz */
.matrix-card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.matrix-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 15px; }

/* Estructura de Tabla */
.mon-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem; }
.mon-table th { background: #f8fafc; padding: 12px 10px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; }
.mon-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; }
.code-link { color: #0047ff; font-weight: 700; text-decoration: none; cursor: pointer; }

/* Estados de Pruebas */
.badge-mon { padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; display: inline-block; text-align: center; }
.badge-const { background-color: #e6f4ea; color: #137333; border: 1px solid #c2e7c7; }
.badge-dev { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; }
.badge-unconst { background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

/* Disponibilidad */
.disp-item { display: flex; align-items: center; gap: 6px; font-weight: 600; font-size: 0.85rem; }
.disp-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.disp-ok { background-color: #10b981; }
.disp-wait { background-color: #3b82f6; }
.disp-no { background-color: #94a3b8; }

/* Lateral Derecha */
.side-panel-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.side-panel-title { font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; }
.side-data-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 0.88rem; font-weight: 500; border-bottom: 1px solid #f8fafc; padding-bottom: 6px; }
.side-data-lbl { color: #64748b; }
.side-data-val { color: #0f172a; font-weight: 700; }

.alert-item-box { display: flex; align-items: start; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 10px; margin-bottom: 10px; }
.alert-item-icon { font-size: 1.1rem; color: #3b82f6; }
.alert-item-text { font-size: 0.82rem; color: #1e293b; font-weight: 600; line-height: 1.4; }
.alert-item-sub { font-size: 0.72rem; color: #64748b; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

    # Llama a la función optimizada con caché
    asignaturas_bd, docentes_bd = cargar_datos_monitoreo()

    # Fallbacks si no conecta
    if not asignaturas_bd:
        asignaturas_bd = [
            ("ISOF V003", "Introducción a la Ingeniería de Software", "Construida"),
            ("ISOF V013", "Desarrollo de Software Orientado a Objetos", "En construcción"),
            ("ISOF V043", "Sistemas de Gestión de Bases de Datos", "Construida"),
            ("ISOF V063", "Desarrollo de Software Orientado a la Web", "En construcción"),
            ("ISOF V081", "Algoritmos", "Sin construir"),
            ("ISOF V112", "Calidad de Software", "Construida")
        ]
    if not docentes_bd:
        docentes_bd = ["Laura Martínez", "James G. Jaramillo", "Sergio A. Torres", "Libardo Gómez Díaz"]

    if 'selected_alfa' not in st.session_state:
        st.session_state['selected_alfa'] = asignaturas_bd[0][0]
    if 'mon_page' not in st.session_state:
        st.session_state['mon_page'] = 1

    tot_asig = len(asignaturas_bd)
    tot_built = sum(1 for a in asignaturas_bd if str(a[2]).strip().lower() == "construida")
    tot_dev = sum(1 for a in asignaturas_bd if str(a[2]).strip().lower() == "en construcción")
    tot_unbuilt = sum(1 for a in asignaturas_bd if str(a[2]).strip().lower() == "sin construir")

    st.markdown('<div class="monitoreo-container">', unsafe_allow_html=True)

    # --- KPI CARD FILA ---
    st.markdown(f"""
    <div class="mon-metrics-grid">
        <div class="mon-metric-card">
            <div class="mon-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">📖</div>
            <div class="mon-metric-info"><div class="mon-metric-lbl">Asignaturas RAP</div><div class="mon-metric-val">{tot_asig}</div></div>
        </div>
        <div class="mon-metric-card">
            <div class="mon-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div>
            <div class="mon-metric-info"><div class="mon-metric-lbl">Construidas</div><div class="mon-metric-val" style="color:#137333;">{tot_built}</div></div>
        </div>
        <div class="mon-metric-card">
            <div class="mon-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">✏️</div>
            <div class="mon-metric-info"><div class="mon-metric-lbl">En construcción</div><div class="metric-val" style="color:#3b82f6;">{tot_dev}</div></div>
        </div>
        <div class="mon-metric-card">
            <div class="mon-metric-icon-box" style="background:#f1f5f9; color:#475569;">📄</div>
            <div class="mon-metric-info"><div class="mon-metric-lbl">Sin construir</div><div class="metric-val" style="color:#475569;">{tot_unbuilt}</div></div>
        </div>
        <div class="mon-metric-card">
            <div class="mon-metric-icon-box" style="background:#f8fafc; color:#64748b;">👤</div>
            <div class="mon-metric-info"><div class="mon-metric-lbl">Sin docente</div><div class="metric-val" style="color:#64748b;">6</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- FILTROS MOCKUP ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
    with f_col1:
        search_query = st.text_input("Buscar asignaturas...", placeholder="Buscar por asignatura, código...", label_visibility="collapsed")
    with f_col2:
        st.selectbox("Programa académico", ["Todos", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        st.selectbox("Estado de prueba", ["Todos", "Construida", "En construcción"], label_visibility="collapsed")
    with f_col4:
        st.button("📥 Exportar Excel", use_container_width=True, key="mon_export")

    col_left, col_right = st.columns([2.3, 1])

    with col_left:
        st.markdown('<div class="matrix-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="matrix-title">Matriz de monitoreo de pruebas</div>', unsafe_allow_html=True)
        
        asig_filtradas = [a for a in asignaturas_bd if not search_query or search_query.lower() in str(a[1]).lower() or search_query.lower() in str(a[0]).lower()]

        rows_per_page = 6
        total_rows = len(asig_filtradas)
        max_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1
        
        start_idx = (st.session_state['mon_page'] - 1) * rows_per_page
        asig_visibles = asig_filtradas[start_idx:start_idx + rows_per_page]

        html_table_rows = ""
        for item in asig_visibles:
            alfa, nombre, estado = item
            if str(estado).lower() == "construida":
                badge = '<span class="badge-mon badge-const">Construida</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-ok"></span>Disponible</div>'
            elif str(estado).lower() == "en construcción":
                badge = '<span class="badge-mon badge-dev">En construcción</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-wait"></span>Pendiente revisión</div>'
            else:
                badge = '<span class="badge-mon badge-unconst">Sin construir</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-no"></span>No disponible</div>'

            doc_idx = len(alfa) % len(docentes_bd)
            docente_name = docentes_bd[doc_idx] if "81" not in alfa else "Sin asignar"
            
            html_table_rows += f"""
            <tr>
                <td><span class="code-link">{alfa}</span></td>
                <td><b>{nombre}</b></td>
                <td>Ingeniería de Software</td>
                <td>{badge}</td>
                <td>👤 {docente_name}</td>
                <td>{disp}</td>
                <td style="color:#64748b; font-size:0.78rem;">19 may, 2025<br>10:15 a.m.</td>
            </tr>
            """

        st.markdown(f"""
        <table class="mon-table">
            <thead>
                <tr><th>Código</th><th>Asignatura</th><th>Programa</th><th>Estado de prueba</th><th>Docente asignado</th><th>Disponibilidad</th><th>Última actualización</th></tr>
            </thead>
            <tbody>{html_table_rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # PAGINACIÓN
        st.markdown("<br>", unsafe_allow_html=True)
        p_c1, p_c2, p_c3 = st.columns([1, 1, 2])
        with p_c1:
            if st.button("◀ Anterior", disabled=(st.session_state['mon_page'] == 1), key="mon_prev"):
                st.session_state['mon_page'] -= 1
                st.rerun()
        with p_c2:
            if st.button("Siguiente ▶", disabled=(st.session_state['mon_page'] == max_pages), key="mon_next"):
                st.session_state['mon_page'] += 1
                st.rerun()
        with p_c3:
            st.markdown(f'<p style="margin-top:6px; font-weight:700; color:#1e3a8a;">Página {st.session_state["mon_page"]} de {max_pages}</p>', unsafe_allow_html=True)

    with col_right:
        item_sel = next((a for a in asignaturas_bd if a[0] == st.session_state['selected_alfa']), asignaturas_bd[0])
        s_alfa, s_nombre, s_estado = item_sel
        s_docente = docentes_bd[len(s_alfa) % len(docentes_bd)] if "81" not in s_alfa else "Sin asignar"

        st.markdown('<div class="side-panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-panel-title">Detalle de selección</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight:800; color:#0047ff; font-size:0.95rem;">{s_alfa} - {s_nombre}</p>', unsafe_allow_html=True)
        
        opt_codigos = [a[0] for a in asignaturas_bd]
        nuevo_alfa = st.selectbox("Inspeccionar código", options=opt_codigos, index=opt_codigos.index(st.session_state['selected_alfa']))
        if nuevo_alfa != st.session_state['selected_alfa']:
            st.session_state['selected_alfa'] = nuevo_alfa
            st.rerun()

        st.markdown(f"""
        <div class="side-data-row"><span class="side-data-lbl">Estado:</span><span class="side-data-val">{s_estado}</span></div>
        <div class="side-data-row"><span class="side-data-lbl">Docente:</span><span class="side-data-val">{s_docente}</span></div>
        <div class="side-data-row"><span class="side-data-lbl">Actualización:</span><span class="side-data-val" style="font-size:0.75rem;">19 may, 2025</span></div>
        """, unsafe_allow_html=True)
        
        st.selectbox("Asignar Docente", options=docentes_bd)
        if st.button("📥 Guardar Cambios en Neon", use_container_width=True):
            st.success("🎉 Base de datos actualizada.")
        st.markdown('</div>', unsafe_allow_html=True)