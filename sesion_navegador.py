from base64 import b64decode
from binascii import Error as Base64Error
from functools import lru_cache
import logging
from pathlib import Path
from secrets import token_urlsafe
from threading import Lock
from time import monotonic

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from local_auth import (
    IDLE_SESSION_SECONDS, TOTAL_SESSION_SECONDS, current_account, read_accounts,
)


SESSION_LIMIT = 2048
CONTEXT = b"gestionrap-session:v1:"
logger = logging.getLogger(__name__)


def cuentas_activas():
    try:
        return read_accounts(st.secrets.get("rap_accounts", {}))
    except StreamlitSecretNotFoundError:
        return {}


class Sesiones:
    def __init__(self):
        self.registros = {}
        self.lock = Lock()

    def abrir(self, sesion):
        identificador = token_urlsafe(32)
        ahora = monotonic()
        with self.lock:
            for clave, (anterior, _) in list(self.registros.items()):
                if ahora - anterior[2] >= TOTAL_SESSION_SECONDS or ahora - anterior[3] >= IDLE_SESSION_SECONDS:
                    del self.registros[clave]
            if len(self.registros) >= SESSION_LIMIT:
                return None
            self.registros[identificador] = (sesion, None)
        return identificador

    def validar(self, identificador, cuentas, *, tocar=True):
        with self.lock:
            registro = self.registros.get(identificador)
            if registro is None:
                return None
            sesion, clave = registro
            ahora = monotonic()
            if current_account(sesion, cuentas, ahora) is None:
                self.registros.pop(identificador, None)
                return None
            if tocar:
                sesion = (*sesion[:3], ahora)
                self.registros[identificador] = (sesion, clave)
            return sesion

    def inscrita(self, identificador):
        with self.lock:
            return self.registros.get(identificador, (None, None))[1] is not None

    def inscribir(self, identificador, valor):
        from cryptography.hazmat.primitives.asymmetric import ec

        datos = decodificar(valor, 65)
        if datos is None:
            return
        try:
            clave = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), datos)
        except ValueError:
            return
        with self.lock:
            registro = self.registros.get(identificador)
            if registro and registro[1] is None:
                self.registros[identificador] = (registro[0], clave)

    def recuperar(self, identificador, valor, reto, cuentas):
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import ec, utils

        if not isinstance(identificador, str) or len(identificador) != 43:
            return None
        firma = decodificar(valor, 64)
        if firma is None:
            return None
        with self.lock:
            registro = self.registros.get(identificador)
        if not registro or registro[1] is None:
            return None
        r, s = (int.from_bytes(firma[i:i+32], "big") for i in (0, 32))
        try:
            registro[1].verify(utils.encode_dss_signature(r, s),
                               CONTEXT + reto.encode("ascii"), ec.ECDSA(hashes.SHA256()))
        except (InvalidSignature, ValueError):
            return None
        return self.validar(identificador, cuentas)

    def cerrar(self, identificador):
        with self.lock:
            self.registros.pop(identificador, None)


def decodificar(valor, longitud):
    if not isinstance(valor, str) or len(valor) != 4 * ((longitud + 2) // 3):
        return None
    try:
        datos = b64decode(valor, validate=True)
    except (Base64Error, ValueError):
        return None
    return datos if len(datos) == longitud else None


sesiones = Sesiones()


@lru_cache(maxsize=1)
def componente():
    js = Path(__file__).with_name("sesion_navegador.js").read_text(encoding="utf-8")
    return st.components.v2.component("rap_sesion_navegador", html="<span hidden></span>", js=js)


def intercambiar(datos):
    try:
        with st.container(key="rap-sesion-navegador"):
            return componente()(key="rap_sesion_web", data=datos, on_reply_change=lambda: None).reply
    except Exception:
        logger.warning("La recuperación de sesión del navegador no está disponible.")
        return None


@st.fragment
def recuperar(cuentas):
    revocada = st.session_state.get("rap_revocada")
    if revocada:
        intercambiar({"revoke": revocada})
        return
    if st.session_state.get("rap_recuperacion_intentada"):
        return None
    if "rap_reto" not in st.session_state:
        st.session_state["rap_reto"] = (token_urlsafe(32), monotonic())
    reto, inicio = st.session_state["rap_reto"]
    respuesta = intercambiar({"challenge": reto})
    if not isinstance(respuesta, dict) or respuesta.get("operation") != reto:
        return None
    st.session_state["rap_recuperacion_intentada"] = True
    st.session_state.pop("rap_reto", None)
    valores = respuesta.get("result")
    if not isinstance(valores, dict) or monotonic() - inicio >= 60:
        return None
    identificador = valores.get("id")
    try:
        sesion = sesiones.recuperar(identificador, valores.get("proof"), reto, cuentas)
    except ImportError:
        return None
    if sesion is not None:
        st.session_state["rap_id"] = identificador
        st.session_state["rap_session"] = sesion
        st.rerun()


@st.fragment
def inscribir(identificador):
    if identificador is None or sesiones.inscrita(identificador) or st.session_state.get("rap_inscripcion_intentada"):
        return
    respuesta = intercambiar({"enroll": identificador})
    if not isinstance(respuesta, dict) or respuesta.get("operation") != identificador:
        return
    st.session_state["rap_inscripcion_intentada"] = True
    valores = respuesta.get("result")
    if isinstance(valores, dict) and valores.get("id") == identificador:
        try:
            sesiones.inscribir(identificador, valores.get("publicKey"))
        except ImportError:
            logger.warning("La verificación de sesión del navegador no está disponible.")

