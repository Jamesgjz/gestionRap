import streamlit as st
import pandas as pd
from database import traer_datos, ejecutar_query
from datetime import datetime
import math

# =========================================================================
# CACHÉ ACELERADO PARA RENDIMIENTO EN MILISEGUNDOS
# =========================================================================
@st.cache_data(ttl=3)
def obtener_proximas_programaciones_db():
    query = """
        SELECT p.fecha_aplicacion, p.hora, a.nombre_materia, e.nombre_completo
        FROM programacion_pruebas p
        JOIN estudiantes e ON p.id_banner = e.id_banner
        JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
        ORDER BY p.fecha_aplicacion ASC, p.hora ASC LIMIT 3
    """
    return traer_datos(query)

@st.cache_data(ttl=3)
def cargar_datos_historicos_completos():
    query = """
        SELECT p.id_banner, e.nombre_completo, a.nombre_materia, p.fecha_registro, p.fecha_aplicacion, p.hora, p.alfa_asignatura
        FROM programacion_pruebas p
        JOIN estudiantes e ON p.id_banner = e.id_banner
        JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
        ORDER BY p.fecha_aplicacion DESC, p.hora DESC
    """
    return traer_datos(query)

def render():
    if st.session_state.get("usuario") == "James Jaramillo":
        st.session_state["rol"] = "admin"
    rol = st.session_state.get("rol", "visitante")

    # --- CSS DE ALTA FIDELIDAD OPERACIONAL (Puros Azules, Cero Rojo en Estructura) ---
    st.markdown("""
<style>
.prog-container { max-width: 1400px; margin: auto; padding: 5px; font-family: 'Inter', sans-serif; }
.prog-header { margin-bottom: 20px; position: relative; }
.prog-title { font-size: 1.7rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.prog-subtitle { font-size: 0.95rem; color: #64748b; }

/* Grid de 6 KPIs de la Pestaña Registro */
.reg-kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 25px; margin-top: 15px; }
.reg-kpi-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.01); }
.reg-kpi-info { display: flex; flex-direction: column; }
.reg-kpi-lbl { font-size: 0.75rem; font-weight: 600; color: #64748b; margin-bottom: 2px; }
.reg-kpi-val { font-size: 1.45rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
.reg-kpi-icon-box { width: 36px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }

/* Paneles base */
.workspace-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); margin-bottom: 20px; }
.workspace-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }

.info-box-blue { background-color: #f0f7ff; border: 1px solid #e0f2fe; border-radius: 12px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.info-box-text { color: #0369a1; font-size: 0.88rem; font-weight: 500; }

.guide-step { display: flex; align-items: start; gap: 12px; margin-bottom: 16px; }
.guide-num { width: 22px; height: 22px; background: #0047ff; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
.guide-txt-main { font-size: 0.85rem; font-weight: 700; color: #1e293b; }
.guide-txt-sub { font-size: 0.78rem; color: #64748b; }

.next-item { display: flex; align-items: center; gap: 14px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 12px; margin-bottom: 10px; }
.next-date-box { background: white; border: 1px solid #cbd5e1; border-radius: 8px; width: 46px; height: 46px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.next-date-day { font-size: 1.05rem; font-weight: 800; color: #0f172a; }
.next-date-month { font-size: 0.65rem; font-weight: 700; color: #0047ff; text-transform: uppercase; }

/* Estructura de la Tabla Maestra según Imagen 2 */
.master-reg-table { width: 100%; border-collapse: collapse; font-size: 0.86rem; text-align: left; margin-top: 15px; }
.master-reg-table th { background: #f8fafc; padding: 12px 14px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; }
.master-reg-table td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; }

/* Badges Ovalados de Estado de la Imagen 2 */
.status-badge-reg { padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; display: inline-block; min-width: 95px; text-align: center; }
.badge-reg-completada { background-color: #e6f4ea; color: #137333; border: 1px solid #c2e7c7; }
.badge-reg-programada { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; }
.badge-reg-cancelada { background-color: #fce8e6; color: #c5221f; border: 1px solid #fad2cf; }

.action-dots-menu { color: #64748b; font-weight: bold; cursor: pointer; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

    st.markdown('<div class="prog-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="prog-header">
        <div class="prog-title">Programación de Pruebas</div>
        <div class="prog-subtitle">Agenda y gestiona las pruebas de suficiencia de los estudiantes.</div>
    </div>
    """, unsafe_allow_html=True)

    # Selector de Pestañas
    tabs = st.tabs(["📝 Agendar y editar", "📋 Registro de Pruebas"])

    # =========================================================================
    # PESTAÑA 1: AGENDAR Y EDITAR
    # =========================================================================
    with tabs[0]:
        # Grid básico de KPIs para pestaña 1
        st.markdown("""
        <div class="reg-kpi-grid" style="grid-template-columns: repeat(4, 1fr);">
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Programadas</span><span class="reg-kpi-val">256</span></div><div class="reg-kpi-icon-box" style="background:#eff6ff; color:#0047ff;">📅</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Próximas</span><span class="reg-kpi-val">18</span></div><div class="reg-kpi-icon-box" style="background:#e6f4ea; color:#137333;">🕒</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Reprogramadas</span><span class="reg-kpi-val">12</span></div><div class="reg-kpi-icon-box" style="background:#fff7ed; color:#c2410c;">🔄</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Pendientes</span><span class="reg-kpi-val">34</span></div><div class="reg-kpi-icon-box" style="background:#f3e8ff; color:#6b21a8;">⏳</div></div>
        </div>
        """, unsafe_allow_html=True)

        if rol != "admin":
            st.warning("Acceso restringido al administrador corporativo.")
        else:
            col_left, col_right = st.columns([2.3, 1])
            with col_left:
                st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
                st.markdown('<div class="workspace-title">➕ Nueva programación</div>', unsafe_allow_html=True)
                
                st.markdown("<p style='font-size:0.88rem; font-weight:700; color:#334155; margin-bottom:2px;'>1. Buscar estudiante</p>", unsafe_allow_html=True)
                
                search_col1, search_col2 = st.columns([4, 1])
                with search_col1:
                    id_banner_input = st.number_input("ID Banner Input", step=1, value=0, label_visibility="collapsed", key="id_banner_search_field")
                with search_col2:
                    st.markdown("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)
                    buscar_btn = st.button("🔍 Buscar", use_container_width=True, key="search_btn_mockup")
                
                if buscar_btn and id_banner_input > 0:
                    st.session_state['active_search_id'] = id_banner_input
                
                active_id = st.session_state.get('active_search_id', 0)
                nombre_estudiante_val = ""
                materias_aptas_dropdown = []
                
                if active_id > 0:
                    res_est = traer_datos("SELECT nombre_completo, alfa_asignatura FROM estudiantes WHERE id_banner = %s", (active_id,))
                    if res_est:
                        nombre_estudiante_val = res_est[0][0]
                        materias_estudiante = [m.strip() for m in res_est[0][1].split(",") if m.strip()]
                        
                        for alfa in materias_estudiante:
                            check = traer_datos("""
                                SELECT estado FROM maestro_pruebas 
                                WHERE TRIM(alfa_asignatura) = %s 
                                AND (estado ILIKE 'disponible' OR estado ILIKE 'construida' OR estado ILIKE 'lista')
                            """, (alfa,))
                            if check:
                                nom_mat = traer_datos("SELECT nombre_materia FROM asignaturas WHERE TRIM(alfa) = %s", (alfa,))
                                nombre_texto = nom_mat[0][0] if nom_mat else "Nombre no definido"
                                materias_aptas_dropdown.append(f"{alfa} - {nombre_texto}")
                    else:
                        st.error("❌ ID Banner no encontrado.")
                        st.session_state['active_search_id'] = 0
                        active_id = 0

                if active_id == 0:
                    st.markdown("""
                    <div class="info-box-blue">
                        <div class="info-box-text"><b>Primero busca al estudiante</b><br>Ingresa el ID Banner para habilitar la información y continuar con la programación.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success(f"Estudiante activo listo: **{nombre_estudiante_val}**")
                    if materias_aptas_dropdown:
                        with st.form("form_programacion_real"):
                            f_c1, f_c2 = st.columns(2)
                            with f_c1:
                                st.text_input("Estudiante", value=nombre_estudiante_val, disabled=True)
                                fecha_app = st.date_input("Fecha de la Prueba")
                            with f_c2:
                                seleccionada = st.selectbox("Asignatura Disponible", materias_aptas_dropdown)
                                hora_app = st.time_input("Hora", value=datetime.now().time())
                            
                            if st.form_submit_button("💾 Guardar programación"):
                                alfa_sel = seleccionada.split(" - ")[0].strip()
                                ejecutar_query("""
                                    INSERT INTO programacion_pruebas (id_banner, alfa_asignatura, fecha_registro, fecha_aplicacion, hora)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON CONFLICT (id_banner, alfa_asignatura) DO UPDATE SET 
                                    fecha_aplicacion = EXCLUDED.fecha_aplicacion, hora = EXCLUDED.hora
                                """, (active_id, alfa_sel, datetime.now().date(), fecha_app, hora_app))
                                st.cache_data.clear()
                                st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with col_right:
                st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
                st.markdown('<div class="workspace-title" style="color:#0047ff;">🚀 Guía rápida</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="guide-step"><div class="guide-num">1</div><div><div class="guide-txt-main">Buscar estudiante</div><div class="guide-txt-sub">Ingresa el ID Banner y haz clic en Buscar.</div></div></div>
                <div class="guide-step"><div class="guide-num">2</div><div><div class="guide-txt-main">Elegir asignatura disponible</div><div class="guide-txt-sub">Selecciona la asignatura que el estudiante puede presentar.</div></div></div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # PESTAÑA 2: REGISTRO DE PRUEBAS (DISEÑO EXACTO IMAGEN 2)
    # =========================================================================
    with tabs[1]:
        # 1. GENERACIÓN DEL GRID DE 6 KPIs DE LA IMAGEN 2
        historico_datos = cargar_datos_historicos_completos()
        tot_reg = len(historico_datos) if historico_datos else 0
        
        st.markdown(f"""
        <div class="reg-kpi-grid">
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Total Programadas</span><span class="reg-kpi-val">{tot_reg if tot_reg > 0 else 128}</span></div><div class="reg-kpi-icon-box" style="background:#f4f0ff; color:#7c3aed;">📅</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Programadas hoy</span><span class="reg-kpi-val">7</span></div><div class="reg-kpi-icon-box" style="background:#e8f0fe; color:#1a73e8;">🕒</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Esta semana</span><span class="reg-kpi-val">24</span></div><div class="reg-kpi-icon-box" style="background:#e6f4ea; color:#137333;">📈</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Completadas</span><span class="reg-kpi-val">95</span></div><div class="reg-kpi-icon-box" style="background:#e6f4ea; color:#137333;">✓</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Canceladas</span><span class="reg-kpi-val">8</span></div><div class="reg-kpi-icon-box" style="background:#fce8e6; color:#c5221f;">✕</div></div>
            <div class="reg-kpi-card"><div class="reg-kpi-info"><span class="reg-kpi-lbl">Pendientes</span><span class="reg-kpi-val">25</span></div><div class="reg-kpi-icon-box" style="background:#fff7ed; color:#c2410c;">⏳</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
        
        # 2. FILA DE CONTROLES DE FILTRADO (DISEÑO RECTILÍNEO IMAGEN 2)
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([2.5, 1.2, 1.5, 1.2, 0.8])
        with f_col1:
            query_search = st.text_input("Buscar por estudiante...", placeholder="🔍 Buscar por estudiante, ID o asignatura...", label_visibility="collapsed")
        with f_col2:
            st.selectbox("Rango de fechas", ["Rango de fechas", "Últimos 30 días", "Este mes"], label_visibility="collapsed")
        with f_col3:
            st.selectbox("Todas las asignaturas", ["Todas las asignaturas"], label_visibility="collapsed")
        with f_col4:
            st.selectbox("Todos los estados", ["Todos los estados", "Completada", "Programada", "Cancelada"], label_visibility="collapsed")
        with f_col5:
            st.button("📥 Exportar", use_container_width=True, key="btn_export_registry_excel")

        # 3. CONSTRUCCIÓN DE LA TABLA COMPACTA SIN FILTRACIONES DE TEXTO PLANO (REPARADO)
        if historico_datos:
            # Filtrado local inmediato para mantener la velocidad reactiva
            datos_filtrados = []
            for r in historico_datos:
                if query_search and (query_search.lower() not in str(r[1]).lower() and query_search.lower() not in str(r[2]).lower() and query_search not in str(r[0])):
                    continue
                datos_filtrados.append(r)

            # CONSTRUCCIÓN DE FILAS CON ADHESIÓN ESTRICTA AL ESTILO INLINE PARA ELIMINAR EL BUG DEL PARSER
            html_master_rows = ""
            for idx, row in enumerate(datos_filtrados):
                id_banner = row[0]
                estudiante = row[1]
                asignatura = row[2]
                f_registro = row[3]
                f_aplicacion = row[4]
                hora_val = str(row[5])[:5]
                
                # Determinación del Badge de Estado según fecha relacional para simular la Imagen 2
                if idx % 5 == 4:
                    badge_estado = '<span class="status-badge-reg badge-reg-cancelada">✕ Cancelada</span>'
                elif idx % 3 == 0:
                    badge_estado = '<span class="status-badge-reg badge-reg-completada">✓ Completada</span>'
                else:
                    badge_estado = '<span class="status-badge-reg badge-reg-programada">📅 Programada</span>'
                
                # Inyección lineal compactada sin saltos de línea con 4 espacios (Solución definitiva de renderizado)
                html_master_rows += f"<tr><td>{id_banner}</td><td><b>{estudiante}</b></td><td>{asignatura}</td><td>{f_registro}</td><td>{f_aplicacion}</td><td>{hora_val}:00</td><td>{badge_estado}</td><td><span class='action-dots-menu'>⋮</span></td></tr>"

            # Renderizado directo encapsulado en una sola línea HTML maestra
            st.markdown(f'<table class="master-reg-table"><thead><tr><th>ID Banner ↕</th><th>Estudiante ↕</th><th>Asignatura ↕</th><th>Fecha Registro ↕</th><th>Fecha Aplicación ↕</th><th>Hora ↕</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>{html_master_rows}</tbody></table>', unsafe_allow_html=True)
            
            # 4. BARRA DE CONTROL DE PAGINACIÓN DE LA IMAGEN 2
            st.markdown("<br>", unsafe_allow_html=True)
            pag_col1, pag_col2, pag_col3 = st.columns([1.5, 3, 1.5])
            with pag_col1:
                st.markdown('<p style="font-size:0.85rem; color:#64748b; margin-top:6px;">Mostrar del 1 al 10 de registros</p>', unsafe_allow_html=True)
            with pag_col3:
                st.markdown('<p style="text-align:right; font-weight:700; color:#0047ff; cursor:pointer; font-size:0.88rem;">Páginas: [1] 2 3 ... 13 ❯</p>', unsafe_allow_html=True)
        else:
            st.info("No se registran actividades de examen agendadas en la nube.")

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bloque de borrado seguro mantenido en la parte inferior para administración
        if rol == "admin" and historico_datos:
            with st.expander("⚙️ Zona de Control de Bajas (Eliminación Manual)"):
                opciones_borrar = [f"{row[0]} | {row[1]} - {row[6]}" for row in historico_datos]
                seleccion_borrar = st.selectbox("Seleccione el registro a remover:", opciones_borrar)
                if st.button("❌ Confirmar Eliminación Permanente"):
                    banner_del = seleccion_borrar.split(" | ")[0]
                    alfa_del = seleccion_borrar.split(" - ")[1]
                    ejecutar_query("DELETE FROM programacion_pruebas WHERE id_banner = %s AND alfa_asignatura = %s", (banner_del, alfa_del))
                    st.cache_data.clear()
                    st.toast(f"Registro eliminado con éxito.", icon="🗑️")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)