from base64 import b64encode
from functools import lru_cache
from html import escape
from pathlib import Path

import streamlit as st

from modules.colores import PALETA, estilo_estado, tono_estado


@lru_cache(maxsize=1)
def css():
    return Path(__file__).with_name("rap.css").read_text(encoding="utf-8")


def aplicar_estilo():
    st.html(f"<style>{css()}</style>")


@lru_cache(maxsize=1)
def logo_institucional():
    archivo = Path(__file__).resolve().parents[1] / "assets" / "logo-uniminuto.png"
    imagen = b64encode(archivo.read_bytes()).decode("ascii")
    return f'<img class="rap-logo" src="data:image/png;base64,{imagen}" alt="UNIMINUTO" width="263" height="71">'


def acceso():
    with st.container(key="rap-login"):
        brand, form = st.columns([1, 1.1], gap=None)
        with brand:
            st.html(f"""
                <div class="rap-login-brand">
                    <div>
                        {logo_institucional()}
                        <h1>RAP Digital</h1>
                        <p>Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
                    </div>
                    <div class="rap-features"><span>Seguimiento</span><span>Evaluación</span><span>Trazabilidad académica</span></div>
                </div>
            """)
        return form.container(key="rap-login-form")


def perfil_lateral(nombre, rol):
    iniciales = "".join(palabra[0].upper() for palabra in nombre.split()[:2])
    etiqueta = "Administrador" if rol == "admin" else "Consulta"
    st.html(f"""
        <div class="rap-sidebar-logo">
            {logo_institucional()}
            <small>Virtual | RAP Digital</small>
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


def tarjetas_metricas(metricas, tonos=()):
    for i, (columna, (etiqueta, valor)) in enumerate(zip(st.columns(len(metricas)), metricas)):
        if not tonos:
            columna.metric(etiqueta, valor, border=True)
            continue
        with columna, st.container(key=f"rap-metric-{tonos[i]}-{i}"):
            st.metric(etiqueta, valor, border=True)


def etiqueta_estado(valor):
    _, fondo, texto = PALETA[tono_estado(valor) or "gris"]
    st.html(f'<span class="rap-status" style="background:{fondo}; color:{texto}">{escape(str(valor))}</span>')


def tabla_con_estados(datos, columnas, *, column_config=None, height="auto"):
    st.dataframe(
        datos.style.map(estilo_estado, subset=list(columnas)),
        hide_index=True, width="stretch", height=height, row_height=36, column_config=column_config,
    )


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
