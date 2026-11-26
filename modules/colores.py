# Cada tono incluye un color de gráfico, un fondo claro y texto con contraste.
PALETA = {
    "verde": ("#00865D", "#E5F6EE", "#07563C"),
    "rojo": ("#C3374B", "#FDECEF", "#8B2031"),
    "ambar": ("#AD6509", "#FFF3DB", "#774305"),
    "azul": ("#1559D6", "#EAF2FF", "#163F88"),
    "turquesa": ("#087D86", "#E5F6F6", "#10565D"),
    "morado": ("#7134B8", "#F4EBFF", "#532889"),
    "gris": ("#667995", "#EEF2F7", "#3F526C"),
}

ESTADOS = {
    "aprobó": "verde", "aprobo": "verde", "aprobado": "verde",
    "reprobó": "rojo", "reprobo": "rojo", "reprobado": "rojo",
    "inasistencia": "ambar", "construida": "verde", "construido": "verde",
    "lista": "verde", "disponible": "verde", "en construcción": "ambar",
    "en construccion": "ambar", "sin construir": "gris", "completada": "verde",
    "asistió": "verde", "no asistió": "ambar", "con programación": "turquesa",
    "por programar": "ambar", "programada": "azul", "cancelada": "rojo", "pendiente": "ambar",
}


def tono_estado(valor):
    return ESTADOS.get(str(valor).strip().casefold())


def estilo_estado(valor):
    tono = tono_estado(valor)
    if not tono:
        return ""
    _, fondo, texto = PALETA[tono]
    return f"background-color: {fondo}; color: {texto}; font-weight: bold"
