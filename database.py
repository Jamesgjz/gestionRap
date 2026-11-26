from contextlib import contextmanager
import logging
import os

from dotenv import load_dotenv
import psycopg2
from psycopg2.pool import PoolError, ThreadedConnectionPool
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from streamlit.runtime.scriptrunner import get_script_run_ctx

from errors import DatabaseError

load_dotenv()
logger = logging.getLogger(__name__)


@st.cache_resource
def connection_pool():
    try:
        settings = st.secrets.get("postgres", {})
    except StreamlitSecretNotFoundError:
        settings = {}
    config = {
        "host": settings.get("host") or os.getenv("DB_HOST"),
        "database": settings.get("database") or os.getenv("DB_NAME"),
        "user": settings.get("user") or os.getenv("DB_USER"),
        "password": settings.get("password") or os.getenv("DB_PASS"),
        "port": settings.get("port") or os.getenv("DB_PORT", "5432"),
        "sslmode": settings.get("sslmode") or os.getenv("DB_SSLMODE", "require"),
        "connect_timeout": 5,
    }
    if not all(config[key] for key in ("host", "database", "user", "password")):
        raise DatabaseError("Falta la configuración de PostgreSQL.")
    return ThreadedConnectionPool(1, 8, **config)


@contextmanager
def transaction(*, read_only=False, pool=None):
    if not read_only and get_script_run_ctx(suppress_warning=True) is not None:
        if st.session_state.get("rol") != "admin":
            raise DatabaseError("Esta cuenta tiene acceso de solo lectura.")
    conn = None
    discard = False
    try:
        if pool is None:
            pool = connection_pool()
        conn = pool.getconn()
        if conn.closed:
            pool.putconn(conn, close=True)
            conn = None
            conn = pool.getconn()
        conn.set_session(readonly=read_only)
        with conn, conn.cursor() as cursor:
            yield cursor
    except (psycopg2.Error, PoolError) as exc:
        discard = isinstance(exc, (psycopg2.InterfaceError, psycopg2.OperationalError))
        logger.warning("Operación de PostgreSQL fallida (%s, SQLSTATE %s)", type(exc).__name__, getattr(exc, "pgcode", None))
        raise DatabaseError("No se pudo completar la operación en PostgreSQL.") from exc
    finally:
        if conn is not None:
            pool.putconn(conn, close=discard)


def ejecutar_query(sql, params=None):
    with transaction() as cursor:
        cursor.execute(sql, params)
        affected = cursor.rowcount
    traer_datos.clear()
    return affected


def leer(sql, params=None, *, pool=None):
    # Reintenta solo lecturas ante una conexión interrumpida o un servidor iniciándose.
    for attempt in range(2):
        try:
            with transaction(read_only=True, pool=pool) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except DatabaseError as error:
            cause = error.__cause__
            code = getattr(cause, "pgcode", None)
            recoverable = isinstance(cause, (psycopg2.OperationalError, psycopg2.InterfaceError)) and (
                code is None or code.startswith("08") or code in {"57P01", "57P02", "57P03"}
            )
            if attempt or not recoverable:
                raise


@st.cache_data(ttl=30, max_entries=256, show_spinner=False)
def traer_datos(sql, params=None):
    return leer(sql, params)
