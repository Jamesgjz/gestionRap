import streamlit as st
import pandas as pd
from database import traer_datos, ejecutar_query
from datetime import datetime

def render():
    st.title("📅 Programación de Pruebas")
    
    if st.session_state.get("usuario") == "James Jaramillo":
        st.session_state["rol"] = "admin"
    
    rol = st.session_state.get("rol", "visitante")
    tabs = st.tabs(["📝 Agendar y Editar", "🔍 Registro de Pruebas"])

    # --- PESTAÑA 1: GESTIÓN ---
    with tabs[0]:
        if rol != "admin":
            st.warning("Acceso restringido al administrador.")
        else:
            st.subheader("Programar Nueva Prueba")
            id_banner = st.number_input("Ingrese ID Banner del Estudiante", step=1, value=0)
            
            if id_banner > 0:
                res_est = traer_datos("SELECT nombre_completo, alfa_asignatura FROM estudiantes WHERE id_banner = %s", (id_banner,))
                
                if res_est:
                    nombre_est = res_est[0][0]
                    materias_estudiante = [m.strip() for m in res_est[0][1].split(",")]
                    st.success(f"Estudiante: **{nombre_est}**")

                    materias_aptas = []
                    for alfa in materias_estudiante:
                        check = traer_datos("""
                            SELECT estado FROM maestro_pruebas 
                            WHERE TRIM(alfa_asignatura) = %s 
                            AND (estado ILIKE 'disponible' OR estado ILIKE 'construida' OR estado ILIKE 'lista')
                        """, (alfa,))
                        
                        if check:
                            nom_mat = traer_datos("SELECT nombre_materia FROM asignaturas WHERE TRIM(alfa) = %s", (alfa,))
                            nombre_texto = nom_mat[0][0] if nom_mat else "Nombre no definido"
                            materias_aptas.append(f"{alfa} - {nombre_texto}")

                    if materias_aptas:
                        with st.form("form_programacion_v5"):
                            col1, col2 = st.columns(2)
                            with col1:
                                seleccionada = st.selectbox("Asignatura Disponible", materias_aptas)
                                fecha_app = st.date_input("Fecha de la Prueba (Aplicación)")
                            with col2:
                                hora_app = st.time_input("Hora de la Prueba")
                            
                            
                            # ... (dentro de tu bloque de st.form_submit_button) ...

                            if st.form_submit_button("💾 Guardar Programación"):
                                alfa_sel = seleccionada.split(" - ")[0].strip()
                                fecha_hoy = datetime.now().date()
    
                                # Esta consulta ahora funcionará porque la DB ya sabe qué es lo "único"
                                ejecutar_query("""
                                    INSERT INTO programacion_pruebas (id_banner, alfa_asignatura, fecha_registro, fecha_aplicacion, hora)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON CONFLICT (id_banner, alfa_asignatura) 
                                    DO UPDATE SET 
                                    fecha_aplicacion = EXCLUDED.fecha_aplicacion, 
                                    hora = EXCLUDED.hora,
                                    fecha_registro = EXCLUDED.fecha_registro
    """, (id_banner, alfa_sel, fecha_hoy, fecha_app, hora_app))
    
                                st.success(f"¡Programación guardada! (ID: {id_banner} - {alfa_sel})")
                                st.rerun()
                    else:
                        st.warning("No hay materias listas para este estudiante.")
                else:
                    st.error("ID Banner no encontrado.")

    # --- PESTAÑA 2: VISTA ---
    with tabs[1]:
        st.subheader("Histórico de Programación")
        query_vista = """
            SELECT p.id_banner, e.nombre_completo, p.alfa_asignatura, p.fecha_registro, p.fecha_aplicacion, p.hora
            FROM programacion_pruebas p
            JOIN estudiantes e ON p.id_banner = e.id_banner
            ORDER BY p.fecha_registro DESC
        """
        datos = traer_datos(query_vista)
        
        if datos:
            df = pd.DataFrame(datos, columns=["ID Banner", "Estudiante", "Asignatura", "Fecha Registro", "Fecha Aplicación", "Hora"])
            st.table(df)
        else:
            st.info("Aún no hay pruebas programadas.")