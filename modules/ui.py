from html import escape
from pathlib import Path

import streamlit as st


def aplicar_estilo():
    st.html(Path(__file__).with_name("rap.css"))


def acceso():
    with st.container(key="rap-login"):
        st.html("""
            <div class="rap-login-masthead">
                <span aria-hidden="true">🎓</span><div>UNIMINUTO<small>Virtual · RAP Digital</small></div>
            </div>
        """)
        brand, form = st.columns([1, 1.1], gap=None)
        with brand:
            st.html("""
                <div class="rap-login-brand">
                    <div>
                        <span class="rap-product">RAP Digital</span>
                        <h1>UNIMINUTO<br><span>VIRTUAL</span></h1>
                        <p>Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
                    </div>
                    <div class="rap-features"><span>Seguimiento</span><span>Evaluación</span><span>Trazabilidad académica</span></div>
                </div>
            """)
        return form.container(key="rap-login-form")


def perfil_lateral(nombre, rol):
    iniciales = "".join(palabra[0].upper() for palabra in nombre.split()[:2])
    etiqueta = "Administrador" if rol == "admin" else "Consulta"
    st.html("""
        <div class="rap-sidebar-logo"><span aria-hidden="true">🎓</span>
            <div><strong>UNIMINUTO</strong><small>Virtual | RAP Digital</small></div>
        </div>
    """)
    st.html(f"""
        <div class="rap-profile">
            <div class="rap-identity">
                <span class="rap-avatar" aria-hidden="true">{escape(iniciales)}</span>
                <div><strong>{escape(nombre)}</strong><small>{etiqueta}</small></div>
            </div>
            <p class="rap-online">● En línea</p>
        </div>
    """)


def encabezado(titulo, descripcion):
    with st.container(key="rap-page-heading"):
        st.title(titulo, anchor=False)
        st.caption(descripcion)


def panel(nombre):
    return st.container(border=True, key=f"rap-panel-{nombre}")


def tarjetas_metricas(metricas):
    for columna, (etiqueta, valor) in zip(st.columns(len(metricas)), metricas):
        columna.metric(etiqueta, valor, border=True)


def tarjetas_acciones(acciones):
    pictograms = {
        ":material/person_add:": "👤",
        ":material/group:": "👤",
        ":material/school:": "🎓",
        ":material/table_view:": "👁️",
        ":material/calendar_month:": "📅",
        ":material/rate_review:": "📝",
        ":material/monitoring:": "📊",
    }
    for i, (columna, (titulo, descripcion, boton, icono, callback, args)) in enumerate(
        zip(st.columns(len(acciones), gap="small"), acciones)
    ):
        with columna, st.container(key=f"rap-action-{i}"):
            st.html(f"""
                <div class="rap-action-card">
                    <span class="rap-action-icon" aria-hidden="true">{pictograms[icono]}</span>
                    <strong>{escape(titulo)}</strong><p>{escape(descripcion)}</p>
                </div>
            """)
            st.button(boton, type="primary", width="stretch", on_click=callback, args=args)
