from hashlib import sha256
from secrets import token_urlsafe
from threading import Lock
from time import monotonic
from urllib.parse import parse_qs

import streamlit as st
from starlette.concurrency import run_in_threadpool
from starlette.responses import RedirectResponse, Response
from streamlit.errors import StreamlitSecretNotFoundError

from local_auth import (
    IDLE_SESSION_SECONDS, MAX_PASSWORD_LENGTH, TOTAL_SESSION_SECONDS, current_account, login_attempts,
    normalize_username, read_accounts, verify_password,
)
from rutas import ruta_valida


COOKIE_NAME = "__Host-rap_session"
MAX_SESSIONS = 2048
MAX_FORM_BYTES = 8192


def cuentas():
    try:
        return read_accounts(st.secrets.get("rap_accounts", {}))
    except StreamlitSecretNotFoundError:
        return {}


class Sesiones:
    def __init__(self):
        self.registros = {}
        self.lock = Lock()

    @staticmethod
    def clave(token):
        if not token or len(token) != 43 or not token.isascii():
            return None
        return sha256(token.encode("ascii")).digest()

    def abrir(self, usuario, cuenta, token_anterior):
        ahora = monotonic()
        token = token_urlsafe(32)
        with self.lock:
            self.registros.pop(self.clave(token_anterior), None)
            for clave, sesion in list(self.registros.items()):
                if self.caducada(sesion, ahora):
                    del self.registros[clave]
            if len(self.registros) >= MAX_SESSIONS:
                return None
            self.registros[self.clave(token)] = (usuario, cuenta.revision, ahora, ahora)
        return token

    @staticmethod
    def caducada(sesion, ahora):
        return ahora - sesion[2] >= TOTAL_SESSION_SECONDS or ahora - sesion[3] >= IDLE_SESSION_SECONDS

    def validar(self, token, cuentas_activas):
        clave = self.clave(token)
        if clave is None:
            return None
        with self.lock:
            ahora = monotonic()
            sesion = self.registros.get(clave)
            cuenta = current_account(sesion, cuentas_activas, ahora)
            if cuenta is None:
                self.registros.pop(clave, None)
            else:
                self.registros[clave] = (*sesion[:3], ahora)
        return cuenta

    def cerrar(self, token):
        with self.lock:
            self.registros.pop(self.clave(token), None)


sesiones = Sesiones()


def respuesta(ruta, aviso=None):
    destino = "./" + ruta
    if aviso:
        destino += "?acceso=" + aviso
    return RedirectResponse(destino, status_code=303, headers={"Cache-Control": "no-store"})


async def iniciar(request):
    if request.headers.get("sec-fetch-site") != "same-origin":
        return Response(status_code=403)
    if request.headers.get("content-type", "").split(";")[0] != "application/x-www-form-urlencoded":
        return Response(status_code=415)
    datos = bytearray()
    async for bloque in request.stream():
        if len(datos) + len(bloque) > MAX_FORM_BYTES:
            return Response(status_code=413)
        datos.extend(bloque)
    try:
        campos = parse_qs(datos.decode("utf-8"), max_num_fields=3)
    except (ValueError, UnicodeError):
        return Response(status_code=400)
    ruta = campos.get("ruta", [""])[0]
    if not ruta_valida(ruta):
        ruta = ""
    usuario = normalize_username(campos.get("usuario", [""])[0])
    password = campos.get("password", [""])[0]
    if not login_attempts.reserve(usuario):
        return respuesta(ruta, "intentos")
    account = cuentas().get(usuario)
    if len(password) > MAX_PASSWORD_LENGTH or not await run_in_threadpool(verify_password, password, account):
        return respuesta(ruta, "incorrecto")
    login_attempts.reset_account(usuario)
    token = sesiones.abrir(usuario, account, request.cookies.get(COOKIE_NAME))
    if token is None:
        return respuesta(ruta, "ocupado")
    response = respuesta(ruta)
    response.set_cookie(COOKIE_NAME, token, max_age=TOTAL_SESSION_SECONDS, secure=True, httponly=True, samesite="lax")
    return response


async def salir(request):
    if request.headers.get("sec-fetch-site") != "same-origin":
        return Response(status_code=403)
    sesiones.cerrar(request.cookies.get(COOKIE_NAME))
    response = respuesta("")
    response.delete_cookie(COOKIE_NAME, secure=True, httponly=True, samesite="lax")
    return response

