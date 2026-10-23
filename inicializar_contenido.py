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

VERSION_CONTENIDO = "catalogo-pedagogico-ia-v1"


def inicializar_contenido():
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'nombre_completo'")
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE usuarios ADD COLUMN nombre_completo VARCHAR(120) NULL"
            )
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'avatar_id'")
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE usuarios ADD COLUMN avatar_id VARCHAR(32) NULL"
            )
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'foto_perfil'")
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE usuarios ADD COLUMN foto_perfil MEDIUMBLOB NULL"
            )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS migraciones_contenido (
                version VARCHAR(100) NOT NULL PRIMARY KEY,
                aplicada_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
            """
        )
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

        cursor.execute(
            "SELECT version FROM migraciones_contenido WHERE version = %s",
            (VERSION_CONTENIDO,)
        )
        if cursor.fetchone() is None:
            for slug, curso in CURSOS.items():
                cursor.execute(
                    """
                    UPDATE cursos
                    SET titulo = %s, descripcion = %s
                    WHERE slug = %s
                    """,
                    (curso["titulo"], curso["descripcion"], slug)
                )

            contador_por_curso = {}
            for modulo in MODULOS:
                curso_slug = modulo["curso"]
                contador_por_curso[curso_slug] = contador_por_curso.get(curso_slug, 0) + 1
                modulo_slug = f"{curso_slug}-modulo-{contador_por_curso[curso_slug]}"
                cursor.execute(
                    """
                    UPDATE modulos
                    SET titulo = %s, descripcion = %s, imagen = %s
                    WHERE slug = %s
                    """,
                    (
                        modulo["titulo"],
                        modulo["descripcion"],
                        modulo["imagen"],
                        modulo_slug,
                    )
                )

                for orden, leccion in enumerate(modulo["lecciones"], start=1):
                    actividad = leccion["actividad"]
                    opciones = [
                        {"valor": valor, "etiqueta": etiqueta}
                        for valor, etiqueta in actividad["opciones"]
                    ]
                    cursor.execute(
                        """
                        UPDATE lecciones
                        SET titulo = %s, duracion = %s, introduccion = %s,
                            objetivos = %s, pasos = %s,
                            actividad_pregunta = %s, actividad_opciones = %s,
                            actividad_respuesta = %s, orden = %s
                        WHERE slug = %s
                        """,
                        (
                            leccion["titulo"],
                            leccion["duracion"],
                            leccion["introduccion"],
                            json.dumps(leccion["objetivos"], ensure_ascii=False),
                            json.dumps(leccion["pasos"], ensure_ascii=False),
                            actividad["pregunta"],
                            json.dumps(opciones, ensure_ascii=False),
                            actividad["respuesta"],
                            orden,
                            leccion["slug"],
                        )
                    )

            cursor.execute(
                "INSERT INTO migraciones_contenido (version) VALUES (%s)",
                (VERSION_CONTENIDO,)
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
    print("Catálogo inicializado; la actualización pedagógica se aplica una sola vez.")
