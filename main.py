from pathlib import Path

import streamlit as st
from starlette.routing import Route

from web_auth import iniciar, salir

prefijo = str(st.get_option("server.baseUrlPath") or "").strip("/")
rutas_sesion = [Route("/rap-iniciar", iniciar, methods=["POST"]),
                Route("/rap-salir", salir, methods=["POST"])]
if prefijo:
    rutas_sesion.extend((Route(f"/{prefijo}/rap-iniciar", iniciar, methods=["POST"]),
                         Route(f"/{prefijo}/rap-salir", salir, methods=["POST"])))

app = st.App(Path(__file__).with_name("gestion_rap.py"), routes=rutas_sesion)
