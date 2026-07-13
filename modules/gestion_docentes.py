import streamlit as st
from database import traer_datos

def render():
    # --- FUNCIONES DE NAVEGACIÓN SEGURA (CALLBACKS DE ALTA RESPUESTA) ---
    def ir_al_panel():
        st.session_state['reg_vista'] = "dashboard"

    def ir_a_nuevo_docente():
        st.session_state['reg_vista'] = "nuevo_docente"

    # --- BOTÓN DE RETORNO NATIVO ---
    st.button("← Volver al Panel Principal", key="back_to_dash", on_click=ir_al_panel)

    # --- CSS DE ALTA FIDELIDAD CON AZUL CLARO CORPORATIVO ---
    st.markdown("""
<style>
.docentes-container { max-width: 1400px; margin: auto; padding: 10px 20px; font-family: 'Inter', sans-serif; }
.section-header { margin-bottom: 25px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.section-subtitle { font-size: 0.95rem; color: #64748b; }

/* INYECCIÓN EXACTA: Target directo al 4to elemento del bloque de filtros (Botón Nuevo Docente) */
[data-testid="stHorizontalBlock"] > div:nth-child(4) button {
    background-color: #3b82f6 !important; /* Azul claro / azul digital de registro */
    color: white !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 4px 6px rgba(59,130,246,0.15) !important;
    transition: background-color 0.2s ease;
}
[data-testid="stHorizontalBlock"] > div:nth-child(4) button:hover {
    background-color: #2563eb !important;
    border-color: #2563eb !important;
}

/* Fila de Métricas */
.doc-metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; margin-top: 25px; }
.doc-metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.doc-metric-icon-box { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-right: 16px; }
.doc-metric-info { display: flex; flex-direction: column; }
.doc-metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.doc-metric-val { font-size: 1.75rem; font-weight: 800; color: #0f172a; line-height: 1.2; }

/* Tabla */
.table-wrapper { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.doc-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
.doc-table th { background: #f8fafc; padding: 16px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; }
.doc-table td { padding: 16px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; }

.doc-profile-cell { display: flex; align-items: center; }
.doc-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 12px; flex-shrink: 0; }
.doc-info-text { display: flex; flex-direction: column; }
.doc-name { font-weight: 700; color: #0f172a; }
.doc-email { font-size: 0.8rem; color: #64748b; }

.badge-doc { padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; display: inline-block; text-align: center; }
.badge-activo { background-color: #e6f4ea; color: #137333; }

.info-banner { background-color: #f0f4ff; border: 1px solid #d2e3fc; border-radius: 12px; padding: 20px; display: flex; align-items: start; margin-top: 30px; }
.info-banner-icon { font-size: 1.4rem; color: #0047ff; margin-right: 15px; margin-top: -2px; }
.info-banner-text { font-size: 0.95rem; color: #1e3a8a; line-height: 1.5; font-weight: 500; }
.action-icons { color: #0047ff; font-weight: 600; letter-spacing: 5px; cursor: pointer; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

    # --- PROCESAMIENTO SEGURO DE DATOS ---
    docentes_filtrados = []
    try:
        raw_data = traer_datos("SELECT * FROM profesores")
        if raw_data:
            for row in raw_data:
                nombre = row[1] if len(row) > 1 else "Docente Evaluador"
                programa = row[3] if len(row) > 3 else "Educación Virtual"
                asignaturas = "Construcción de pruebas"
                estado = row[6] if len(row) > 6 else "Activo"
                fecha = row[7] if len(row) > 7 else "Hoy"
                
                email = ""
                horas = 16
                for idx, campo in enumerate(row):
                    if campo is None: continue
                    campo_str = str(campo).strip()
                    if "@" in campo_str:
                        email = campo_str
                    elif idx != 0 and (isinstance(campo, (int, float)) or campo_str.isdigit()):
                        horas = int(campo)
                
                if not email:
                    partes_name = nombre.lower().split()
                    p_nombre = partes_name[0] if partes_name else "docente"
                    p_apellido = partes_name[1] if len(partes_name) > 1 else "evaluador"
                    email = f"{p_nombre}.{p_apellido}@uniminuto.edu.co"
                
                docentes_filtrados.append((nombre, email, programa, asignaturas, horas, estado, fecha))
    except Exception as e:
        st.sidebar.error(f"Nota de sincronización: {e}")

    if not docentes_filtrados:
        docentes_filtrados = [
            ("James Gabriel Jaramillo Zambrano", "james.jaramillo@uniminuto.edu.co", "Ingeniería de Sistemas", "Construcción de pruebas", 4, "Activo", "Hoy"),
            ("Libardo Gómez Díaz", "libardo.gomez@uniminuto.edu.co", "Educación Virtual", "Construcción de pruebas", 2, "Activo", "Hoy"),
            ("Sergio Andrés Torres Martínez", "sergio.torres@uniminuto.edu.co", "Educación Virtual", "Construcción de pruebas", 2, "Activo", "Hoy")
        ]

    tot_doc = len(docentes_filtrados)
    tot_act = sum(1 for d in docentes_filtrados if "activo" in str(d[5]).lower())
    tot_asig = len(docentes_filtrados)
    tot_pend = 0

    st.markdown('<div class="docentes-container">', unsafe_allow_html=True)

    # --- ENCABEZADO ---
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Gestión de docentes evaluadores</div>
        <div class="section-subtitle">Registra, actualiza y administra los docentes que participan en el proceso RAP.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- FILTROS Y BOTÓN MODIFICADOS (USO DE CALLBACK SEGURO) ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
    with f_col1:
        search_query = st.text_input("Buscar por nombre...", key="doc_search_input", label_visibility="collapsed", placeholder="Buscar por nombre del docente...")
    with f_col2:
        st.selectbox("Programa", ["Todos los programas"], label_visibility="collapsed")
    with f_col3:
        st.selectbox("Estado", ["Todos los estados"], label_visibility="collapsed")
    with f_col4:
        # El callback 'on_click' soluciona de raíz el problema de congelamiento
        st.button("+ Nuevo docente", use_container_width=True, key="new_doc_nav_btn", on_click=ir_a_nuevo_docente)

    # --- GRID DE MÉTRICAS ---
    st.markdown(f"""
    <div class="doc-metrics-grid">
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #e8f0fe; color: #1a73e8;">👥</div>
            <div class="doc-metric-info"><div class="doc-metric-lbl">Total docentes</div><div class="metric-val">{tot_doc}</div></div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #e6f4ea; color: #137333;">✓</div>
            <div class="doc-metric-info"><div class="doc-metric-lbl">Activos</div><div class="metric-val" style="color:#137333;">{tot_act}</div></div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #f3e8ff; color: #6b21a8;">📖</div>
            <div class="doc-metric-info"><div class="doc-metric-lbl">Con asignación</div><div class="metric-val" style="color:#6b21a8;">{tot_asig}</div></div>
        </div>
        <div class="doc-metric-card">
            <div class="doc-metric-icon-box" style="background: #fef7e0; color: #b06000;">🕒</div>
            <div class="doc-metric-info"><div class="doc-metric-lbl">Pendientes</div><div class="metric-val" style="color:#b06000;">{tot_pend}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TABLA ---
    html_table_rows = ""
    for doc in docentes_filtrados:
        nombre, email, programa, asignaturas, horas, estado, ultima_act = doc
        if search_query and search_query.lower() not in nombre.lower():
            continue
            
        partes = nombre.split()
        iniciales = "".join([p[0] for p in partes[:2]]).upper() if len(partes) >= 2 else nombre[:2].upper()
        
        avatar_bg = "#e8f0fe"
        avatar_txt = "#1a73e8"

        html_table_rows += f"<tr><td><div class='doc-profile-cell'><div class='doc-avatar' style='background:{avatar_bg}; color:{avatar_txt};'>{iniciales}</div><div class='doc-info-text'><span class='doc-name'>{nombre}</span><span class='doc-email'>{email}</span></div></div></td><td>{programa}</td><td><b style='color:#6b21a8;'>{asignaturas}</b></td><td><b>{horas}</b> hrs</td><td><span class='badge-doc badge-activo'>{estado}</span></td><td>{ultima_act}</td><td class='action-icons'>👁️📝⋮</td></tr>"

    st.markdown(f"""
    <h3 style="font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 20px; margin-bottom: 10px;">Listado de docentes</h3>
    <div class="table-wrapper">
        <table class="doc-table">
            <thead>
                <tr>
                    <th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th>
                </tr>
            </thead>
            <tbody>{html_table_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <div class="info-banner-icon">ℹ️</div>
        <div class="info-banner-text">
            Este módulo permite la parametrización y soporte académico del proceso RAP. Asegúrate de mantener actualizada la información de los docentes y sus asignaciones para garantizar la correcta operación del proceso.
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)