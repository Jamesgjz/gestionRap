from database import ejecutar_query

def actualizar_catalogo():
    # 1. Limpiamos la tabla para evitar duplicados o datos viejos
    print("Limpiando tabla de asignaturas...")
    ejecutar_query("TRUNCATE TABLE asignaturas RESTART IDENTITY CASCADE")

    # 2. Lista oficial según la imagen
    materias = [
        ('ISOF V003', 'Introducción a la Ingeniería de Software', 1),
        ('ISOF V013', 'Desarrollo de Software Orientado a Objetos', 2),
        ('ISUD D063', 'Infraestructura de TI', 2),
        ('ISOF V023', 'Estructuras de Datos y Análisis de Algoritmos', 3),
        ('ISOF V033', 'Análisis y Diseño de Software', 3),
        ('ISOF V043', 'Sistemas de Gestión de Bases de Datos', 3),
        ('ISOF V053', 'Ingeniería de Software Avanzada', 4),
        ('ISOF V063', 'Desarrollo de Software Orientado a la Web', 4),
        ('ISOF V073', 'Data Warehouse y Minería de Datos', 4),
        ('ISUD D103', 'Sistemas Operativos', 4),
        ('ISOF V083', 'Diseño de Interfaces', 5),
        ('ISOF V093', 'Inteligencia de Negocios', 5),
        ('ISOF V103', 'Pruebas de Software y Aseguramiento de la Calidad', 6),
        ('ISOF V113', 'Infraestructura en la Nube', 6),
        ('ISOF V123', 'Seguridad en el Desarrollo de Software', 7),
        ('ISOF V133', 'Desarrollo de Software en Plataformas Móviles', 7),
        ('ISOF V143', 'Ethical Hacking y Seguridad de la Información', 7),
        ('ISOF V153', 'Computación Bioinspirada', 8),
        ('ISOF V163', 'Inteligencia Artificial y Sistemas Inteligentes', 8),
        ('ISOF V173', 'Gerencia de Proyectos de Software', 9),
        ('ISOF V183', 'Machine Learning', 9),
        ('ISOF V193', 'Plataformas de Desarrollo de Software', 9),
        ('UVFI V061', 'Fundamentos de Investigación', 9),
        ('ISOF V203', 'Administración y Gestión de la Configuración de Software', 10),
        ('UVFI V071', 'Metodología de la Investigación', 10)
    ]

    # 3. Insertar en la base de datos
    print("Insertando nuevas materias...")
    for alfa, nombre, periodo in materias:
        ejecutar_query(
            "INSERT INTO asignaturas (alfa, nombre_materia, periodo) VALUES (%s, %s, %s)",
            (alfa, nombre, periodo)
        )
    print("¡Proceso terminado con éxito!")

if __name__ == "__main__":
    actualizar_catalogo()