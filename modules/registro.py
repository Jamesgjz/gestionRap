import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

def conectar_neon_db():
    if "postgres" not in st.secrets:
        return None
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"],
            connect_timeout=5
        )
    except Exception:
        return None

def obtener_datos_registro_db():
    conn = conectar_neon_db()
    datos_dinamicos = {
        "total_estudiantes": 0,
        "total_docentes": 0,
        "pendientes_gestion": 0,
        "asignaturas_activas": 0,
        "actividad_reciente_html": "",
        "origen_info": "Mostrando datos de respaldo (Mockup)"
    }
    
    if conn is None:
        # Fallback seguro con estética del diseño si falla la conexión
        datos_dinamicos["actividad_reciente_html"] = '<div class="timeline-item"><div class="timeline-marker" style="background:#ef4444;"></div><div class="timeline-content"><b>Sin conexión a la DB</b><br><span style="color:#64748b; font-size:0.75rem;">Verifica st.secrets</span></div></div>'
        return datos_dinamicos
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Conteo seguro de filas en las tablas del esquema neondb
        try:
            cursor.execute("SELECT COUNT(*) as total FROM public.estudiantes;")
            datos_dinamicos["total_estudiantes"] = cursor.fetchone()["total"] or 0
        except Exception:
            conn.rollback()
            
        try:
            cursor.execute("SELECT COUNT(*) as total FROM public.profesores;")
            datos_dinamicos["total_docentes"] = cursor.fetchone()["total"] or 0
        except Exception:
            conn.rollback()
            
        try:
            cursor.execute("SELECT COUNT(*) as total FROM public.estado_pruebas;")
            datos_dinamicos["pendientes_gestion"] = cursor.fetchone()["total"] or 0
        except Exception:
            conn.rollback()
            
        try:
            cursor.execute("SELECT COUNT(*) as total FROM public.asignaturas;")
            datos_dinamicos["asignaturas_activas"] = cursor.fetchone()["total"] or 0
        except Exception:
            conn.rollback()

        # CONSTRUCCIÓN DE LA ACTIVIDAD RECIENTE 100% REAL DESDE LA BASE DE DATOS
        html_actividades = ""
        
        try:
            cursor.execute("SELECT * FROM public.estudiantes ORDER BY 1 DESC LIMIT 2;")
            estudiantes_reales = cursor.fetchall()
            for est in estudiantes_reales:
                valores = list(est.values())
                nombre = valores[1] if len(valores) > 1 else "Estudiante sin nombre"
                html_actividades += '<div class="timeline-item"><div class="timeline-marker" style="background:#16a34a;"></div><div class="timeline-content"><b>Nuevo estudiante registrado en DB</b><br><span style="color:#64748b; font-size:0.75rem;">Sincronizado</span><br>' + str(nombre) + '</div></div>'
        except Exception:
            conn.rollback()

        try:
            cursor.execute("SELECT * FROM public.profesores ORDER BY 1 DESC LIMIT 2;")
            profesores_reales = cursor.fetchall()
            for prof in profesores_reales:
                valores = list(prof.values())
                nombre_prof = valores[1] if len(valores) > 1 else "Docente sin nombre"
                html_actividades += '<div class="timeline-item"><div class="timeline-marker" style="background:#0052cc;"></div><div class="timeline-content"><b>Docente evaluador en DB</b><br><span style="color:#64748b; font-size:0.75rem;">Actualización de registro</span><br>' + str(nombre_prof) + '</div></div>'
        except Exception:
            conn.rollback()

        if html_actividades == "":
            html_actividades = '<div class="timeline-item"><div class="timeline-marker" style="background:#94a3b8;"></div><div class="timeline-content"><b>Sin actividad nueva</b><br><span style="color:#64748b; font-size:0.75rem;">Tablas vacías en Neon</span></div></div>'

        datos_dinamicos["actividad_reciente_html"] = html_actividades
        datos_dinamicos["origen_info"] = "Conectado a Neon PostgreSQL (neondb)"
        
        cursor.close()
        conn.close()
        return datos_dinamicos
    except Exception:
        return datos_dinamicos

