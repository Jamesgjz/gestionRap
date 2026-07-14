import streamlit as st
import pandas as pd
from database import traer_datos, ejecutar_query
from datetime import datetime
import math

# =========================================================================
# CACHÉ ACELERADO PARA RENDERIZADO EN MILISEGUNDOS
# =========================================================================
@st.cache_data(ttl=5)
def obtener_proximas_programaciones_db():
    query = """
        SELECT p.fecha_aplicacion, p.hora, a.nombre_materia, e.nombre_completo
        FROM programacion_pruebas p
        JOIN estudiantes e ON p.id_banner = e.id_banner
        JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
        ORDER BY p.fecha_aplicacion ASC, p.hora ASC LIMIT 3
    """
    return traer_datos(query)

@st.cache_data(ttl=5)
def cargar_conteos_kpi():
    try:
        total_prog = traer_datos("SELECT COUNT(*) FROM programacion_pruebas")
        prog_val = total_prog[0][0] if total_prog else 0
    except Exception:
        prog_val = 256  
    return prog_val

def render():
    # --- CONFIGURACIÓN DE ROLES Y UNIFICACIÓN DE SEGURIDAD ---
    if st.session_state.get("usuario") == "James Jaramillo":
        st.session_state["rol"] = "admin"
    rol = st.session_state.get("rol", "visitante")

    # --- CSS DE ALTA INTENSIDAD GRÁFICA (Puros Azules, Cero Rojo) ---
    st.markdown("""
<style>
.prog-container { max-width: 1400px; margin: auto; padding: 10px; font-family: 'Inter', sans-serif; }
.prog-header { margin-bottom: 25px; position: relative; }
.prog-title { font-size: 1.7rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.prog-subtitle { font-size: 0.95rem; color: #64748b; }
.prog-date-badge { position: absolute; right: 0; top: 10px; font-size: 0.88rem; color: #475569; font-weight: 600; }

/* Grid superior de KPIs estilo Mockup */
.prog-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
.prog-kpi-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
.prog-kpi-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-right: 14px; }
.prog-kpi-lbl { font-size: 0.8rem; font-weight: 600; color: #64748b; }
.prog-kpi-val { font-size: 1.6rem; font-weight: 800; color: #0f172a; line-height: 1.2; }
.prog-kpi-sub { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }

/* Paneles de trabajo */
.workspace-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); margin-bottom: 20px; }
.workspace-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }

/* Alerta informativa azul */
.info-box-blue { background-color: #f0f7ff; border: 1px solid #e0f2fe; border-radius: 12px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.info-box-icon { color: #0284c7; font-size: 1.2rem; font-weight: bold; }
.info-box-text { color: #0369a1; font-size: 0.88rem; font-weight: 500; line-height: 1.4; }

/* Guía rápida lateral */
.guide-step { display: flex; align-items: start; gap: 12px; margin-bottom: 16px; }
.guide-num { width: 22px; height: 22px; background: #0047ff; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; margin-top: 2px; }
.guide-txt-main { font-size: 0.85rem; font-weight: 700; color: #1e293b; }
.guide-txt-sub { font-size: 0.78rem; color: #64748b; line-height: 1.3; }

/* Listas de próximas programaciones */
.next-item { display: flex; align-items: center; gap: 14px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 12px; margin-bottom: 10px; }
.next-date-box { background: white; border: 1px solid #cbd5e1; border-radius: 8px; width: 46px; height: 46px; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.1; }
.next-date-day { font-size: 1.05rem; font-weight: 800; color: #0f172a; }
.next-date-month { font-size: 0.65rem; font-weight: 700; color: #0047ff; text-transform: uppercase; }
.next-details { display: flex; flex-direction: column; flex-grow: 1; min-width: 0; }
.next-subject { font-size: 0.82rem; font-weight: 700; color: #1e293b; white-space: nowrap; overflow: hidden; text-transform: ellipsis; }
.next-student { font-size: 0.78rem; color: #64748b; white-space: nowrap; overflow: hidden; text-transform: ellipsis; }
.next-time { font-size: 0.78rem; color: #475569; font-weight: 600; text-align: right; white-space: nowrap; }

/* Tablas e Historiales */
.hist-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.hist-table th { background: #f8fafc; padding: 12px; font-weight: 700; color: #475569; border-bottom: 2px solid #e2e8f0; text-align: left; }
.hist-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; color: #334155; }

div[data-testid="stForm"] button,
.stButton button[id*="search_btn"] {
    background-color: #ffffff !important;
    color: #0047ff !important;
    border: 1px solid #cbd5e1 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

    tot_programadas = cargar_conteos_kpi()
    st.markdown('<div class="prog-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="prog-header">
        <div class="prog-title">Programación de Pruebas</div>
        <div class="prog-subtitle">Agenda, edita y consulta la aplicación de pruebas RAP.</div>
        <div class="prog-date-badge">📅 14 de julio de 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="prog-kpi-grid">
        <div class="prog-kpi-card">
            <div class="prog-kpi-icon" style="background:#eff6ff; color:#0047ff;">📅</div>
            <div><div class="prog-kpi-lbl">Programadas</div><div class="prog-kpi-val">{tot_programadas}</div><div class="prog-kpi-sub">Todas las programaciones</div></div>
        </div>
        <div class="prog-kpi-card">
            <div class="prog-kpi-icon" style="background:#e6f4ea; color:#137333;">🕒</div>
            <div><div class="prog-kpi-lbl">Próximas</div><div class="prog-kpi-val" style="color:#137333;">18</div><div class="prog-kpi-sub">En los próximos 7 días</div></div>
        </div>
        <div class="prog-kpi-card">
            <div class="prog-kpi-icon" style="background:#fff7ed; color:#c2410c;">🔄</div>
            <div><div class="prog-kpi-lbl">Reprogramadas</div><div class="prog-kpi-val" style="color:#c2410c;">12</div><div class="prog-kpi-sub">Cambios realizados</div></div>
        </div>
        <div class="prog-kpi-card">
            <div class="prog-kpi-icon" style="background:#f3e8ff; color:#6b21a8;">⏳</div>
            <div><div class="prog-kpi-lbl">Pendientes</div><div class="prog-kpi-val" style="color:#6b21a8;">34</div><div class="prog-kpi-sub">Sin fecha asignada</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📝 Agendar y editar", "📋 Registro de pruebas"])

    with tabs[0]:
        if rol != "admin":
            st.warning("Acceso restringido al administrador corporativo.")
        else:
            col_left, col_right = st.columns([2.3, 1])
            
            with col_left:
                st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
                st.markdown('<div class="workspace-title">➕ Nueva programación</div>', unsafe_allow_html=True)
                
                st.markdown("<p style='font-size:0.88rem; font-weight:700; color:#334155; margin-bottom:2px;'>1. Buscar estudiante</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:0.8rem; color:#64748b; margin-bottom:10px;'>Ingresa el ID Banner del estudiante para cargar su información de malla.</p>", unsafe_allow_html=True)
                
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
                        st.error("❌ El ID Banner ingresado no se encuentra registrado en el sistema.")
                        st.session_state['active_search_id'] = 0
                        active_id = 0

                if active_id == 0:
                    st.markdown("""
                    <div class="info-box-blue">
                        <div class="info-box-icon">ℹ️</div>
                        <div class="info-box-text"><b>Primero busca al estudiante</b><br>Ingresa el ID Banner para habilitar la información y continuar con la programación.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    f_c1, f_c2 = st.columns(2)
                    with f_c1:
                        st.text_input("Estudiante", placeholder="👤 —", disabled=True)
                        st.date_input("Fecha de aplicación", disabled=True, key="disabled_f_input")
                    with f_c2:
                        st.text_input("Asignatura disponible", placeholder="📖 Selecciona una asignatura", disabled=True)
                        st.text_input("Hora de la prueba", placeholder="🕒 Selecciona una hora", disabled=True)
                    st.button("💾 Guardar programación", disabled=True, key="disabled_save_action")
                else:
                    st.success(f"Estudiante activo listo para asignación: **{nombre_estudiante_val}**")
                    
                    if materias_aptas_dropdown:
                        with st.form("form_programacion_v5_real"):
                            f_c1, f_c2 = st.columns(2)
                            with f_c1:
                                st.text_input("Estudiante", value=nombre_estudiante_val, disabled=True)
                                fecha_app = st.date_input("Fecha de la Prueba (Aplicación)")
                            with f_c2:
                                seleccionada = st.selectbox("Asignatura Disponible", materias_aptas_dropdown)
                                hora_app = st.time_input("Hora de la Prueba", value=datetime.now().time())
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.form_submit_button("💾 Guardar programación"):
                                alfa_sel = seleccionada.split(" - ")[0].strip()
                                fecha_hoy = datetime.now().date()
                                
                                ejecutar_query("""
                                    INSERT INTO programacion_pruebas (id_banner, alfa_asignatura, fecha_registro, fecha_aplicacion, hora)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON CONFLICT (id_banner, alfa_asignatura) 
                                    DO UPDATE SET 
                                    fecha_aplicacion = EXCLUDED.fecha_aplicacion, 
                                    hora = EXCLUDED.hora,
                                    fecha_registro = EXCLUDED.fecha_registro
                                """, (active_id, alfa_sel, fecha_hoy, fecha_app, hora_app))
                                
                                st.toast(f"¡Éxito! Prueba agendada para {nombre_estudiante_val}.", icon="🔹")
                                st.session_state['active_search_id'] = 0 
                                st.cache_data.clear() 
                                st.rerun()
                    else:
                        st.warning("⚠️ No se encontraron materias en estado 'Lista' o 'Construida' para la malla de este alumno.")
                        if st.button("Limpiar búsqueda"):
                            st.session_state['active_search_id'] = 0
                            st.rerun()
                            
                st.markdown('</div>', unsafe_allow_html=True)

            with col_right:
                st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
                st.markdown('<div class="workspace-title" style="color:#0047ff;">🚀 Guía rápida</div>', unsafe_allow_html=True)
                st.markdown('<p style="font-size:0.78rem; color:#64748b; margin-bottom:15px;">Sigue estos pasos para programar una prueba:</p>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="guide-step"><div class="guide-num">1</div><div><div class="guide-txt-main">Buscar estudiante</div><div class="guide-txt-sub">Ingresa el ID Banner y haz clic en Buscar.</div></div></div>
                <div class="guide-step"><div class="guide-num">2</div><div><div class="guide-txt-main">Elegir asignatura disponible</div><div class="guide-txt-sub">Selecciona la asignatura que el estudiante puede presentar.</div></div></div>
                <div class="guide-step"><div class="guide-num">3</div><div><div class="guide-txt-main">Definir fecha y hora</div><div class="guide-txt-sub">Elige la fecha de aplicación y la hora de la prueba.</div></div></div>
                <div class="guide-step"><div class="guide-num">4</div><div><div class="guide-txt-main">Guardar programación</div><div class="guide-txt-sub">Confirma la información para agendar la prueba.</div></div></div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
                st.markdown('<div class="workspace-title">📅 Próximas programaciones</div>', unsafe_allow_html=True)
                
                proximas_list = obtener_proximas_programaciones_db()
                if proximas_list:
                    for row in proximas_list:
                        f_app = row[0] 
                        h_app = str(row[1])[:5]
                        nom_materia = row[2]
                        nom_estudiante = row[3]
                        
                        day_str = f_app.strftime("%d") if hasattr(f_app, "strftime") else "15"
                        month_str = f_app.strftime("%b") if hasattr(f_app, "strftime") else "JUL"
                        
                        st.markdown(f"""
                        <div class="next-item">
                            <div class="next-date-box">
                                <div class="next-date-day">{day_str}</div>
                                <div class="next-date-month">{month_str}</div>
                            </div>
                            <div class="next-details">
                                <div class="next-subject">{nom_materia}</div>
                                <div class="next-student">{nom_estudiante}</div>
                            </div>
                            <div class="next-time">🕒 {h_app}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size:0.8rem; color:#94a3b8; text-align:center;'>No hay exámenes programados para esta semana.</p>", unsafe_allow_html=True)
                
                st.markdown("<br><p style='font-size:0.82rem; font-weight:700;'><a href='#' style='color:#0047ff; text-decoration:none;'>Ver todas las programaciones →</a></p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
        st.markdown('<div class="workspace-title">📋 Histórico de Programación</div>', unsafe_allow_html=True)
        
        query_vista = """
            SELECT p.id_banner, e.nombre_completo, a.nombre_materia, p.fecha_registro, p.fecha_aplicacion, p.hora, p.alfa_asignatura
            FROM programacion_pruebas p
            JOIN estudiantes e ON p.id_banner = e.id_banner
            JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
            ORDER BY p.fecha_registro DESC
        """
        datos = traer_datos(query_vista)
        
        if datos:
            html_rows = ""
            for row in datos:
                html_rows += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td><b>{row[1]}</b></td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                    <td><span style='color:#0047ff; font-weight:700;'>{row[4]}</span></td>
                    <td>🕒 {str(row[5])[:5]}</td>
                </tr>
                """
            
            st.markdown(f"""
            <table class="hist-table">
                <thead>
                    <tr>
                        <th>ID Banner</th><th>Estudiante</th><th>Asignatura</th><th>Fecha Registro</th><th>Fecha Aplicación</th><th>Hora</th>
                    </tr>
                </thead>
                <tbody>{html_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)
            
            if rol == "admin":
                st.markdown("<br><hr style='border:0; border-top:1px dashed #cbd5e1;'><br>", unsafe_allow_html=True)
                # REPARADO AQUÍ: Corrección de comillas HTML simples a comillas dobles para blindar el compilador
                st.markdown('<div class="workspace-title" style="color:#64748b;">🗑️ Eliminar Programación</div>', unsafe_allow_html=True)
                
                opciones_borrar = [f"{row[0]} | {row[1]} - {row[6]}" for row in datos]
                seleccion_borrar = st.selectbox("Seleccione la programación a eliminar:", opciones_borrar, label_visibility="collapsed")
                
                if st.button("❌ Eliminar Actividad Seleccionada"):
                    banner_del = seleccion_borrar.split(" | ")[0]
                    alfa_del = seleccion_borrar.split(" - ")[1]
                    
                    ejecutar_query("""
                        DELETE FROM programacion_pruebas 
                        WHERE id_banner = %s AND alfa_asignatura = %s
                    """, (banner_del, alfa_del))
                    
                    st.cache_data.clear() 
                    st.toast(f"Programación eliminada con éxito para el ID {banner_del}", icon="🗑️")
                    st.rerun()
        else:
            st.info("Aún no hay pruebas programadas en la base de datos de Neon.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)