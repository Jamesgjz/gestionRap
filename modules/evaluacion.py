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
                # Buscamos las pruebas programadas
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
                    
                    opciones = {f"{r[2]} ({r[3]})": r[0] for r in res_progs}
                    seleccion = st.selectbox("Seleccione la Asignatura a Evaluar", list(opciones.keys()))
                    id_prog_sel = opciones[seleccion]

                    # Verificar existencia para EDITAR
                    nota_existente = traer_datos("""
                        SELECT asistencia, calificacion, resultado 
                        FROM notas 
                        WHERE id_programacion = %s
                    """, (id_prog_sel,))

                    asistencia_ini = True
                    calificacion_ini = 0.0
                    es_edicion = False

                    if nota_existente:
                        st.warning("⚠️ Esta prueba ya tiene una nota registrada. Si guarda cambios, se actualizarán los datos.")
                        asistencia_ini = nota_existente[0][0]
                        calificacion_ini = float(nota_existente[0][1])
                        es_edicion = True

                    with st.form("form_notas_v2"):
                        asistencia = st.radio("¿Asistió a la prueba?", [True, False], 
                                            index=0 if asistencia_ini else 1,
                                            format_func=lambda x: "SÍ" if x else "NO")
                        
                        if not asistencia:
                            calificacion = st.number_input("Calificación", value=0.0, disabled=True)
                            st.info("Nota automática de 0.0 por inasistencia.")
                        else:
                            calificacion = st.number_input("Calificación (0.0 - 5.0)", 
                                                          min_value=0.0, max_value=5.0, 
                                                          value=calificacion_ini, step=0.1)
                        
                        label_boton = "🔄 Actualizar Nota registrada" if es_edicion else "💾 Guardar Calificación"
                        if st.form_submit_button(label_boton):
                            if not asistencia:
                                resultado = "INASISTENCIA"
                                calificacion = 0.0
                            else:
                                resultado = "APROBÓ" if calificacion >= 3.5 else "REPROBÓ"

                            ejecutar_query("""
                                INSERT INTO notas (id_programacion, asistencia, calificacion, resultado)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (id_programacion) 
                                DO UPDATE SET 
                                    asistencia = EXCLUDED.asistencia,
                                    calificacion = EXCLUDED.calificacion,
                                    resultado = EXCLUDED.resultado
                            """, (id_prog_sel, asistencia, calificacion, resultado))
                            
                            st.success(f"✅ ¡{resultado}! Nota: {calificacion}")
                            st.rerun()
                else:
                    st.warning("No hay programaciones para este ID.")

    # --- PESTAÑA 2: HISTÓRICO CON SEMÁFORO ---
    with tabs[1]:
        st.subheader("Listado General de Notas")
        # SQL modificado sutilmente solo para recuperar el n.id_programacion necesario para la UI de borrado
        query_notas = """
            SELECT e.id_banner, e.nombre_completo, a.nombre_materia, n.asistencia, n.calificacion, n.resultado, n.id_programacion
            FROM notas n
            JOIN programacion_pruebas p ON n.id_programacion = p.id
            JOIN estudiantes e ON p.id_banner = e.id_banner
            JOIN asignaturas a ON TRIM(p.alfa_asignatura) = TRIM(a.alfa)
            ORDER BY n.id DESC
        """
        datos_notas = traer_datos(query_notas)
        
        if datos_notas:
            df_notas = pd.DataFrame(datos_notas, columns=[
                "ID Banner", "Estudiante", "Asignatura", "Asistió", "Nota", "Resultado", "id_prog_oculto"
            ])
            
            # Función de Semáforo
            def estilo_semaforo(row):
                resultado = row['Resultado']
                estilo = [''] * len(row)
                
                # Buscamos el índice de la columna 'Resultado'
                idx_res = df_notas.columns.get_loc('Resultado')
                
                if resultado == 'APROBÓ':
                    estilo[idx_res] = 'background-color: #d4edda; color: #155724; font-weight: bold; border: 1px solid #c3e6cb'
                elif resultado == 'REPROBÓ':
                    estilo[idx_res] = 'background-color: #f8d7da; color: #721c24; font-weight: bold; border: 1px solid #f5c6cb'
                elif resultado == 'INASISTENCIA':
                    estilo[idx_res] = 'background-color: #fff3cd; color: #856404; font-weight: bold; border: 1px solid #ffeeba'
                
                return estilo

            # Aplicar estilos (Ocultando la columna del ID de programación para que la tabla quede limpia)
            try:
                df_final = df_notas.style.apply(estilo_semaforo, axis=1)
            except:
                df_final = df_notas # En caso de error de pandas, muestra la tabla normal

            st.dataframe(df_final, use_container_width=True, hide_index=True, column_order=["ID Banner", "Estudiante", "Asignatura", "Asistió", "Nota", "Resultado"])
            
            # --- NUEVA FUNCIÓN: ELIMINAR CALIFICACIÓN (Solo Admin) ---
            if rol == "admin":
                st.divider()
                st.subheader("🗑️ Eliminar Registro de Calificación")
                st.info("Utilice esta opción si cometió un error de digitalización de raíz o si la prueba debe ser anulada para reprogramación.")
                
                # Generamos una lista estructurada para facilitar la búsqueda en el selectbox
                opciones_borrar_nota = {
                    f"Estudiante: {row[1]} ({row[0]}) | Asignatura: {row[2]} | Nota: {row[4]}": row[6]
                    for row in datos_notas
                }
                
                nota_sel = st.selectbox("Seleccione la calificación que desea eliminar permanentemente:", list(opciones_borrar_nota.keys()), key="del_nota_select")
                
                if st.button("❌ Eliminar Calificación Seleccionada"):
                    id_prog_del = opciones_borrar_nota[nota_sel]
                    
                    # Ejecutamos la remoción física del registro en la tabla de notas
                    ejecutar_query("DELETE FROM notas WHERE id_programacion = %s", (id_prog_del,))
                    
                    st.error(f"La calificación seleccionada ha sido eliminada del sistema.")
                    st.rerun()
        else:
            st.info("No hay registros de notas todavía.")