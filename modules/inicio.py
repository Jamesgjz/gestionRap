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

def obtener_datos_dinamicos_dashboard():
    conn = conectar_neon_db()
    
    # Estructura base de respaldo alineada a la izquierda
    res = {
        "solicitudes_activas": 128,
        "pruebas_programadas": 31,
        "resultados_pendientes": 34,
        "casos_cerrados": 362,
        "tabla_pendientes_html": "<tr><td>Validar documentos de estudiantes</td><td><b>48</b></td><td><span class=\"pill-alta\">Alta</span></td><td>23 may. 2025</td></tr><tr><td>Pruebas por programar</td><td><b>26</b></td><td><span class=\"pill-media\">Media</span></td><td>24 may. 2025</td></tr><tr><td>Evaluaciones por revisar</td><td><b>18</b></td><td><span class=\"pill-alta\">Alta</span></td><td>25 may. 2025</td></tr><tr><td>Resultados por registrar</td><td><b>14</b></td><td><span class=\"pill-media\">Media</span></td><td>27 may. 2025</td></tr>",
        "actividad_reciente_html": "<div class=\"timeline-item\"><div class=\"timeline-marker\" style=\"background:#0052cc;\"></div><div class=\"timeline-content\"><b>Nueva solicitud recibida</b><br><span style=\"color:#64748b; font-size:0.75rem;\">Hoy, 09:15 a. m.</span><br>Estudiante: María Fernanda Gómez</div></div><div class=\"timeline-item\"><div class=\"timeline-marker\" style=\"background:#9333ea;\"></div><div class=\"timeline-content\"><b>Prueba programada</b><br><span style=" "color:#64748b; font-size:0.75rem;\">Hoy, 08:47 a. m.</span><br>Competencia: Lectura Crítica</div></div><div class=\"timeline-item\"><div class=\"timeline-marker\" style=\"background:#16a34a;\"></div><div class=\"timeline-content\"><b>Resultado registrado</b><br><span style=\"color:#64748b; font-size:0.75rem;\">Ayer, 04:32 p. m.</span><br>Estudiante: Juan Camilo Pérez</div></div>",
        "distribucion_html": "<div class=\"progress-bar-container\"><div class=" "progress-bar-labels\"><span>En evaluación</span><span>78 (25%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: 25%; background: #0052cc;\"></div></div></div><div class=\"progress-bar-container\"><div class=\"progress-bar-labels\"><span>Programadas</span><span>56 (18%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: 18%; background: #9333ea;\"></div></div></div><div class=\"progress-bar-container\"><div class=\"progress-bar-labels\"><span>Pendientes</span><span>64 (21%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: 21%; background: #ea580c;\"></div></div></div>",
        "origen_info": "Mostrando datos de respaldo (Mockup)"
    }
    
    if conn is None:
        return res
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        def contar_filas_tabla(nombre_tabla):
            try:
                cursor.execute("SELECT COUNT(*) as total FROM public." + str(nombre_tabla) + ";")
                return cursor.fetchone()["total"] or 0
            except Exception:
                conn.rollback()
                return 0
        
        c_seguimiento = contar_filas_tabla("seguimiento")
        c_programacion = contar_filas_tabla("programacion_pruebas")
        c_estado = contar_filas_tabla("estado_pruebas")
        c_estudiantes = contar_filas_tabla("estudiantes")
        c_notas = contar_filas_tabla("notas")
        c_profesores = contar_filas_tabla("profesores")
        
        if c_seguimiento > 0: res["solicitudes_activas"] = c_seguimiento
        if c_programacion > 0: res["pruebas_programadas"] = c_programacion
        if c_estado > 0: res["resultados_pendientes"] = c_estado
        if c_estudiantes > 0: res["casos_cerrados"] = c_estudiantes
        
        res["tabla_pendientes_html"] = "<tr><td>Flujos en Seguimiento</td><td><b>" + str(c_seguimiento) + "</b></td><td><span class=\"pill-alta\">Alta</span></td><td>Activo</td></tr><tr><td>Exámenes Programados</td><td><b>" + str(c_programacion) + "</b></td><td><span class=\"pill-media\">Media</span></td><td>Pendiente</td></tr><tr><td>Trazabilidad de Estados</td><td><b>" + str(c_estado) + "</b></td><td><span class=\"pill-alta\">Alta</span></td><td>En cola</td></tr><tr><td>Notas Registradas</td><td><b>" + str(c_notas) + "</b></td><td><span class=\"pill-media\">Media</span></td><td>Completado</td></tr>"
        
        try:
            cursor.execute("SELECT * FROM public.estudiantes ORDER BY 1 DESC LIMIT 3;")
            filas_est = cursor.fetchall()
            if filas_est:
                html_act = ""
                for est in filas_est:
                    valores = list(est.values())
                    nombre_visible = valores[1] if len(valores) > 1 else "Registro RAP"
                    html_act += "<div class=\"timeline-item\"><div class=\"timeline-marker\" style=\"background:#0052cc;\"></div><div class=\"timeline-content\"><b>Fila detectada en DB</b><br><span style=\"color:#64748b; font-size:0.75rem;\">Sincronización en tiempo real</span><br>Valor: " + str(nombre_visible) + "</div></div>"
                res["actividad_reciente_html"] = html_act
        except Exception:
            conn.rollback()
            
        total_volumen = c_notas + c_estudiantes + c_profesores
        if total_volumen > 0:
            p_notas = int((c_notas / total_volumen) * 100)
            p_est = int((c_estudiantes / total_volumen) * 100)
            p_prof = int((c_profesores / total_volumen) * 100)
            
            res["distribucion_html"] = "<div class=\"progress-bar-container\"><div class=\"progress-bar-labels\"><span>Volumen de Notas</span><span>" + str(c_notas) + " (" + str(p_notas) + "%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: " + str(p_notas) + "%; background: #0052cc;\"></div></div></div><div class=\"progress-bar-container\"><div class=\"progress-bar-labels"><span>Volumen de Estudiantes</span><span>" + str(c_estudiantes) + " (" + str(p_est) + "%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: " + str(p_est) + "%; background: #9333ea;\"></div></div></div><div class=\"progress-bar-container\"><div class=\"progress-bar-labels"><span>Volumen de Profesores</span><span>" + str(c_profesores) + " (" + str(p_prof) + "%)</span></div><div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" style=\"width: " + str(p_prof) + "%; background: #ea580c;\"></div></div></div>"
            
        res["origen_info"] = "Conectado a Neon PostgreSQL (neondb)"
        cursor.close()
        conn.close()
        return res
    except Exception:
        return res

def render():
    db = obtener_datos_dinamicos_dashboard()
    
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
.workspace-grid { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.block-card { background: white; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; }
.block-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }
.custom-table { width: 100%; border-collapse: collapse; text-align: left; }
.custom-table th { font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; padding: 10px 8px; border-bottom: 1px solid #f1f5f9; }
.custom-table td { font-size: 0.85rem; color: #334155; padding: 12px 8px; border-bottom: 1px solid #f1f5f9; }
.pill-alta { background: #ffeeef; color: #ef4444; padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; }
.pill-media { background: #fff7ed; color: #f97316; padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; }
.progress-bar-container { margin-bottom: 14px; }
.progress-bar-labels { display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 500; margin-bottom: 5px; }
.progress-bar-bg { background: #f1f5f9; height: 6px; border-radius: 3px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 3px; }
.bottom-grid { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 20px; }
.action-square-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.action-square-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
.action-square-card:hover { border-color: #0052cc; box-shadow: 0 10px 20px rgba(0,82,204,0.04); }
.timeline-item { display: flex; gap: 15px; margin-bottom: 14px; position: relative; }
.timeline-marker { width: 10px; height: 10px; border-radius: 50%; background: #0052cc; margin-top: 5px; flex-shrink: 0; }
.timeline-content { font-size: 0.85rem; color: #334155; }
.footer-link { font-size: 0.85rem; color: #0052cc; font-weight: 600; text-decoration: none; margin-top: 15px; display: inline-flex; align-items: center; gap: 5px; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

    parte_superior = """<div class="panel-header"><div><div class="breadcrumb">Inicio &gt; Panel de control</div><h1 class="main-title">Panel de control</h1><p class="subtitle">Bienvenido, James. Origen: """ + str(db['origen_info']) + """</p></div><div style="text-align: right;"><div style="font-size: 0.9rem; color: #64748b; font-weight: 600;"><i class="fa-regular fa-calendar"></i> 21 de mayo de 2025</div></div></div><div class="metrics-row"><div class="metric-premium-card"><div class="metric-premium-title">Solicitudes activas</div><div class="metric-premium-value">""" + str(db['solicitudes_activas']) + """</div><div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> Conectado <span style="color:#94a3b8; font-weight:400;">(seguimiento)</span></div><div class="metric-icon-box" style="background:#edf5ff; color:#0052cc;"><i class="fa-regular fa-file-lines"></i></div></div><div class="metric-premium-card"><div class="metric-premium-title">Pruebas programadas</div><div class="metric-premium-value">""" + str(db['pruebas_programadas']) + """</div><div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> Conectado <span style="color:#94a3b8; font-weight:400;">(programacion)</span></div><div class="metric-icon-box" style="background:#f3e8ff; color:#9333ea;"><i class="fa-regular fa-calendar"></i></div></div><div class="metric-premium-card"><div class="metric-premium-title">Resultados pendientes</div><div class="metric-premium-value">""" + str(db['resultados_pendientes']) + """</div><div class="metric-premium-delta" style="color: #ea580c;"><i class="fa-solid fa-clock"></i> Conectado <span style="color:#94a3b8; font-weight:400;">(estado_pruebas)</span></div><div class="metric-icon-box" style="background:#fff7ed; color:#ea580c;"><i class="fa-regular fa-clock"></i></div></div><div class="metric-premium-card"><div class="metric-premium-title">Casos cerrados</div><div class="metric-premium-value">""" + str(db['casos_cerrados']) + """</div><div class="metric-premium-delta" style="color: #22c55e;"><i class="fa-solid fa-arrow-up"></i> Conectado <span style="color:#94a3b8; font-weight:400;">(estudiantes)</span></div><div class="metric-icon-box" style="background:#f0fdf4; color:#16a34a;"><i class="fa-regular fa-circle-check"></i></div></div></div>"""

    parte_inferior = """<div class="workspace-grid"><div class="block-card"><div><div class="block-title">Métricas de Tablas (Neon)</div><table class="custom-table"><thead><tr><th>Componente DB</th><th>Filas Reales</th><th>Prioridad</th><th>Estado</th></tr></thead><tbody>""" + str(db['tabla_pendientes_html']) + """</tbody></table></div><div class="footer-link">Ver todas las pendientes <i class="fa-solid fa-arrow-right"></i></div></div><div class="block-card"><div><div class="block-title">Actividad reciente</div>""" + str(db['actividad_reciente_html']) + """</div><div class="footer-link">Ver toda la actividad <i class="fa-solid fa-arrow-right"></i></div></div><div class="block-card"><div><div class="block-title">Volumen Relativo de Datos</div>""" + str(db['distribucion_html']) + """</div><div class="footer-link">Ver reporte detallado <i class="fa-solid fa-arrow-right"></i></div></div></div><div class="bottom-grid"><div><div style="font-size: 1rem; font-weight:700; color:#0f172a; margin-bottom:15px;">Acciones rápidas</div><div class="action-square-grid"><div class="action-square-card"><div style="font-size:1.5rem; color:#0052cc;"><i class="fa-solid fa-user-plus"></i></div><div style="font-size:0.85rem; font-weight:600; color:#334155;">Registrar estudiante</div></div><div class="action-square-card"><div style="font-size:1.5rem; color:#9333ea;"><i class="fa-solid fa-calendar-plus"></i></div><div style="font-size:0.85rem; font-weight:600; color:#334155;">Programar prueba</div></div><div class="action-square-card"><div style="font-size:1.5rem; color:#ea580c;"><i class="fa-regular fa-square-check"></i></div><div style="font-size:0.85rem; font-weight:600; color:#334155;">Registrar resultado</div></div><div class="action-square-card"><div style="font-size:1.5rem; color:#16a34a;"><i class="fa-solid fa-chart-pie"></i></div><div style="font-size:0.85rem; font-weight:600; color:#334155;">Ver reportes</div></div></div></div><div class="block-card" style="padding: 20px 24px;"><div><div style="font-size: 1rem; font-weight:700; color:#0f172a; margin-bottom:15px;">Próximas actividades</div><div style="display:flex; align-items:center; gap:15px; margin-bottom:12px;"><div style="background:#eff6ff; border-radius:10px; padding:8px; text-align:center; min-width:45px;"><div style="font-size:0.7rem; font-weight:700; color:#0052cc; text-transform:uppercase;">May</div><div style="font-size:1.1rem; font-weight:800; color:#0052cc; line-height:1;">23</div></div><div style="font-size:0.85rem;"><div style="font-weight:700; color:#334155;">Reunión de coordinación RAP</div><div style="color:#64748b; font-size:0.75rem;"><i class="fa-regular fa-clock"></i> 10:00 a. m. - 11:00 a. m.</div></div></div></div><div class="footer-link" style="margin-top:5px;">Ver calendario completo <i class="fa-solid fa-arrow-right"></i></div></div></div>"""

    st.markdown(parte_superior + parte_inferior, unsafe_allow_html=True)