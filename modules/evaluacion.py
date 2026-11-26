import streamlit as st

from modules.ui import encabezado, panel


PAGE_SIZE = 25
CATALOGO = """
    LEFT JOIN LATERAL (
        SELECT nombre_materia
        FROM asignaturas WHERE trim(alfa) = trim(p.alfa_asignatura)
        ORDER BY nombre_materia LIMIT 1
    ) a ON true
"""


def calificar():
    with panel("evaluacion-buscar"):
        st.subheader("Buscar participante", anchor=False)
        with st.form("evaluacion_buscar", border=False):
            banner = st.text_input("ID Banner")
            buscar = st.form_submit_button("Buscar pruebas", type="primary", icon=":material/search:")
    if buscar:
        st.session_state.pop("evaluacion_banner", None)
        banner = banner.strip()
        if banner.isascii() and banner.isdecimal() and len(banner) <= 18:
            st.session_state["evaluacion_banner"] = int(banner)
        else:
            st.warning("Ingresa un ID Banner numérico válido.")

    banner = st.session_state.get("evaluacion_banner")
    if banner is None:
        return

    from database import ejecutar_query, traer_datos

    pruebas = traer_datos(f"""
        SELECT p.id, e.nombre_completo, COALESCE(a.nombre_materia, p.alfa_asignatura),
               p.alfa_asignatura, n.id_programacion IS NOT NULL,
               n.asistencia, n.calificacion, n.resultado
        FROM programacion_pruebas p
        JOIN estudiantes e ON e.id_banner = p.id_banner
        {CATALOGO}
        LEFT JOIN notas n ON n.id_programacion = p.id
        WHERE p.id_banner = %s
        ORDER BY p.fecha_aplicacion DESC, p.id DESC
    """, (banner,))
    if not pruebas:
        st.info("No hay pruebas programadas para este ID Banner.")
        return

    opciones = {row[0]: row for row in pruebas}
    with panel("evaluacion-nota"):
        st.subheader("Asistencia y calificación", anchor=False)
        st.text(pruebas[0][1])
        id_programacion = st.selectbox(
            "Prueba", list(opciones), key=f"evaluacion_prueba_{banner}",
            format_func=lambda id_: f"{opciones[id_][2]} · {opciones[id_][3]}",
        )
        _, _, _, _, registrada, asistencia_anterior, nota_anterior, resultado_anterior = opciones[id_programacion]
        if registrada:
            st.caption(f"Resultado registrado · {resultado_anterior or 'Pendiente'}")
        with st.form(f"evaluacion_nota_{id_programacion}", border=False):
            col_asistencia, col_nota = st.columns(2)
            asistencia = col_asistencia.radio(
                "¿Asistió a la prueba?", [True, False], index=0 if asistencia_anterior is not False else 1,
                format_func=lambda valor: "Sí" if valor else "No", horizontal=True,
            )
            nota = col_nota.number_input(
                "Calificación (0.0 – 5.0)", min_value=0.0, max_value=5.0,
                value=min(5.0, max(0.0, float(nota_anterior or 0.0))), step=0.1,
            )
            st.caption("Si no asistió, la calificación se guarda en 0.")
            label = "Actualizar calificación" if registrada else "Guardar calificación"
            if st.form_submit_button(label, icon=":material/save:", type="primary"):
                resultado = ("APROBÓ" if nota >= 3.5 else "REPROBÓ") if asistencia else "INASISTENCIA"
                nota = nota if asistencia else 0.0
                ejecutar_query("""
                    INSERT INTO notas (id_programacion, asistencia, calificacion, resultado)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id_programacion) DO UPDATE SET
                        asistencia = EXCLUDED.asistencia,
                        calificacion = EXCLUDED.calificacion,
                        resultado = EXCLUDED.resultado
                """, (id_programacion, asistencia, nota, resultado))
                st.session_state["evaluation_feedback"] = ("success", f"Resultado guardado · {resultado}. Nota: {nota}.")
                st.rerun()


