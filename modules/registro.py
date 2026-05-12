import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    st.title("📝 Gestión de Registros")
    t1, t2, t3 = st.tabs(["👨‍🏫 Docentes", "🎓 Estudiantes", "🔍 Vista Maestro"])
    
    with t1: # Registro Docentes
        with st.form("f_p", clear_on_submit=True):
            c1, c2 = st.columns([2, 1])
            nom_p = c1.text_input("Nombre del Profesor")
            hrs = c2.number_input("Horas", 1, 48, 1)
            if st.form_submit_button("💾 Guardar"):
                ejecutar_query("INSERT INTO profesores (nombre_completo, horas_dedicacion) VALUES (%s,%s)", (nom_p, hrs))
                st.success("Docente registrado")

    with t2: # Registro Estudiantes
        with st.form("f_e", clear_on_submit=True):
            c1, c2 = st.columns([1, 2])
            id_b = c1.number_input("ID Banner", step=1)
            nom_e = c2.text_input("Nombre Estudiante")
            est = st.selectbox("Estado", ["Matriculado", "Admitido", "No matriculado"])
            mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
            opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db}
            mats_sel = st.multiselect("Asignaturas", list(opts.keys()))
            if st.form_submit_button("🚀 Registrar"):
                alfas = ",".join([opts[m] for m in mats_sel])
                ejecutar_query("INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) VALUES (%s,%s,%s,%s)", (id_b, nom_e, est, alfas))
                st.success("Estudiante registrado")

    with t3: # Vista Maestro con Semáforo Automático
        st.subheader("Estado de Aplicación por Estudiante")
        ests = traer_datos("SELECT id_banner, nombre_completo, alfa_asignatura FROM estudiantes")
        
        for idb, nom, alfas in ests:
            with st.expander(f"🎓 {nom} ({idb})"):
                lista_alfas = alfas.split(",")
                cols = st.columns(len(lista_alfas))
                
                for i, alfa in enumerate(lista_alfas):
                    # 1. Traer el Nombre Completo y el Estado de la prueba
                    info_materia = traer_datos("""
                        SELECT a.nombre_materia, m.estado 
                        FROM asignaturas a 
                        LEFT JOIN maestro_pruebas m ON a.alfa = m.alfa_asignatura 
                        WHERE a.alfa = %s
                    """, (alfa,))
                    
                    nombre_completo = info_materia[0][0] if info_materia else alfa
                    status = info_materia[0][1] if info_materia and info_materia[0][1] else "Sin construir"
                    
                    # 2. Lógica de Semáforo
                    ready = "✅ Lista" if status == "Construida" else "⏳ Pendiente"
                    color = "#28a745" if status == "Construida" else "#ffc107" if status == "En construcción" else "#dc3545"
                    
                    # 3. Renderizado visual
                    cols[i].markdown(f"""
                        <div style='border-left:5px solid {color}; background-color: #f8f9fa; padding:10px; border-radius:4px; height: 100px;'>
                            <div style='font-size: 0.8rem; font-weight: bold;'>{nombre_completo}</div>
                            <div style='font-size: 0.7rem; color: #555;'>{alfa}</div>
                            <div style='margin-top: 5px; font-size: 0.75rem;'>{ready}</div>
                        </div>
                    """, unsafe_allow_html=True)