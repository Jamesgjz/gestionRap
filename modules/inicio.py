import streamlit as st

def render():
    # --- CABECERA DE BIENVENIDA Y BUSCADOR ---
    c_path, c_search = st.columns([2, 1])
    with c_path:
        st.caption("Inicio > Panel de control")
        st.markdown("<h1 style='margin-top:-10px; color:#0f172a; font-weight:800;'>Panel de control</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#64748b; margin-top:-10px;'>Bienvenido, {st.session_state.get('usuario', 'Usuario')}. El sistema está listo para apoyar la gestión académica del proceso RAP.</p>", unsafe_allow_html=True)
    with c_search:
        st.text_input("🔍 Buscar estudiantes, pruebas, solicitudes...", placeholder="Presione Ctrl + K", label_visibility="collapsed")
        st.markdown("<div style='text-align:right; font-size:0.85rem; color:#64748b; padding-top:5px;'>📅 06 de Julio de 2026</div>", unsafe_allow_html=True)
        
    st.divider()
    
    # --- FILA 1: TARJETAS DE INDICADORES CLAVE (KPI CARDS) ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown("""
            <div class="kpi-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="kpi-title">Solicitudes activas</span>
                    <span style="color:#0056b3; background:#e6f0fa; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-regular fa-file-lines"></i></span>
                </div>
                <div class="kpi-value">128</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 12% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown("""
            <div class="kpi-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="kpi-title">Pruebas programadas</span>
                    <span style="color:#7c3aed; background:#f3e8ff; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-regular fa-calendar"></i></span>
                </div>
                <div class="kpi-value">56</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 8% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown("""
            <div class="kpi-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="kpi-title">Resultados pendientes</span>
                    <span style="color:#ea580c; background:#ffedd5; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-regular fa-clock"></i></span>
                </div>
                <div class="kpi-value">34</div>
                <div class="kpi-trend" style="color:#ef4444;"><i class="fa-solid fa-arrow-up"></i> 6% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown("""
            <div class="kpi-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="kpi-title">Casos cerrados</span>
                    <span style="color:#16a34a; background:#dcfce7; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-regular fa-circle-check"></i></span>
                </div>
                <div class="kpi-value">245</div>
                <div class="kpi-trend" style="color:#22c55e;"><i class="fa-solid fa-arrow-up"></i> 15% <span style="color:#94a3b8; font-weight:400;">vs. semana anterior</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- FILA 2: PENDIENTES, ACTIVIDAD Y DISTRIBUCIÓN ---
    col_b1, col_b2, col_b3 = st.columns([1.3, 1, 1])
    
    with col_b1:
        st.markdown('<div class="dash-block"><div class="block-title">Pendientes de gestión</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="display:flex; flex-direction:column; gap:16px; font-size:0.9rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
                    <span>👤 Validar documentos de estudiantes</span><strong>48</strong><span style="background:#fee2e2; color:#ef4444; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">Alta</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
                    <span>📅 Pruebas por programar</span><strong>26</strong><span style="background:#fef3c7; color:#d97706; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">Media</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
                    <span>📝 Evaluaciones por revisar</span><strong>18</strong><span style="background:#fee2e2; color:#ef4444; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">Alta</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:8px;">
                    <span>📋 Resultados por registrar</span><strong>14</strong><span style="background:#fef3c7; color:#d97706; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">Media</span>
                </div>
            </div>
            <div style="text-align:center; margin-top:35px;"><a href="#" style="color:#0056b3; font-weight:600; text-decoration:none; font-size:0.9rem;">Ver todas las pendientes ➔</a></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b2:
        st.markdown('<div class="dash-block"><div class="block-title">Actividad reciente</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="display:flex; flex-direction:column; gap:14px; font-size:0.85rem; border-left:2px solid #e2e8f0; padding-left:15px; margin-left:10px;">
                <div style="position:relative;"><span style="color:#0056b3; font-weight:700;">● Nueva solicitud recibida</span><br><span style="color:#64748b;">Estudiante: María Fernanda Gómez</span></div>
                <div style="position:relative;"><span style="color:#7c3aed; font-weight:700;">● Prueba programada</span><br><span style="color:#64748b;">Competencia: Lectura Crítica</span></div>
                <div style="position:relative;"><span style="color:#0056b3; font-weight:700;">● Resultado registrado</span><br><span style="color:#64748b;">Estudiante: Juan Camilo Pérez</span></div>
                <div style="position:relative;"><span style="color:#16a34a; font-weight:700;">● Documento validado</span><br><span style="color:#64748b;">Estudiante: Andrés Felipe Rojas</span></div>
            </div>
            <div style="text-align:center; margin-top:40px;"><a href="#" style="color:#0056b3; font-weight:600; text-decoration:none; font-size:0.9rem;">Ver toda la actividad ➔</a></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b3:
        st.markdown('<div class="dash-block"><div class="block-title">Distribución por estado</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="display:flex; flex-direction:column; gap:15px; font-size:0.85rem;">
                <div><div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>En evaluación</span><span>78 (25%)</span></div><div style="background:#e2e8f0; border-radius:4px; height:6px;"><div style="background:#0056b3; width:25%; height:100%; border-radius:4px;"></div></div></div>
                <div><div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Programadas</span><span>56 (18%)</span></div><div style="background:#e2e8f0; border-radius:4px; height:6px;"><div style="background:#7c3aed; width:18%; height:100%; border-radius:4px;"></div></div></div>
                <div><div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Pendientes</span><span>64 (21%)</span></div><div style="background:#e2e8f0; border-radius:4px; height:6px;"><div style="background:#ea580c; width:21%; height:100%; border-radius:4px;"></div></div></div>
                <div><div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Cerradas</span><span>245 (24%)</span></div><div style="background:#e2e8f0; border-radius:4px; height:6px;"><div style="background:#16a34a; width:24%; height:100%; border-radius:4px;"></div></div></div>
            </div>
            <div style="text-align:center; margin-top:35px;"><a href="#" style="color:#0056b3; font-weight:600; text-decoration:none; font-size:0.9rem;">Ver reporte detallado ➔</a></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- FILA 3: ACCIONES RÁPIDAS ---
    st.markdown("<h3 style='color:#0f172a; font-weight:700;'>Acciones rápidas</h3>", unsafe_allow_html=True)
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