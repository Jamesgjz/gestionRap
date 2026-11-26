import streamlit as st


def encabezado(titulo, descripcion):
    st.title(titulo, anchor=False)
    st.caption(descripcion)


def tarjetas_metricas(metricas):
    for columna, (etiqueta, valor) in zip(st.columns(len(metricas)), metricas):
        columna.metric(etiqueta, valor, border=True)


def tarjetas_acciones(acciones):
    for columna, (titulo, descripcion, boton, icono, callback, args) in zip(
        st.columns(len(acciones)), acciones
    ):
        with columna, st.container(border=True):
            st.subheader(titulo, anchor=False)
            st.caption(descripcion)
            st.button(boton, icon=icono, type="primary", width="stretch", on_click=callback, args=args)
