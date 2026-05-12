import streamlit as st
import pandas as pd
from database import traer_datos, ejecutar_query

def render():
    st.title("🏗️ Gestión y Monitoreo de Pruebas")

    # --- LLAVE MAESTRA DE EMERGENCIA ---
    # Si el login falla, este botón te dará acceso total para probar
    if st.session_state.get("rol") != "admin":
        if st.sidebar.button("🔓 Forzar Modo Admin (Pruebas)"):
            st.session_state["rol"] = "admin"
            st.session_state["usuario"] = "James Jaramillo"
            st.rerun()

    rol_actual = st.session_state.get("rol", "visitante")
    
    # 1. Carga de datos
    materias_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo ASC")
    profesores_db = traer_datos("SELECT id_profesor, nombre_completo FROM profesores")
    dict_profesores = {p[1]: p[0] for p in profesores_db}
    nombres_profes = ["Sin asignar"] + list(dict_profesores.keys())

    # --- CREACIÓN DE PESTAÑAS ---
    if rol_actual == "admin":
        # Aquí definimos las dos pestañas para el administrador
        tab_editor, tab_monitor = st.tabs(["🛠️ Panel de Edición", "📋 Monitor de Disponibilidad"])
        
        # CONTENIDO PESTAÑA EDITOR
        with tab_editor:
            st.subheader("Actualizar Avance de Pruebas")
            
            opciones_malla = {f"{m[0]} - {m[1]}": m[0] for m in materias_db}
            seleccion = st.selectbox("Seleccione asignatura:", ["Elija una..."] + list(opciones_malla.keys()), key="sb_admin")

            if seleccion != "Elija una...":
                alfa_edit = opciones_malla[seleccion]
                actual = traer_datos("SELECT estado, id_profesor FROM maestro_pruebas WHERE alfa_asignatura = %s", (alfa_edit,))
                est_act = actual[0][0] if actual else "Sin construir"
                id_p_act = actual[0][1] if actual else None

                with st.form("form_admin_final"):
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c1:
                        nuevo_est = st.selectbox("Estado", ["Sin construir", "En construcción", "Construida"],
                                                index=["Sin construir", "En construcción", "Construida"].index(est_act))
                    with c2:
                        nom_p_act = next((n for n, idp in dict_profesores.items() if idp == id_p_act), "Sin asignar")
                        nuevo_p = st.selectbox("Docente", nombres_profes, index=nombres_profes.index(nom_p_act))
                    with c3:
                        emoji = "🔴" if nuevo_est == "Sin construir" else "🟡" if nuevo_est == "En construcción" else "🟢"
                        st.markdown(f"<h2 style='text-align: center;'>{emoji}</h2>", unsafe_allow_html=True)
                    
                    if st.form_submit_button("💾 Guardar Cambios"):
                        ejecutar_query("""
                            INSERT INTO maestro_pruebas (alfa_asignatura, estado, id_profesor) 
                            VALUES (%s, %s, %s)
                            ON CONFLICT (alfa_asignatura) 
                            DO UPDATE SET estado = EXCLUDED.estado, id_profesor = EXCLUDED.id_profesor
                        """, (alfa_edit, nuevo_est, dict_profesores.get(nuevo_p)))
                        st.success("¡Actualizado!")
                        st.rerun()
    else:
        # Si no es admin, solo creamos una pestaña
        tabs = st.tabs(["📋 Monitor de Disponibilidad"])
        tab_monitor = tabs[0]
        tab_editor = None

    # --- CONTENIDO PESTAÑA MONITOR (Para todos) ---
    with tab_monitor:
        st.subheader("Estado actual de la malla curricular")
        data_vista = []
        for alfa, nombre in materias_db:
            res = traer_datos("SELECT estado, id_profesor FROM maestro_pruebas WHERE alfa_asignatura = %s", (alfa,))
            estado = res[0][0] if res else "Sin construir"
            id_p = res[0][1] if res else None
            nom_doc = next((n for n, idp in dict_profesores.items() if idp == id_p), "Por asignar")
            ind = "🔴 No disponible" if estado == "Sin construir" else "🟡 En proceso" if estado == "En construcción" else "🟢 DISPONIBLE"
            
            data_vista.append({"Código": alfa, "Asignatura": nombre, "Docente": nom_doc, "Estado": ind})
        
        st.table(pd.DataFrame(data_vista))