import streamlit as st
import streamlit.components.v1 as components

def render():
    # Estilos CSS específicos para los botones de la barra lateral (Arregla el contraste del menú)
    st.markdown("""
        <style>
        /* Forzar que los botones de la barra lateral tengan texto blanco y fondo transparente elegante */
        div[data-testid="stSidebar"] button {
            background-color: transparent !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 10px 15px !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stSidebar"] button:hover {
            background-color: #0056b3 !important;
            color: white !important;
            border-color: #0056b3 !important;
            box-shadow: 0 4px 12px rgba(0,86,179,0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # El Tablero Completo unificado dentro de un iframe limpio para evitar scrolls y espacios fantasma
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #fcfdfe;
                margin: 0;
                padding: 0;
                color: #0f172a;
                box-sizing: border-box;
            }
            
            /* ENCABEZADO */
            .dash-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 20px;
            }
            .header-title h1 { font-size: 2rem; font-weight: 800; margin: 0 0 5px 0; color: #0f172a; }
            .header-title p { color: #64748b; margin: 0; font-size: 0.95rem; }
            
            .search-box-container { text-align: right; }
            .search-mock {
                padding: 10px 16px;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                width: 280px;
                font-size: 0.9rem;
                color: #94a3b8;
                background: white;
                display: inline-block;
                text-align: left;
                box-shadow: 0 2px 5px rgba(0,0,0,0.01);
            }
            .date-mock { color: #64748b; font-size: 0.85rem; margin-top: 6px; }

            /* CONTENEDOR DE TARJETAS KPI */
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 25px;
            }
            .kpi-card {
                background: white;
                padding: 18px;
                border-radius: 14px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 4px 10px rgba(0,0,0,0.01);
            }
            .kpi-top { display: flex; justify-content: space-between; align-items: center; }
            .kpi-title { font-size: 0.85rem; color: #64748b; font-weight: 600; }
            .kpi-value { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 6px 0; }
            .kpi-trend { font-size: 0.8rem; font-weight: 700; }

            /* BLOQUES INFERIORES SÍNCRONOS */
            .blocks-grid {
                display: grid;
                grid-template-columns: 1.2fr 1fr 1fr;
                gap: 15px;
                margin-bottom: 25px;
            }
            .dash-block {
                background: white;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #e2e8f0;
                display: flex;
                flex-direction: column;
            }
            .block-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; }

            /* Listas internas sin paddings rotos */
            .data-list { display: flex; flex-direction: column; gap: 12px; font-size: 0.85rem; }
            .data-item { display: flex; justify-content: space-between; align-items: center; padding-bottom: 4px; }
            
            /* Barras de progreso */
            .progress-container { margin-bottom: 10px; }
            .progress-bar-bg { background: #e2e8f0; border-radius: 4px; height: 6px; width: 100%; margin-top: 4px; }
            .progress-bar-fill { height: 100%; border-radius: 4px; }
        </style>
    </head>
    <body>

        <!-- CABECERA -->
        <div class="dash-header">
            <div class="header-title">
                <h1>Panel de control</h1>
                <p>Bienvenido, James. El sistema está listo para apoyar la gestión académica del proceso RAP.</p>
            </div>
            <div class="search-box-container">
                <div class="search-mock"><i class="fa-solid fa-magnifying-glass"></i> Buscar estudiantes, pruebas...</div>
                <div class="date-mock">📅 06 de Julio de 2026</div>
            </div>
        </div>

        <!-- FILA 1: KPIs -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-top"><span class="kpi-title">Solicitudes activas</span><span style="color:#0056b3; background:#e6f0fa; padding:6px; border-radius:6px;"><i class="fa-regular fa-file-lines"></i></span></div>
                <div class="kpi-value">128</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top"><span class="kpi-title">Pruebas programadas</span><span style="color:#7c3aed; background:#f3e8ff; padding:6px; border-radius:6px;"><i class="fa-regular fa-calendar"></i></span></div>
                <div class="kpi-value">56</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top"><span class="kpi-title">Resultados pendientes</span><span style="color:#ea580c; background:#ffedd5; padding:6px; border-radius:6px;"><i class="fa-regular fa-clock"></i></span></div>
                <div class="kpi-value">34</div>
                <div class="kpi-trend" style="color:#ef4444;"><i class="fa-solid fa-arrow-up"></i> 6% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-top"><span class="kpi-title">Casos cerrados</span><span style="color:#16a34a; background:#dcfce7; padding:6px; border-radius:6px;"><i class="fa-regular fa-circle-check"></i></span></div>
                <div class="kpi-value">245</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 15% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
        </div>

        <!-- FILA 2: MAPEO DE BLOQUES SIN ESPACIOS INTERMEDIOS -->
        <div class="blocks-grid">
            
            <!-- PENDIENTES -->
            <div class="dash-block">
                <div class="block-title">Pendientes de gestión</div>
                <div class="data-list">
                    <div class="data-item"><span>👤 Validar documentos</span><strong>48</strong><span style="background:#fee2e2; color:#ef4444; padding:2px 6px; border-radius:4px; font-weight:700; font-size:0.75rem;">Alta</span></div>
                    <div class="data-item"><span>📅 Pruebas por programar</span><strong>26</strong><span style="background:#fef3c7; color:#d97706; padding:2px 6px; border-radius:4px; font-weight:700; font-size:0.75rem;">Media</span></div>
                    <div class="data-item"><span>📝 Evaluaciones por revisar</span><strong>18</strong><span style="background:#fee2e2; color:#ef4444; padding:2px 6px; border-radius:4px; font-weight:700; font-size:0.75rem;">Alta</span></div>
                    <div class="data-item"><span>📋 Resultados por registrar</span><strong>14</strong><span style="background:#fef3c7; color:#d97706; padding:2px 6px; border-radius:4px; font-weight:700; font-size:0.75rem;">Media</span></div>
                </div>
            </div>

            <!-- ACTIVIDAD -->
            <div class="dash-block">
                <div class="block-title">Actividad reciente</div>
                <div class="data-list" style="border-left: 2px solid #e2e8f0; padding-left: 12px;">
                    <div><b style="color:#0056b3;">● Nueva solicitud</b><br><span style="color:#64748b; font-size:0.8rem;">Estudiante: M. Fernanda Gómez</span></div>
                    <div><b style="color:#7c3aed;">● Prueba programada</b><br><span style="color:#64748b; font-size:0.8rem;">Competencia: Lectura Crítica</span></div>
                    <div><b style="color:#16a34a;">● Caso cerrado exitoso</b><br><span style="color:#64748b; font-size:0.8rem;">Estudiante: Juan C. Pérez</span></div>
                </div>
            </div>

            <!-- DISTRIBUCIÓN -->
            <div class="dash-block">
                <div class="block-title">Distribución por estado</div>
                <div class="data-list">
                    <div class="progress-container">
                        <div style="display:flex; justify-content:space-between;"><span>En evaluación</span><b>78 (25%)</b></div>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="background:#0056b3; width:25%;"></div></div>
                    </div>
                    <div class="progress-container">
                        <div style="display:flex; justify-content:space-between;"><span>Programadas</span><b>56 (18%)</b></div>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="background:#7c3aed; width:18%;"></div></div>
                    </div>
                    <div class="progress-container">
                        <div style="display:flex; justify-content:space-between;"><span>Pendientes</span><b>64 (21%)</b></div>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="background:#ea580c; width:21%;"></div></div>
                    </div>
                </div>
            </div>

        </div>

    </body>
    </html>
    """, height=520)

    # Las acciones rápidas las dejamos fuera como botones de Streamlit para la navegación responsiva nativa
    st.markdown("<h3 style='color:#0f172a; font-weight:700; font-size:1.2rem; margin-top:10px;'>Acciones rápidas</h3>", unsafe_allow_html=True)
    act1, act2, act3, act4 = st.columns(4)
    with act1:
        if st.button("➕ Registrar Estudiante", use_container_width=True):
            st.session_state['opcion_menu'] = "Registro Estudiantes"
            st.rerun()
    with act2:
        if st.button("📅 Programar Prueba", use_container_width=True):
            st.session_state['opcion_menu'] = "Programación"
            st.rerun()
    with act3:
        if st.button("📝 Registrar Resultado", use_container_width=True):
            st.session_state['opcion_menu'] = "Evaluación"
            st.rerun()
    with act4:
        if st.button("📊 Ver Reportes Analíticos", use_container_width=True):
            st.session_state['opcion_menu'] = "Dashboard / KPIs"
            st.rerun()