from contextlib import contextmanager
import logging
import os

from dotenv import load_dotenv
import psycopg2
from psycopg2.pool import PoolError, ThreadedConnectionPool
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()
logger = logging.getLogger(__name__)


class DatabaseError(RuntimeError):
    pass


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
def transaction():
    pool = None
    conn = None
    discard = False
    try:
        pool = connection_pool()
        conn = pool.getconn()
        if conn.closed:
            pool.putconn(conn, close=True)
            conn = None
            conn = pool.getconn()
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


@st.cache_data(ttl=30, max_entries=256, show_spinner=False)
def traer_datos(sql, params=None):
    with transaction() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()
