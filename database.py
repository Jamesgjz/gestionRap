import psycopg2
import os
import streamlit as st
from dotenv import load_dotenv

# Carga las variables del .env
load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT"),
            sslmode='require' # Neon siempre exige esto
        )
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def ejecutar_query(sql, params=None):
    conn = get_connection()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
        conn.close()

def traer_datos(sql, params=None):
    conn = get_connection()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        conn.close()
    return []