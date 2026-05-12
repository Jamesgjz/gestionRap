import streamlit as st
import pandas as pd
from database import traer_datos, ejecutar_query
from datetime import datetime

def render():
    st.title("📝 Módulo de Evaluación")
    
    if st.session_state.get("usuario") == "James Jaramillo":
        st.session_state["rol"] = "admin"
    
    rol = st.session_state.get("rol", "visitante")
    tabs = st.tabs(["🎯 Calificar Prueba", "📊 Histórico de Resultados"])

    # --- PESTAÑA 1: CALIFICACIÓN ---
    with tabs[0]:
        if rol != "admin":
            st.warning("Acceso restringido al administrador.")
        else:
            st.subheader("Registrar / Actualizar Nota")
            id_banner = st.number_input("ID Banner del Estudiante", step=1, value=0, key="eval_banner")
            
            if id_banner > 0:
                # Buscamos las pruebas programadas activas para este estudiante
                # Traemos el id_programacion para insertarlo en la tabla 'notas'
                res_progs = traer_datos("""
                    SELECT p.id, e.nombre_completo, a.nombre_materia, p.alfa_asignatura 
                    FROM programacion_pruebas p
                    JOIN estudiantes e ON p.id_banner = e.id_banner
                    JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
                    WHERE e.id_banner = %s
                """, (id_banner,))
                
                if res_progs:
                    nombre_est = res_progs[0][1]
                    st.success(f"Estudiante: **{nombre_est}**")
                    
                    # Diccionario para manejar la selección
                    opciones = {f"{r[2]} ({r[3]})": r[0] for r in res_progs}
                    seleccion = st.selectbox("Seleccione la Asignatura a Evaluar", list(opciones.keys()))
                    id_prog_sel = opciones[seleccion]

                    # Verificar si ya existe registro en la tabla 'notas'
                    nota_existente = traer_datos("""
                        SELECT asistencia, calificacion, resultado 
                        FROM notas 
                        WHERE id_programacion = %s
                    """, (id_prog_sel,))

                    # Valores iniciales (por defecto o recuperados)
                    asistencia_ini = True
                    calificacion_ini = 0.0
                    es_edicion = False

                    if nota_existente:
                        st.info("Ya existe una calificación. Puede editarla abajo.")
                        asistencia_ini = nota_existente[0][0]
                        calificacion_ini = float(nota_existente[0][1])
                        es_edicion = True

                    with st.form("form_notas"):
                        asistencia = st.radio("¿Asistió a la prueba?", [True, False], 
                                            index=0 if asistencia_ini else 1,
                                            format_func=lambda x: "SÍ" if x else "NO")
                        
                        if not asistencia:
                            calificacion = st.number_input("Calificación", value=0.0, disabled=True)
                        else:
                            calificacion = st.number_input("Calificación (0.0 - 5.0)", 
                                                          min_value=0.0, max_value=5.0, 
                                                          value=calificacion_ini, step=0.1)
                        
                        if st.form_submit_button("💾 Guardar Calificación"):
                            # Lógica de negocio solicitada
                            if not asistencia:
                                resultado = "INASISTENCIA"
                                calificacion = 0.0
                            else:
                                resultado = "APROBÓ" if calificacion >= 3.5 else "REPROBÓ"

                            # Guardar en la tabla 'notas' según tu imagen
                            ejecutar_query("""
                                INSERT INTO notas (id_programacion, asistencia, calificacion, resultado)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (id_programacion) 
                                DO UPDATE SET 
                                    asistencia = EXCLUDED.asistencia,
                                    calificacion = EXCLUDED.calificacion,
                                    resultado = EXCLUDED.resultado
                            """, (id_prog_sel, asistencia, calificacion, resultado))
                            
                            st.success(f"Registro guardado: {resultado} ({calificacion})")
                            st.rerun()
                else:
                    st.warning("No hay programaciones pendientes para este ID.")

    # --- PESTAÑA 2: HISTÓRICO ---
    with tabs[1]:
        st.subheader("Listado General de Notas")
        query_notas = """
            SELECT e.id_banner, e.nombre_completo, a.nombre_materia, n.asistencia, n.calificacion, n.resultado
            FROM notas n
            JOIN programacion_pruebas p ON n.id_programacion = p.id
            JOIN estudiantes e ON p.id_banner = e.id_banner
            JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
            ORDER BY n.id DESC
        """
        datos_notas = traer_datos(query_notas)
        
        if datos_notas:
            df_notas = pd.DataFrame(datos_notas, columns=[
                "ID Banner", "Estudiante", "Asignatura", "Asistió", "Nota", "Resultado"
            ])
            
            # Estilo visual para aprobados/reprobados
            def resaltar_resultado(val):
                color = 'red' if val in ['REPROBÓ', 'INASISTENCIA'] else 'green'
                return f'color: {color}; font-weight: bold'

            st.table(df_notas.style.applymap(resaltar_resultado, subset=['Resultado']))
        else:
            st.info("No hay registros de notas todavía.")