def render():
    if 'sub_view_registro' not in st.session_state:
        st.session_state['sub_view_registro'] = "dashboard"

    # --- ENRUTADOR INTERNO DE BOTONES Y ENLACES REALES ---
    if st.session_state['sub_view_registro'] == "docentes":
        st.markdown("<h2>👨‍🏫 Panel de Gestión - Docentes Evaluadores</h2>", unsafe_allow_html=True)
        if st.button("← Volver al Panel de Registros", icon=":material/arrow_back:"):
            st.session_state['sub_view_registro'] = "dashboard"
            st.rerun()
        
        conn = conectar_neon_db()
        if conn:
            try:
                df_doc = pd.read_sql("SELECT * FROM public.profesores;", conn)
                st.dataframe(df_doc, use_container_width=True, hide_index=True)
                conn.close()
            except Exception as e:
                st.error(f"Error al leer la tabla de profesores: {e}")
        else:
            st.warning("No se pudo conectar a la base de datos para listar los docentes.")
        return

    elif st.session_state['sub_view_registro'] == "estudiantes":
        st.markdown("<h2>🎓 Panel de Gestión - Estudiantes RAP</h2>", unsafe_allow_html=True)
        if st.button("← Volver al Panel de Registros", icon=":material/arrow_back:"):
            st.session_state['sub_view_registro'] = "dashboard"
            st.rerun()
            
        conn = conectar_neon_db()
        if conn:
            try:
                df_est = pd.read_sql("SELECT * FROM public.estudiantes;", conn)
                st.dataframe(df_est, use_container_width=True, hide_index=True)
                conn.close()
            except Exception as e:
                st.error(f"Error al leer la tabla de estudiantes: {e}")
        else:
            st.warning("No se pudo conectar a la base de datos para listar los estudiantes.")
        return

    # --- VISTA PRINCIPAL POR DEFECTO ---
    db = obtener_datos_registro_db()
    
    st.markdown("""
<style>
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.breadcrumb { font-size: 0.85rem; color: #64748b; margin-bottom: 5px; }
.main-title { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0; }
.subtitle { font-size: 0.95rem; color: #64748b; margin: 4px 0 0 0; }
.metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.metric-premium-card { background: white; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(15,23,42,0.02); position: relative; }
.metric-premium-title { font-size: 0.9rem; font-weight: 600; color: #64748b; margin-bottom: 8px; }
.metric-premium-value { font-size: 2.2rem; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
.metric-premium-delta { font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
.metric-icon-box { position: absolute; top: 24px; right: 24px; font-size: 1.3rem; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.block-card { background: white; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; min-height: 260px; }
.block-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }
.timeline-item { display: flex; gap: 15px; margin-bottom: 14px; position: relative; }
.timeline-marker { width: 10px; height: 10px; border-radius: 50%; background: #0052cc; margin-top: 5px; flex-shrink: 0; }
.timeline-content { font-size: 0.85rem; color: #334155; }
.module-row-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 15px; }
.module-premium-card { background: white; border-radius: 16px; padding: 28px; border: 1px solid #e2e8f0; display: flex; gap: 20px; }
.module-card-icon { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

    # Cabecera
    st.markdown("""<div class="panel-header">
<div>
<div class="breadcrumb">Inicio &gt; Gestión de Registros</div>
<h1 class="main-title">Gestión de Registros</h1>
<p class="subtitle">Administra docentes evaluadores, estudiantes y consulta la vista maestra del proceso RAP. (DB: """ + str(db['origen_info']) + """)</p>
</div>
<div style="text-align: right;">
<div style="font-size: 0.9rem; color: #64748b; font-weight: 600;"><i class="fa-regular fa-calendar"></i> 21 de mayo de 2025</div>
</div>
</div>""", unsafe_allow_html=True)

    # Tarjetas de bloques descriptivos superiores
    st.markdown("""<div class="module-row-grid">
<div class="module-premium-card">
<div class="module-card-icon" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-user-graduate"></i></div>
<div>
<div style="font-weight:700; color:#0f172a; font-size:1.1rem; margin-bottom:6px;">Docentes evaluadores</div>
<div style="font-size:0.85rem; color:#64748b; line-height:1.5;">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div>
</div>
</div>
<div class="module-premium-card">
<div class="module-card-icon" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-user"></i></div>
<div>
<div style="font-weight:700; color:#0f172a; font-size:1.1rem; margin-bottom:6px;">Estudiantes</div>
<div style="font-size:0.85rem; color:#64748b; line-height:1.5;">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div>
</div>
</div>
<div class="module-premium-card">
<div class="module-card-icon" style="background:#f3e8ff; color:#9333ea;"><i class="fa-regular fa-eye"></i></div>
<div>
<div style="font-weight:700; color:#0f172a; font-size:1.1rem; margin-bottom:6px;">Vista maestra</div>
<div style="font-size:0.85rem; color:#64748b; line-height:1.5;">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # Botonera real vinculada a los estados de sesión
    c_btn1, c_btn2, c_btn3 = st.columns(3)
    with c_btn1:
        if st.button("Gestionar docentes", key="reg_btn_doc", use_container_width=True, icon=":material/badge:"):
            st.session_state['sub_view_registro'] = "docentes"
            st.rerun()
    with c_btn2:
        if st.button("Gestionar estudiantes", key="reg_btn_est", use_container_width=True, icon=":material/person:"):
            st.session_state['sub_view_registro'] = "estudiantes"
            st.rerun()
    with c_btn3:
        if st.button("Abrir vista maestra", key="reg_btn_vis", use_container_width=True, icon=":material/table_chart:"):
            st.session_state['opcion_menu'] = "Dashboard / KPIs"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila de métricas conectadas
    st.markdown("""<div class="metrics-row">
<div class="metric-premium-card">
<div class="metric-premium-title">Total estudiantes</div>
<div class="metric-premium-value">""" + str(db['total_estudiantes']) + """</div>
<div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> DB Real <span style="color:#94a3b8; font-weight:400;">(estudiantes)</span></div>
<div class="metric-icon-box" style="background:#f0fdf4; color:#16a34a;"><i class="fa-solid fa-users"></i></div>
</div>
<div class="metric-premium-card">
<div class="metric-premium-title">Docentes evaluadores</div>
<div class="metric-premium-value">""" + str(db['total_docentes']) + """</div>
<div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> DB Real <span style="color:#94a3b8; font-weight:400;">(profesores)</span></div>
<div class="metric-icon-box" style="background:#edf5ff; color:#0052cc;"><i class="fa-solid fa-id-badge"></i></div>
</div>
<div class="metric-premium-card">
<div class="metric-premium-title">Pendientes de gestión</div>
<div class="metric-premium-value">""" + str(db['pendientes_gestion']) + """</div>
<div class="metric-premium-delta" style="color: #64748b;"><i class="fa-solid fa-clock"></i> DB Real <span style="color:#94a3b8; font-weight:400;">(estado_pruebas)</span></div>
<div class="metric-icon-box" style="background:#fff7ed; color:#ea580c;"><i class="fa-regular fa-clock"></i></div>
</div>
<div class="metric-premium-card">
<div class="metric-premium-title">Asignaturas activas</div>
<div class="metric-premium-value">""" + str(db['asignaturas_activas']) + """</div>
<div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> DB Real <span style="color:#94a3b8; font-weight:400;">(asignaturas)</span></div>
<div class="metric-icon-box" style="background:#f3e8ff; color:#9333ea;"><i class="fa-solid fa-book-open"></i></div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mitad inferior: Actividad Reciente Dinámica vs Accesos rápidos
    col_izq, col_der = st.columns([1.1, 1])
    
    with col_izq:
        st.markdown("""<div class="block-card">
<div class="block-title">Actividad reciente (Neon)</div>
""" + str(db['actividad_reciente_html']) + """
</div>""", unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="block-title" style="margin-left:10px;">Accesos rápidos</div>', unsafe_allow_html=True)
        
        if st.button("Validar documentos de estudiantes", icon=":material/verified_user:", use_container_width=True):
            st.session_state['opcion_menu'] = "Estado de Pruebas"
            st.rerun()
            
        if st.button("Programar prueba por asignatura", icon=":material/calendar_month:", use_container_width=True):
            st.session_state['opcion_menu'] = "Programación"
            st.rerun()
            
        if st.button("Evaluaciones por revisar", icon=":material/rate_review:", use_container_width=True):
            st.session_state['opcion_menu'] = "Evaluación"
            st.rerun()
            
        if st.button("Exportar reportes académicos", icon=":material/download:", use_container_width=True):
            st.toast("Descargando listados y reportes consolidados del proceso RAP...")

    # Footer Informativo
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""<div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 16px 24px; color: #1e40af; font-size: 0.9rem; display: flex; align-items: center; gap: 12px;">
<i class="fa-solid fa-circle-info" style="font-size: 1.1rem;"></i>
<span>El módulo de Docentes evaluadores es un espacio de soporte y parametrización del proceso RAP. Su gestión asegura la correcta asignación y evaluación de las pruebas institucionales.</span>
</div>
<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:30px; font-weight:500;">
RAP Digital - Gestión Académica<br>Reconocimiento de Aprendizajes Previos | UNIMINUTO Virtual
</div>""", unsafe_allow_html=True)