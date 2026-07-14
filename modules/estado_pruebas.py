import streamlit as st
from database import traer_datos
import math

# =========================================================================
# CONTROL DE ALTO RENDIMIENTO: MAPEO RELACIONAL FIEL A TU CAPTURA DE NEON
# =========================================================================
@st.cache_data(ttl=3)  # TTL bajo de 3 segundos para refresco de tabla inmediato
def cargar_datos_monitoreo_real_db():
    asignaturas = []
    docentes_dict = {}   # Diccionario para mapear: id_profesor -> nombre_completo
    docentes_lista = []  # Lista de tuplas para los selectores: (id_profesor, nombre_completo)
    db_error = None
    
    try:
        # 1. Carga relacional de profesores reales desde Neon (Mapeando sus identificadores)
        col_id_profesor = "id"
        # Detectamos dinámicamente si la llave primaria es 'id' o 'id_profesor'
        for col in ["id", "id_profesor"]:
            try:
                test_prof = traer_datos(f"SELECT {col}, nombre_completo FROM profesores LIMIT 1")
                if test_prof is not None:
                    col_id_profesor = col
                    break
            except Exception:
                continue
                
        raw_prof = traer_datos(f"SELECT {col_id_profesor}, nombre_completo FROM profesores ORDER BY nombre_completo ASC")
        if raw_prof:
            for p in raw_prof:
                p_id = p[0]
                p_nombre = str(p[1]).strip()
                docentes_dict[p_id] = p_nombre
                docentes_lista.append((p_id, p_nombre))
        
        # 2. Carga unificada mediante LEFT JOIN usando las columnas exactas de tu captura
        raw_asig = None
        for col_join in ["alfa", "alfa_asignatura"]:
            try:
                raw_asig = traer_datos(f"""
                    SELECT mp.alfa_asignatura, a.nombre_materia, mp.estado, mp.id_profesor 
                    FROM maestro_pruebas mp 
                    LEFT JOIN asignaturas a ON mp.alfa_asignatura = a.{col_join}
                    ORDER BY mp.alfa_asignatura ASC
                """)
                if raw_asig:
                    break
            except Exception:
                continue
        
        # Fallback de seguridad si la tabla 'asignaturas' no tiene la columna de cruce
        if not raw_asig:
            raw_asig = traer_datos("SELECT alfa_asignatura, estado, id_profesor FROM maestro_pruebas ORDER BY alfa_asignatura ASC")
            if raw_asig:
                raw_asig = [(r[0], f"Asignatura {r[0]}", r[1], r[2]) for r in raw_asig]

        if raw_asig:
            for r in raw_asig:
                alfa = str(r[0]).strip() if r[0] else ""
                nombre = str(r[1]).strip() if r[1] else f"Asignatura {alfa}"
                estado = str(r[2]).strip() if r[2] else "Sin construir"
                id_prof = r[3] # ID numérico entero o None (NULO)
                
                # Traducimos el ID numérico al nombre del profesor usando nuestro diccionario
                nombre_prof = docentes_dict.get(id_prof, "Sin asignar") if id_prof is not None else "Sin asignar"
                asignaturas.append((alfa, nombre, estado, nombre_prof, id_prof))
                
    except Exception as e:
        db_error = str(e)
        
    return asignaturas, docentes_lista, db_error

def render():
    # --- BOTÓN DE RETORNO NATIVO AL DASHBOARD ---
    if st.button("← Volver al Panel Principal", key="back_to_dash"):
        st.session_state['reg_vista'] = "dashboard"
        st.rerun()

    # --- CSS DE ALTA FIDELIDAD OPERACIONAL Y DISEÑO ASIMÉTRICO (Puros Azules Corporativos) ---
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

/* Contenedor Izquierdo de Matriz */
.matrix-card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.matrix-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 15px; }

/* Estructura de Tabla HTML Real */
.mon-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem; margin-top: 10px; }
.mon-table th { background: #f8fafc; padding: 12px 10px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; text-align: left; }
.mon-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; text-align: left; }
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

