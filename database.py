import psycopg2
import os
import streamlit as st
from dotenv import load_dotenv

# Carga las variables del .env solo para trabajo local
load_dotenv()

def get_connection():
    try:
        # 1. Intentar obtener credenciales de Streamlit Secrets (NUBE)
        if "postgres" in st.secrets:
            config = st.secrets["postgres"]
            return psycopg2.connect(
                host=config["host"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
                port=config["port"],
                sslmode='require'
            )
        
        # 2. Si no hay Secrets, usar variables de entorno (LOCAL)
        else:
            return psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                port=os.getenv("DB_PORT"),
                sslmode='require'
            )
    except Exception as e:
        # Imprimimos el error para depurar si algo falla
        st.error(f"❌ Error de conexión: {e}")
        return None

def ejecutar_query(sql, params=None):
    conn = get_connection()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    conn.commit()
        finally:
            conn.close()

def traer_datos(sql, params=None):
    conn = get_connection()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    return cur.fetchall()
        finally:
            conn.close()
    return []