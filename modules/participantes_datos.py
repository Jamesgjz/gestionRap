import csv
from io import StringIO
import re

from psycopg2 import sql
from psycopg2.extras import execute_values

from database import traer_datos, transaction


COLUMNAS_CSV = ("id_banner", "nombre_completo", "estado_matricula", "asignaturas", "observaciones")
ESTADOS_MATRICULA = ("Matriculado", "No matriculado")


def preparar_participante(banner, nombre, estado, asignaturas, observaciones, catalogo):
    banner = banner.strip()
    if not re.fullmatch(r"[0-9]{1,18}", banner) or int(banner) == 0:
        raise ValueError("ID Banner inválido.")
    if not nombre.strip():
        raise ValueError("Falta el nombre completo.")
    estados = {value.casefold(): value for value in ESTADOS_MATRICULA}
    estado = estados.get(estado.strip().casefold())
    if not estado:
        raise ValueError("Usa Matriculado o No matriculado.")
    codigos = list(dict.fromkeys(item.strip().upper() for item in asignaturas if item.strip()))
    if not codigos or any(codigo not in catalogo for codigo in codigos):
        raise ValueError("Verifica los códigos de asignatura de ese programa.")
    if len(observaciones.strip()) > 500:
        raise ValueError("Las observaciones admiten hasta 500 caracteres.")
    return int(banner), nombre.strip(), estado, ", ".join(codigos), observaciones.strip()


def leer_csv(data, catalogo):
    try:
        contenido = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        contenido = data.decode("cp1252")
    encabezado = contenido.splitlines()[0] if contenido else ""
    reader = csv.DictReader(StringIO(contenido, newline=""), delimiter=";" if ";" in encabezado else ",", strict=True)
    if reader.fieldnames is None:
        raise ValueError("El archivo está vacío.")
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
    requeridas = set(COLUMNAS_CSV[:4])
    if not requeridas.issubset(reader.fieldnames) or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError("La cabecera no coincide con la plantilla de importación.")

    registros, errores, vistos = [], [], set()
    for row in reader:
        if None in row or any(row[campo] is None for campo in requeridas):
            errores.append(f"Fila {reader.line_num}. Revisa la cantidad de columnas.")
            continue
        try:
            registro = preparar_participante(
                row["id_banner"], row["nombre_completo"], row["estado_matricula"],
                re.split(r"[|,]", row["asignaturas"]), row.get("observaciones") or "", catalogo,
            )
            if registro[0] in vistos:
                raise ValueError("ID Banner repetido dentro del archivo.")
        except ValueError as e:
            errores.append(f"Fila {reader.line_num}. {e}")
        else:
            vistos.add(registro[0])
            registros.append(registro)
    return registros, errores


def guardar_participantes(registros, programa_id):
    if not registros:
        return 0, 0

    with transaction() as cursor:
        # Serializa las altas de esta aplicación incluso en instalaciones antiguas.
        cursor.execute("SELECT pg_advisory_xact_lock(827725517)")
        cursor.execute("""
            SELECT id_banner::text FROM estudiantes
            WHERE ltrim(id_banner::text, '0') = ANY(%s)
        """, ([str(fila[0]) for fila in registros],))
        existentes = {value.lstrip("0") for (value,) in cursor.fetchall()}
        nuevos = [fila for fila in registros if str(fila[0]) not in existentes]
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_attribute WHERE attrelid = 'estudiantes'::regclass
                  AND attname = 'estado_matricula' AND NOT attisdropped
            )
        """)
        tiene_estado_legacy = cursor.fetchone()[0]
        columnas = ["id_banner", "nombre_completo", "estado_matriz", "alfa_asignatura",
                    "observaciones", "rap_programa_id"]
        valores = [(*fila, programa_id) for fila in nuevos]
        if tiene_estado_legacy:
            columnas.append("estado_matricula")
            valores = [(*fila, fila[2]) for fila in valores]

        if not valores:
            return 0, len(registros)
        comando = sql.SQL("INSERT INTO estudiantes ({}) VALUES %s ON CONFLICT DO NOTHING RETURNING id_banner").format(
            sql.SQL(", ").join(map(sql.Identifier, columnas)),
        )
        insertados = len(execute_values(cursor, comando, valores, page_size=500, fetch=True))
    traer_datos.clear()
    return insertados, len(registros) - insertados
