import streamlit as st
from database import traer_datos

def render():
    # --- CSS ESPECÍFICO PARA GESTIÓN DOCENTES ---
    st.markdown("""
<style>
.docentes-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Inter', sans-serif; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.metric-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; }
.metric-val { font-size: 1.8rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
.metric-lbl { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.doc-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9rem; }
.doc-table th { background: #f8fafc; padding: 16px 12px; text-align: left; color: #475569; border-bottom: 2px solid #e2e8f0; }
.doc-table td { padding: 16px 12px; border-bottom: 1px solid #f1f5f9; color: #334155; }
.badge { padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
.btn-primary-doc { background: #0047ff !important; color: white !important; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

    # --- LÓGICA DE DATOS ---
    try:
        # Ajusta estos nombres de tabla/columna a tu DB real
        tot_doc = traer_datos("SELECT COUNT(*) FROM profesores")[0][0]
        tot_act = traer_datos("SELECT COUNT(*) FROM profesores WHERE estado = 'Activo'")[0][0]
        tot_asig = traer_datos("SELECT COUNT(*) FROM profesores WHERE asignacion IS NOT NULL")[0][0]
        tot_pend = traer_datos("SELECT COUNT(*) FROM profesores WHERE estado = 'Pendiente'")[0][0]
        
        docentes_data = traer_datos("SELECT nombre_completo, email, programa, asignaturas, horas_asignadas, estado, ultima_actualizacion FROM profesores")
    except:
        tot_doc = tot_act = tot_asig = tot_pend = 0
        docentes_data = []

    st.markdown('<div class="docentes-container">', unsafe_allow_html=True)
    
    # Cabecera
    st.markdown("""<div class="top-bar">
        <h2>Gestión de docentes evaluadores</h2>
        <button class="btn-primary-doc">+ Nuevo docente</button>
    </div>""", unsafe_allow_html=True)

    # Métricas
    st.markdown(f"""<div class="metrics-row">
        <div class="metric-box"><div class="metric-lbl">Total docentes</div><div class="metric-val">{tot_doc}</div></div>
        <div class="metric-box"><div class="metric-lbl">Activos</div><div class="metric-val" style="color:#00875a;">{tot_act}</div></div>
        <div class="metric-box"><div class="metric-lbl">Con asignación</div><div class="metric-val" style="color:#6b21a8;">{tot_asig}</div></div>
        <div class="metric-box"><div class="metric-lbl">Pendientes</div><div class="metric-val" style="color:#b06000;">{tot_pend}</div></div>
    </div>""", unsafe_allow_html=True)

    # Filtros
    c1, c2, c3, c4 = st.columns([2,1,1,1])
    c1.text_input("Buscar por nombre del docente...", key="search")
    c2.selectbox("Programa", ["Todos los programas"])
    c3.selectbox("Estado", ["Todos los estados"])
    
    # Tabla
    html_rows = ""
    for doc in docentes_data:
        nombre, email, prog, asig, horas, estado, fecha = doc
        color_estado = "#e6f4ea" if estado == "Activo" else "#fef7e0"
        text_estado = "#137333" if estado == "Activo" else "#b06000"
        
        html_rows += f"""<tr>
            <td><b>{nombre}</b><br><small style="color:#64748b;">{email}</small></td>
            <td>{prog}</td>
            <td>{asig}</td>
            <td>{horas} horas</td>
            <td><span class="badge" style="background:{color_estado}; color:{text_estado};">{estado}</span></td>
            <td>{fecha}</td>
            <td>👁️ ✎ ⋮</td>
        </tr>"""

    st.markdown(f"""<table class="doc-table">
        <thead><tr><th>Docente</th><th>Programa / Área</th><th>Asignaturas RAP</th><th>Horas asignadas</th><th>Estado</th><th>Última actualización</th><th>Acciones</th></tr></thead>
        <tbody>{html_rows}</tbody>
    </table>""", unsafe_allow_html=True)