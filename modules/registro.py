import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    # Botón de regreso
    if st.button("← Volver"):
        st.session_state['reg_vista_actual'] = "resumen"
        st.rerun()

    st.subheader("Registrar / Actualizar Estudiante")
    
    # Lógica de datos
    estudiantes_carga = traer_datos("SELECT id_banner, nombre_completo FROM estudiantes ORDER BY nombre_completo")
    
    # Formulario limpio y funcional
    with st.form("form_estudiante_real", clear_on_submit=True):
        st.markdown("### 1. Datos generales")
        c1, c2 = st.columns(2)
        id_b = c1.number_input("ID Banner *", step=1, value=0)
        nom_e = c2.text_input("Nombre completo *")
        
        c3, c4 = st.columns(2)
        est = c3.selectbox("Estado *", ["Matriculado", "Admitido", "No matriculado"])
        correo = c4.text_input("Correo institucional")
        
        st.markdown("### 2. Asignación académica")
        mats_db = traer_datos("SELECT alfa, nombre_materia FROM asignaturas ORDER BY periodo")
        opts = {f"{m[1]} ({m[0]})": m[0] for m in mats_db} if mats_db else {}
        mats_sel = st.multiselect("Asignaturas RAP *", list(opts.keys()))
        
        submit = st.form_submit_button("🚀 Registrar / Actualizar Estudiante")
        
        if submit:
            if id_b <= 0 or not nom_e.strip():
                st.error("Por favor, ingresa un ID Banner válido y un nombre.")
            else:
                alfas = ",".join([opts[m] for m in mats_sel])
                try:
                    ejecutar_query("""
                        INSERT INTO estudiantes (id_banner, nombre_completo, estado_matricula, alfa_asignatura) 
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id_banner) DO UPDATE SET 
                            nombre_completo = EXCLUDED.nombre_completo,
                            estado_matricula = EXCLUDED.estado_matricula,
                            alfa_asignatura = EXCLUDED.alfa_asignatura
                    """, (id_b, nom_e, est, alfas))
                    st.success("¡Estudiante procesado correctamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")