def historial():
    from database import ejecutar_query, traer_datos

    with panel("evaluacion-historico"):
        st.subheader("Histórico de resultados", anchor=False)
        col_buscar, col_resultado = st.columns([2, 1])
        buscar = col_buscar.text_input("Buscar por nombre, ID Banner o asignatura").strip()
        estado = col_resultado.selectbox("Resultado", ("Todos", "APROBÓ", "REPROBÓ", "INASISTENCIA"))
        if (buscar, estado) != st.session_state.get("evaluacion_filtro"):
            st.session_state["evaluacion_filtro"] = (buscar, estado)
            st.session_state["evaluacion_pagina"] = 0

        pagina = st.session_state["evaluacion_pagina"]
        rows = traer_datos(f"""
            SELECT e.id_banner, e.nombre_completo, COALESCE(a.nombre_materia, p.alfa_asignatura),
                   n.asistencia, n.calificacion, n.resultado, n.id_programacion
            FROM notas n
            JOIN programacion_pruebas p ON n.id_programacion = p.id
            JOIN estudiantes e ON p.id_banner = e.id_banner
            {CATALOGO}
            WHERE (%s = 'Todos' OR n.resultado = %s)
              AND strpos(lower(concat_ws(' ', e.id_banner, e.nombre_completo,
                                         p.alfa_asignatura, a.nombre_materia)), lower(%s)) > 0
            ORDER BY n.id_programacion DESC
            LIMIT %s OFFSET %s
        """, (estado, estado, buscar, PAGE_SIZE + 1, PAGE_SIZE * pagina))
        if not rows and pagina:
            st.session_state["evaluacion_pagina"] = pagina - 1
            st.rerun()
        if not rows:
            st.info("No hay resultados para estos filtros.")
            return
        visibles = rows[:PAGE_SIZE]
        st.dataframe([
            {"ID Banner": row[0], "Participante": row[1], "Asignatura": row[2],
             "Asistió": row[3], "Nota": float(row[4]) if row[4] is not None else None, "Resultado": row[5]}
            for row in visibles
        ], hide_index=True, width="stretch")

        anterior, centro, siguiente = st.columns([1, 2, 1])
        if anterior.button("Anterior", disabled=pagina == 0, icon=":material/chevron_left:"):
            st.session_state["evaluacion_pagina"] -= 1
            st.rerun()
        centro.caption(f"Página {pagina + 1}")
        if siguiente.button("Siguiente", disabled=len(rows) <= PAGE_SIZE, icon=":material/chevron_right:"):
            st.session_state["evaluacion_pagina"] += 1
            st.rerun()

    with st.expander("Eliminar calificación", icon=":material/delete:"):
        opciones = {row[6]: f"{row[1]} ({row[0]}) · {row[2]} · Nota: {row[4]}" for row in visibles}
        id_programacion = st.selectbox("Calificación", list(opciones), format_func=opciones.__getitem__)
        if st.button("Confirmar eliminación de calificación"):
            eliminadas = ejecutar_query("DELETE FROM notas WHERE id_programacion = %s", (id_programacion,))
            st.session_state["evaluation_feedback"] = (
                ("success", "Calificación eliminada.") if eliminadas else ("warning", "La calificación ya no existe.")
            )
            st.rerun()


def render():
    encabezado("Evaluación", "Registra la asistencia y las calificaciones o consulta los resultados de las pruebas RAP.")
    if feedback := st.session_state.pop("evaluation_feedback", None):
        tipo, mensaje = feedback
        st.success(mensaje) if tipo == "success" else st.warning(mensaje)

    vista = st.segmented_control(
        "Vista de evaluación", ("Calificar prueba", "Histórico de resultados"),
        default="Calificar prueba", required=True, label_visibility="collapsed",
    )
    if vista == "Calificar prueba":
        calificar()
    else:
        historial()
