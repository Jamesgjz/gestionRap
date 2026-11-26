import csv

import pandas as pd
import streamlit as st

from errors import DatabaseError
from modules.participantes_datos import COLUMNAS_CSV, guardar_participantes, leer_csv
from modules.programas_datos import catalogo_asignaturas, preparar_esquema, selector_programa
from modules.ui import encabezado, panel
from rutas import enlace


def render():
    enlace("registro", label="← Volver a registros")
    encabezado("Registro automático", "Importa participantes desde una plantilla CSV y revisa los datos antes de guardarlos.")
    if not preparar_esquema():
        return

    with panel("importacion-registro"):
        programa_id = selector_programa(key="csv_programa")
        catalogo = dict(catalogo_asignaturas(programa_id))
        if not catalogo:
            st.info("Vincula asignaturas al programa antes de importar.")
            return
        st.download_button(
            "Descargar plantilla CSV", (";".join(COLUMNAS_CSV) + "\r\n").encode("utf-8-sig"),
            "plantilla-participantes-rap.csv", mime="text/csv", on_click="ignore",
        )
        st.caption("Completa una fila por persona. Separa varios códigos de asignatura con |.")
        with st.expander("Ver códigos disponibles"):
            st.dataframe(pd.DataFrame(list(catalogo.items()), columns=["Código", "Asignatura"]),
                         hide_index=True, width="stretch")
        archivo = st.file_uploader("Archivo CSV", type=["csv"])
        if archivo is None:
            return
        try:
            registros, errores = leer_csv(archivo.getvalue(), catalogo)
        except (ValueError, csv.Error) as exc:
            st.error(f"No se pudo leer el archivo. {exc}")
            return
        if errores:
            filas = "fila" if len(errores) == 1 else "filas"
            st.error(f"Corrige {len(errores)} {filas} antes de importar.")
            st.write("\n".join(errores[:15]))
            return
        if not registros:
            st.info("La plantilla no contiene participantes.")
            return

        st.caption(f"Filas válidas: {len(registros)}. Los ID Banner ya registrados se omiten.")
        st.dataframe(pd.DataFrame(registros[:15], columns=COLUMNAS_CSV), hide_index=True, width="stretch")
        if st.button("Confirmar importación", type="primary", icon=":material/upload:"):
            try:
                insertados, omitidos = guardar_participantes(registros, programa_id)
            except DatabaseError:
                st.error("No se completó la importación. Revisa el archivo y la conexión.")
            else:
                st.success(f"Participantes registrados: {insertados}. Omitidos por duplicidad: {omitidos}.")
