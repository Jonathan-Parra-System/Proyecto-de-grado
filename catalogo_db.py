import json


def cargar_catalogo(cursor, incluir_inactivos=False):
    filtro_curso = "" if incluir_inactivos else "WHERE activo = 1"
    cursor.execute(
        f"""
        SELECT id, slug, titulo, descripcion, activo
        FROM cursos
        {filtro_curso}
        ORDER BY id
        """
    )
    cursos = {}
    for fila in cursor.fetchall():
        curso = dict(fila)
        curso["modulos"] = []
        cursos[curso["slug"]] = curso

    if not cursos:
        return cursos, {}, {}

    curso_ids = [curso["id"] for curso in cursos.values()]
    placeholders = ", ".join(["%s"] * len(curso_ids))
    filtro_modulo = "" if incluir_inactivos else "AND m.activo = 1 AND c.activo = 1"
    cursor.execute(
        f"""
        SELECT
            m.id, m.curso_id, m.slug, m.titulo, m.descripcion, m.imagen,
            m.orden, m.activo
        FROM modulos m
        JOIN cursos c ON c.id = m.curso_id
        WHERE m.curso_id IN ({placeholders}) {filtro_modulo}
        ORDER BY m.curso_id, m.orden, m.id
        """,
        tuple(curso_ids)
    )
    modulos_por_id = {}
    for fila in cursor.fetchall():
        modulo = dict(fila)
        modulo["lecciones"] = []
        curso = next(
            curso for curso in cursos.values()
            if curso["id"] == modulo["curso_id"]
        )
        curso["modulos"].append(modulo)
        modulos_por_id[modulo["id"]] = modulo

    if not modulos_por_id:
        return cursos, {}, {slug: [] for slug in cursos}

    modulo_ids = list(modulos_por_id)
    placeholders = ", ".join(["%s"] * len(modulo_ids))
    filtro_leccion = "" if incluir_inactivos else "AND l.activo = 1 AND m.activo = 1 AND c.activo = 1"
    cursor.execute(
        f"""
        SELECT
            l.id, l.modulo_id, l.slug, l.titulo, l.duracion, l.introduccion,
            l.objetivos, l.pasos, l.actividad_pregunta, l.actividad_opciones,
            l.actividad_respuesta, l.orden, l.activo,
            m.titulo AS modulo_titulo, m.imagen,
            c.slug AS curso_slug, c.titulo AS curso_titulo
        FROM lecciones l
        JOIN modulos m ON m.id = l.modulo_id
        JOIN cursos c ON c.id = m.curso_id
        WHERE l.modulo_id IN ({placeholders}) {filtro_leccion}
        ORDER BY l.modulo_id, l.orden, l.id
        """,
        tuple(modulo_ids)
    )
    lecciones = {}
    ordenes = {slug: [] for slug in cursos}
    for fila in cursor.fetchall():
        leccion = dict(fila)
        leccion["objetivos"] = _leer_json(leccion["objetivos"])
        leccion["pasos"] = _leer_json(leccion["pasos"])
        leccion["actividad"] = {
            "pregunta": leccion.pop("actividad_pregunta"),
            "opciones": [
                (opcion["valor"], opcion["etiqueta"])
                for opcion in _leer_json(leccion.pop("actividad_opciones"))
            ],
            "respuesta": leccion.pop("actividad_respuesta"),
        }
        leccion["curso"] = leccion.pop("curso_slug")
        leccion["modulo"] = leccion.pop("modulo_titulo")
        leccion["curso_titulo"] = leccion.pop("curso_titulo")
        modulo = modulos_por_id[leccion["modulo_id"]]
        modulo["lecciones"].append(leccion)
        lecciones[leccion["slug"]] = leccion
        ordenes[leccion["curso"]].append(leccion["slug"])

    return cursos, lecciones, ordenes


def cargar_evaluaciones(cursor, curso_slug=None, incluir_inactivas=False):
    filtros = []
    parametros = []
    if not incluir_inactivas:
        filtros.append("e.activo = 1")
        filtros.append("(e.curso_id IS NULL OR c.activo = 1)")
    if curso_slug:
        filtros.append("(c.slug = %s OR e.curso_id IS NULL)")
        parametros.append(curso_slug)
    where = f"WHERE {' AND '.join(filtros)}" if filtros else ""
    cursor.execute(
        f"""
        SELECT e.id, e.slug, e.titulo, e.descripcion, e.version, e.activo,
               c.slug AS curso_slug, c.titulo AS curso_titulo
        FROM evaluaciones e
        LEFT JOIN cursos c ON c.id = e.curso_id
        {where}
        ORDER BY e.id
        """,
        tuple(parametros)
    )
    evaluaciones = [dict(fila) for fila in cursor.fetchall()]
    if not evaluaciones:
        return []

    ids = [evaluacion["id"] for evaluacion in evaluaciones]
    placeholders = ", ".join(["%s"] * len(ids))
    cursor.execute(
        f"""
        SELECT id, evaluacion_id, pregunta, opciones, respuesta_correcta, orden
        FROM preguntas_evaluacion
        WHERE evaluacion_id IN ({placeholders}) AND activo = 1
        ORDER BY evaluacion_id, orden, id
        """,
        tuple(ids)
    )
    preguntas = {}
    for fila in cursor.fetchall():
        pregunta = dict(fila)
        pregunta["opciones"] = _leer_json(pregunta["opciones"])
        preguntas.setdefault(pregunta["evaluacion_id"], []).append(pregunta)
    for evaluacion in evaluaciones:
        evaluacion["preguntas"] = preguntas.get(evaluacion["id"], [])
    if not incluir_inactivas:
        evaluaciones = [
            evaluacion for evaluacion in evaluaciones
            if evaluacion["preguntas"]
        ]
    return evaluaciones


def _leer_json(valor):
    if isinstance(valor, (dict, list)):
        return valor
    return json.loads(valor)
