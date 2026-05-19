import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    st.title("📝 Gestión de Registros")
    
    # Leemos el rol directamente de la sesión. Si no existe, por defecto es visitante.
    rol = st.session_state.get("rol", "visitante")
    
    t1, t2, t3 = st.tabs(["👨‍🏫 Docentes", "🎓 Estudiantes", "🔍 Vista Maestro"])
    
    with t1: # Registro Docentes
        st.subheader("Programar Nuevo Docente")
        with st.form("f_p", clear_on_submit=True):
            c1, c2 = st.columns([2, 1])
            nom_p = c1.text_input("Nombre del Profesor")
            hrs = c2.number_input("Horas", 1, 48, 1)
            if st.form_submit_button("💾 Guardar"):
                ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nom_p, hrs))
                st.success("Docente registrado")
                st.rerun()

        # --- NUEVA OPCIÓN: ELIMINAR DOCENTE (Solo Admin) ---
        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Docente")
            # Usamos el nombre exacto de tu columna: id_profesor
            profesores_db = traer_datos("SELECT id_profesor, nombre_completo FROM profesores ORDER BY nombre_completo")
            
            if profesores_db:
                # Mapeamos la lista usando el id_profesor real de tu base de datos
                opts_profes = {f"{p[1]} (ID: {p[0]})": p[0] for p in profesores_db}
                profe_sel = st.selectbox("Seleccione el docente a eliminar:", list(opts_profes.keys()), key="del_fe")
                
                if st.button("❌ Eliminar Docente Seleccionado"):
                    id_profe_del = opts_profes[profe_sel]
                    # Ejecutamos el DELETE usando la columna id_profesor
                    ejecutar_query("DELETE FROM profesores WHERE id_profesor = %s", (id_profe_del,))
                    st.error(f"Docente '{profe_sel}' eliminado correctamente.")
                    st.rerun()
            else:
                st.info("No hay docentes registrados para eliminar.")

    with t2: # Registro / Actualización de Estudiantes
        st.subheader("Registrar / Actualizar Estudiante")
        with st.form("f_e", clear_on_submit=True):
            c1, c2 = st.columns([1, 2])
            id_b = c1.number_input("ID Banner", step=1)
            nom_e = c2.text_input("Nombre Estudiante")
            est = st.selectbox("Estado", ["Matriculado", "Admitido", "No matriculado"])
            mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
            opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db}
            mats_sel = st.multiselect("Asignaturas", list(opts.keys()))
            
            if st.form_submit_button("🚀 Registrar / Actualizar"):
                if id_b <= 0 or not nom_e.strip():
                    st.error("Por favor, ingrese un ID Banner válido y el nombre del estudiante.")
                else:
                    alfas = ",".join([opts[m] for m in mats_sel])
                    
                    # Usamos ON CONFLICT para guardar o actualizar automáticamente según corresponda
                    ejecutar_query("""
                        INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id_banner) 
                        DO UPDATE SET 
                            nombre_completo = EXCLUDED.nombre_completo,
                            estado_matricula = EXCLUDED.estado_matricula,
                            alfa_asignatura = EXCLUDED.alfa_asignatura
                    """, (id_b, nom_e, est, alfas))
                    
                    st.success(f"¡Procesado correctamente! El estudiante con ID **{id_b}** ha sido guardado/actualizado.")
                    st.rerun()

        # --- NUEVA OPCIÓN: ELIMINAR ESTUDIANTE (Solo Admin) ---
        if rol == "admin":
            st.divider()
            st.subheader("🗑️ Eliminar Estudiante")
            estudiantes_db = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
            
            if estudiantes_db:
                opts_est = {f"{e[1]} (Banner: {e[0]})": e[0] for e in estudiantes_db}
                est_sel = st.selectbox("Seleccione el estudiante a eliminar:", list(opts_est.keys()), key="del_est")
                
                if st.button("❌ Eliminar Estudiante Seleccionado"):
                    id_banner_del = opts_est[est_sel]
                    ejecutar_query("DELETE FROM estudiantes WHERE id_banner = %s", (id_banner_del,))
                    st.error(f"Estudiante '{est_sel}' eliminado correctamente.")
                    st.rerun()
            else:
                st.info("No hay estudiantes registrados para eliminar.")

    with t3: # Vista Maestro con Semáforo Automático y Barra de Progreso
        st.subheader("Estado de Aplicación por Estudiante")
        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        if ests:
            total_estudiantes = len(ests)
            
            # 1. Crear el contenedor de la barra de progreso al inicio
            st.caption("Cargando el historial de estudiantes...")
            barra_progreso = st.progress(0)
            
            # 2. Iterar con un contador para calcular el porcentaje
            for indice, (idb, nom, alfas) in enumerate(ests):
                
                # Calcular el porcentaje actual de carga
                porcentaje = int(((indice + 1) / total_estudiantes) * 100)
                barra_progreso.progress(porcentaje)
                
                with st.expander(f"🎓 {nom} ({idb})"):
                    if not alfas:
                        st.info("Este estudiante no tiene asignaturas asignadas.")
                        continue
                    
                    lista_alfas = alfas.split(",")
                    cols = st.columns(len(lista_alfas))
                    
                    for i, alfa in enumerate(lista_alfas):
                        # Traer el Nombre Completo y el Estado de la prueba
                        info_materia = traer_datos("""
                            SELECT a.nombre_materia, m.estado 
                            FROM asignaturas a 
                            LEFT JOIN maestro_pruebas m ON a.alfa = m.alfa_asignatura 
                            WHERE a.alfa = %s
                        """, (alfa,))
                        
                        nombre_completo = info_materia[0][0] if info_materia else alfa
                        status = info_materia[0][1] if info_materia and info_materia[0][1] else "Sin construir"
                        
                        # Lógica de Semáforo
                        ready = "✅ Lista" if status == "Construida" else "⏳ Pendiente"
                        color = "#28a745" if status == "Construida" else "#ffc107" if status == "En construcción" else "#dc3545"
                        
                        # Renderizado visual
                        cols[i].markdown(f"""
                            <div style='border-left:5px solid {color}; background-color: #f8f9fa; padding:10px; border-radius:4px; height: 100px;'>
                                <div style='font-size: 0.8rem; font-weight: bold;'>{nombre_completo}</div>
                                <div style='font-size: 0.7rem; color: #555;'>{alfa}</div>
                                <div style='margin-top: 5px; font-size: 0.75rem;'>{ready}</div>
                            </div>
                        """, unsafe_allow_html=True)
            
            # 3. Limpiar o completar la barra cuando termine el proceso
            barra_progreso.empty() # Esto borra la barra una vez cargue todo para dejar la interfaz limpia
            st.success(f" Se cargaron {total_estudiantes} estudiantes con éxito.")
        else:
            st.info("No hay estudiantes registrados en el sistema.")