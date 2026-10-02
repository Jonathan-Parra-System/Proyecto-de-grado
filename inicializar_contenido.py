import json

from conexion import conectar_db
from lecciones import CURSOS, MODULOS


EVALUACION_INICIAL = {
    "slug": "informatica-basica",
    "titulo": "Evaluación de informática básica",
    "descripcion": "Comprueba lo aprendido sobre las partes del computador.",
    "curso": "informatica-basica",
    "preguntas": [
        {
            "pregunta": "¿Cuál dispositivo permite introducir texto?",
            "opciones": [
                {"valor": "monitor", "etiqueta": "Monitor"},
                {"valor": "teclado", "etiqueta": "Teclado"},
                {"valor": "parlantes", "etiqueta": "Parlantes"},
            ],
            "respuesta": "teclado",
        },
        {
            "pregunta": "¿Qué dispositivo muestra información en pantalla?",
            "opciones": [
                {"valor": "mouse", "etiqueta": "Mouse"},
                {"valor": "monitor", "etiqueta": "Monitor"},
                {"valor": "teclado", "etiqueta": "Teclado"},
            ],
            "respuesta": "monitor",
        },
        {
            "pregunta": "¿Qué dispositivo permite mover el puntero?",
            "opciones": [
                {"valor": "mouse", "etiqueta": "Mouse"},
                {"valor": "monitor", "etiqueta": "Monitor"},
                {"valor": "cpu", "etiqueta": "CPU"},
            ],
            "respuesta": "mouse",
        },
    ],
}


def inicializar_contenido():
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        curso_ids = {}
        for slug, curso in CURSOS.items():
            cursor.execute(
                """
                INSERT INTO cursos (slug, titulo, descripcion)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
                """,
                (slug, curso["titulo"], curso["descripcion"])
            )
            curso_ids[slug] = cursor.lastrowid

        modulo_ids = {}
        contador_por_curso = {}
        for modulo in MODULOS:
            curso_slug = modulo["curso"]
            contador_por_curso[curso_slug] = contador_por_curso.get(curso_slug, 0) + 1
            modulo_slug = f"{curso_slug}-modulo-{contador_por_curso[curso_slug]}"
            curso_id = curso_ids[curso_slug]
            cursor.execute(
                """
                INSERT INTO modulos
                    (curso_id, slug, titulo, descripcion, imagen, orden)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
                """,
                (
                    curso_id,
                    modulo_slug,
                    modulo["titulo"],
                    modulo["descripcion"],
                    modulo["imagen"],
                    contador_por_curso[curso_slug],
                )
            )
            modulo_ids[(curso_id, modulo_slug)] = cursor.lastrowid

            for orden, leccion in enumerate(modulo["lecciones"], start=1):
                actividad = leccion["actividad"]
                opciones = [
                    {"valor": valor, "etiqueta": etiqueta}
                    for valor, etiqueta in actividad["opciones"]
                ]
                cursor.execute(
                    """
                    INSERT IGNORE INTO lecciones
                        (modulo_id, slug, titulo, duracion, introduccion, objetivos,
                         pasos, actividad_pregunta, actividad_opciones,
                         actividad_respuesta, orden)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        modulo_ids[(curso_id, modulo_slug)],
                        leccion["slug"],
                        leccion["titulo"],
                        leccion["duracion"],
                        leccion["introduccion"],
                        json.dumps(leccion["objetivos"], ensure_ascii=False),
                        json.dumps(leccion["pasos"], ensure_ascii=False),
                        actividad["pregunta"],
                        json.dumps(opciones, ensure_ascii=False),
                        actividad["respuesta"],
                        orden,
                    )
                )

        curso_id = curso_ids[EVALUACION_INICIAL["curso"]]
        cursor.execute(
            """
            INSERT INTO evaluaciones (curso_id, slug, titulo, descripcion)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
            """,
            (
                curso_id,
                EVALUACION_INICIAL["slug"],
                EVALUACION_INICIAL["titulo"],
                EVALUACION_INICIAL["descripcion"],
            )
        )
        evaluacion_id = cursor.lastrowid
        for orden, pregunta in enumerate(EVALUACION_INICIAL["preguntas"], start=1):
            cursor.execute(
                """
                SELECT id
                FROM preguntas_evaluacion
                WHERE evaluacion_id = %s AND orden = %s
                """,
                (evaluacion_id, orden)
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    """
                    INSERT INTO preguntas_evaluacion
                        (evaluacion_id, pregunta, opciones, respuesta_correcta, orden)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        evaluacion_id,
                        pregunta["pregunta"],
                        json.dumps(pregunta["opciones"], ensure_ascii=False),
                        pregunta["respuesta"],
                        orden,
                    )
                )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    inicializar_contenido()
    print("Contenido inicial creado sin sobrescribir cambios previos.")