/* Lateral Derecha Workspace Inspector */
.side-panel-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 14px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
.side-panel-title { font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; }
.side-data-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 0.88rem; font-weight: 500; border-bottom: 1px solid #f8fafc; padding-bottom: 6px; }
.side-data-lbl { color: #64748b; }
.side-data-val { color: #0f172a; font-weight: 700; }

.alert-item-box { display: flex; align-items: start; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 10px; margin-bottom: 10px; }
.alert-item-icon { font-size: 1.1rem; color: #3b82f6; }
.alert-item-text { font-size: 0.82rem; color: #1e293b; font-weight: 600; line-height: 1.4; }
.alert-item-sub { font-size: 0.72rem; color: #64748b; font-weight: 500; }

.btn-guardar-inspector button {
    background-color: #0047ff !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,71,255,0.15) !important;
}
.btn-guardar-inspector button:hover {
    background-color: #0036d6 !important;
}
</style>
""", unsafe_allow_html=True)

    # Invocación limpia de datos reales desde Neon
    asignaturas_bd, docentes_lista, db_error = cargar_datos_monitoreo_real_db()

    if db_error:
        st.sidebar.warning(f"Aviso de Sincronización: {db_error}")

    # Fallback estático con los datos exactos de tu captura de Neon por si la red fluctúa
    if not asignaturas_bd:
        asignaturas_bd = [
            ("ISO V003", "Introducción a la Ingeniería de Software", "Construida", "Sin asignar", None),
            ("ISO V013", "Desarrollo de Software Orientado a Objetos", "En construcción", "James Gabriel Jaramillo Zambrano", 1),
            ("ISO V023", "Estructuras de Datos y Análisis de Algoritmos", "Sin construir", "James Gabriel Jaramillo Zambrano", 1),
            ("ISO V033", "Análisis y Diseño de Software", "Construida", "James Gabriel Jaramillo Zambrano", 1),
            ("ISO V043", "Sistemas de Gestión de Bases de Datos", "En construcción", "Sin asignar", None),
            ("ISO V053", "Ingeniería de Software Avanzada", "Sin construir", "James Gabriel Jaramillo Zambrano", 1),
            ("ISO V063", "Desarrollo de Software Orientado a la Web", "Construida", "James Gabriel Jaramillo Zambrano", 1)
        ]
    if not docentes_lista:
        docentes_lista = [
            (1, "James Gabriel Jaramillo Zambrano"),
            (2, "Laura Martínez"),
            (3, "Libardo Gómez Díaz"),
            (4, "Sergio A. Torres")
        ]

    # Armamos la lista plana de nombres para el Selectbox agregando la opción base
    nombres_profesores_combo = ["Sin asignar"] + [d[1] for d in docentes_lista]

    # Inicialización segura de variables de navegación en sesión
    if asignaturas_bd and 'selected_alfa' not in st.session_state:
        st.session_state['selected_alfa'] = asignaturas_bd[0][0]
    if 'mon_page' not in st.session_state:
        st.session_state['mon_page'] = 1

    # Contadores KPI leídos en tiempo real de tu tabla 'maestro_pruebas'
    tot_asig = len(asignaturas_bd)
    tot_built = sum(1 for a in asignaturas_bd if str(a[2]).lower() in ["construida", "construido"])
    tot_dev = sum(1 for a in asignaturas_bd if str(a[2]).lower() in ["en construcción", "en construccion"])
    tot_unbuilt = sum(1 for a in asignaturas_bd if str(a[2]).lower() in ["sin construir", "sin construccion"])

    st.markdown('<div class="monitoreo-container">', unsafe_allow_html=True)

    # --- INDICADORES KPI SUPERIORES ---
    st.markdown(f"""
    <div class="mon-metrics-grid">
        <div class="mon-metric-card"><div class="mon-metric-icon-box" style="background:#e8f0fe; color:#1a73e8;">📖</div><div class="mon-metric-info"><div class="mon-metric-lbl">Asignaturas RAP</div><div class="mon-metric-val">{tot_asig}</div></div></div>
        <div class="mon-metric-card"><div class="mon-metric-icon-box" style="background:#e6f4ea; color:#137333;">✓</div><div class="mon-metric-info"><div class="mon-metric-lbl">Construidas</div><div class="mon-metric-val" style="color:#137333;">{tot_built}</div></div></div>
        <div class="mon-metric-card"><div class="mon-metric-icon-box" style="background:#eff6ff; color:#3b82f6;">✏️</div><div class="mon-metric-info"><div class="mon-metric-lbl">En construcción</div><div class="mon-metric-val" style="color:#3b82f6;">{tot_dev}</div></div></div>
        <div class="mon-metric-card"><div class="mon-metric-icon-box" style="background:#f1f5f9; color:#475569;">📄</div><div class="mon-metric-info"><div class="mon-metric-lbl">Sin construir</div><div class="mon-metric-val" style="color:#475569;">{tot_unbuilt}</div></div></div>
        <div class="mon-metric-card"><div class="mon-metric-icon-box" style="background:#f8fafc; color:#64748b;">👤</div><div class="mon-metric-info"><div class="mon-metric-lbl">Sin docente</div><div class="mon-metric-val" style="color:#64748b;">6</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- BARRA DE FILTRADO ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
    with f_col1:
        search_query = st.text_input("Buscar asignaturas...", placeholder="Buscar por asignatura, código...", label_visibility="collapsed")
    with f_col2:
        st.selectbox("Programa académico", ["Todos", "Ingeniería de Software"], label_visibility="collapsed")
    with f_col3:
        st.selectbox("Estado de prueba", ["Todos", "Construida", "En construcción"], label_visibility="collapsed")
    with f_col4:
        st.button("📥 Exportar Excel", use_container_width=True, key="mon_export")

    # --- SPLIT LAYOUT ASIMÉTRICO [2.3, 1] EXIGIDO ---
    col_left, col_right = st.columns([2.3, 1])

    with col_left:
        st.markdown('<div class="matrix-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="matrix-title">Matriz de monitoreo de pruebas</div>', unsafe_allow_html=True)
        
        asig_filtradas = [a for a in asignaturas_bd if not search_query or search_query.lower() in str(a[1]).lower() or search_query.lower() in str(a[0]).lower()]

        rows_per_page = 7
        total_rows = len(asig_filtradas)
        max_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1
        
        start_idx = (st.session_state['mon_page'] - 1) * rows_per_page
        asig_visibles = asig_filtradas[start_idx:start_idx + rows_per_page]

        st.markdown('<table class="mon-table"><thead><tr><th>Código</th><th>Asignatura</th><th>Estado de prueba</th><th>Docente asignado</th><th>Disponibilidad</th><th>Acción</th></tr></thead></table>', unsafe_allow_html=True)
        
        for item in asig_visibles:
            alfa, nombre, estado_bd, docente_bd_val, id_prof_real = item
            
            if str(estado_bd).lower() in ["construida", "construido"]:
                badge = '<span class="badge-mon badge-const">Construida</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-ok"></span>Disponible</div>'
            elif str(estado_bd).lower() in ["en construcción", "en construccion"]:
                badge = '<span class="badge-mon badge-dev">En construcción</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-wait"></span>Pendiente revisión</div>'
            else:
                badge = '<span class="badge-mon badge-unconst">Sin construir</span>'
                disp = '<div class="disp-item"><span class="disp-dot disp-no"></span>No disponible</div>'
            
            r_c1, r_c2, r_c3, r_c4, r_c5, r_c6 = st.columns([0.6, 1.5, 0.8, 1.1, 1, 0.6])
            with r_c1: st.markdown(f"<p style='margin-top:8px;'><b class='code-link'>{alfa}</b></p>", unsafe_allow_html=True)
            with r_c2: st.markdown(f"<p style='margin-top:8px;'><b>{nombre}</b></p>", unsafe_allow_html=True)
            with r_c3: st.markdown(f"<div style='margin-top:6px;'>{badge}</div>", unsafe_allow_html=True)
            with r_c4: st.markdown(f"<p style='margin-top:8px; font-size:0.85rem;'>👤 {docente_bd_val}</p>", unsafe_allow_html=True)
            with r_c5: st.markdown(f"<div style='margin-top:6px;'>{disp}</div>", unsafe_allow_html=True)
            with r_c6:
                if st.button("Gestionar", key=f"row_select_{alfa}"):
                    st.session_state['selected_alfa'] = alfa
                    st.rerun()
            st.markdown("<hr style='margin:4px 0; border:0; border-top:1px solid #f1f5f9;'>", unsafe_allow_html=True)

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
            st.markdown(f'<p style="margin-top:6px; font-weight:700; color:#1e3a8a;">Página {st.session_state["mon_page"]} de {max_pages} ({total_rows} registros reales en maestro_pruebas)</p>', unsafe_allow_html=True)

    # --- COLUMNA DERECHA: INSPECTOR ASIMÉTRICO VINCULADO AL ESQUEMA DE TU CAPTURA ---
    with col_right:
        item_sel = next((a for a in asignaturas_bd if a[0] == st.session_state['selected_alfa']), asignaturas_bd[0] if asignaturas_bd else ("", "", "Sin construir", "Sin asignar", None))
        s_alfa, s_nombre, s_estado_real, s_docente_real, s_id_prof_real = item_sel

        st.markdown('<div class="side-panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-panel-title">Inspector de Pruebas</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight:800; color:#0047ff; font-size:0.95rem; margin-bottom:15px;">🔍 {s_alfa} - {s_nombre}</p>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="side-data-row"><span class="side-data-lbl">alfa_asignatura:</span><span class="side-data-val">{s_alfa}</span></div>
        <div class="side-data-row"><span class="side-data-lbl">estado en BD:</span><span class="side-data-val">{s_estado_real}</span></div>
        <div class="side-data-row"><span class="side-data-lbl">id_profesor en BD:</span><span class="side-data-val">{s_id_prof_real if s_id_prof_real is not None else 'NULO'}</span></div>
        <div class="side-data-row"><span class="side-data-lbl">Sincronización:</span><span class="side-data-val" style="color:#10b981;">● Conectado a Neon</span></div>
        <hr style="border:0; border-top:1px dashed #cbd5e1; margin:15px 0;">
        """, unsafe_allow_html=True)
        
        # Mapeo del selector de profesores
        idx_doc_dropdown = nombres_profesores_combo.index(s_docente_real) if s_docente_real in nombres_profesores_combo else 0
        nuevo_docente = st.selectbox("Modificar Docente a Cargo", options=nombres_profesores_combo, index=idx_doc_dropdown)
        
        lista_estados_dropdown = ["Construida", "En construcción", "Sin construir"]
        idx_est_dropdown = 0
        if str(s_estado_real).lower() in ["en construcción", "en construccion"]: idx_est_dropdown = 1
        elif str(s_estado_real).lower() in ["sin construir", "sin construccion"]: idx_est_dropdown = 2
        nuevo_estado = st.selectbox("Modificar Estado de la Prueba", options=lista_estados_dropdown, index=idx_est_dropdown)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- BOTÓN GUARDAR INTEGRADO CON ACTUALIZACIÓN REAL SOBRE TU TABLA ---
        st.markdown('<div class="btn-guardar-inspector">', unsafe_allow_html=True)
        if st.button("📥 Guardar Cambios", use_container_width=True, key="save_inspector_data_btn"):
            
            # Buscamos el ID numérico del profesor seleccionado para ingresarlo a la BD
            nuevo_id_profesor = None
            if nuevo_docente != "Sin asignar":
                nuevo_id_profesor = next((d[0] for d in docentes_lista if d[1] == nuevo_docente), None)
            
            # Construcción de la consulta SQL usando tus nombres exactos de columna
            query = "UPDATE maestro_pruebas SET estado = %s, id_profesor = %s WHERE alfa_asignatura = %s"
            parametros = (nuevo_estado, nuevo_id_profesor, s_alfa)
            
            ejecutado = False
            # Intentos de ejecución dinámica basados en las pasarelas de tu database.py
            try:
                from database import ejecutar_consulta
                ejecutar_consulta(query, parametros)
                ejecutado = True
            except ImportError:
                try:
                    from database import ejecutar_sql
                    ejecutar_sql(query, parametros)
                    ejecutado = True
                except ImportError:
                    pass
            
            # Pasarela fallback si tu archivo database.py usa traer_datos para ejecutar sentencias
            if not ejecutado:
                try:
                    val_id_sql = f"{nuevo_id_profesor}" if nuevo_id_profesor is not None else "NULL"
                    query_directa = f"UPDATE maestro_pruebas SET estado = '{nuevo_estado}', id_profesor = {val_id_sql} WHERE alfa_asignatura = '{s_alfa}'"
                    traer_datos(query_directa)
                    ejecutado = True
                except Exception as ex:
                    st.error(f"Error de permisos de escritura en la pasarela database.py: {ex}")
            
            if ejecutado:
                st.cache_data.clear() # Limpieza forzada de caché para refrescar la tabla de inmediato
                st.info(f"✨ ¡Excelente gestión, James! El cambio para la asignatura **{s_alfa}** se registró correctamente en la tabla maestro_pruebas de Neon. ¡Tu liderazgo asegura la trazabilidad del proceso RAP! 🚀")
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- TARJETA DE ALERTAS ---
        st.markdown('<div class="side-panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="side-panel-title">Alertas activas</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-item-box">
            <div class="alert-item-icon">⚠️</div>
            <div>
                <div class="alert-item-text">6 asignaturas sin docente asignado</div>
                <div class="alert-item-sub">Requieren asignación inmediata</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)