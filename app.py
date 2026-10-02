import os
import hmac
import json
import re
import secrets
import unicodedata
from functools import wraps
from pathlib import Path

import mysql.connector
from flask import Flask, abort, flash, render_template, request, session, redirect, url_for
from conexion import conectar_db
from catalogo_db import cargar_catalogo, cargar_evaluaciones
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Falta configurar FLASK_SECRET_KEY en el archivo .env")


def iniciar_sesion_requerida(vista):
    @wraps(vista)
    def vista_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return vista_protegida


def administrador_requerido(vista):
    @wraps(vista)
    def vista_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        rol = _rol_usuario_actual()
        if rol is None:
            session.clear()
            return redirect(url_for("login"))
        if rol != "admin":
            return redirect(url_for("panel") if rol == "estudiante" else url_for("login"))
        session["rol"] = rol
        return vista(*args, **kwargs)
    return vista_protegida


def estudiante_requerido(vista):
    @wraps(vista)
    def vista_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        rol = _rol_usuario_actual()
        if rol is None:
            session.clear()
            return redirect(url_for("login"))
        if rol == "admin":
            session["rol"] = rol
            return redirect(url_for("admin"))
        if rol != "estudiante":
            abort(403)
        session["rol"] = rol
        return vista(*args, **kwargs)
    return vista_protegida


def _rol_usuario_actual():
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "SELECT usuario, rol, activo FROM usuarios WHERE id = %s",
            (session["usuario_id"],)
        )
        resultado = cursor.fetchone()
        if not resultado:
            return None
        usuario, rol, activo = resultado
        if not activo or rol not in {"admin", "estudiante"}:
            return None
        session["usuario"] = usuario
        return rol
    finally:
        cursor.close()
        conexion.close()


def validar_csrf():
    enviado = request.form.get("csrf_token", "")
    guardado = session.get("csrf_token", "")
    if not guardado or not hmac.compare_digest(enviado, guardado):
        abort(400)


def _serializar(valor):
    return json.dumps(valor, ensure_ascii=False)


def _lineas(texto):
    return [linea.strip() for linea in texto.splitlines() if linea.strip()]


def _parsear_opciones(texto):
    opciones = []
    for linea in _lineas(texto):
        partes = linea.split("|", 1)
        if len(partes) != 2 or not all(parte.strip() for parte in partes):
            raise ValueError("Escribe cada opción como valor|texto.")
        if len(partes[0].strip()) > 80:
            raise ValueError("El valor de cada opción debe tener hasta 80 caracteres.")
        opciones.append({
            "valor": partes[0].strip(),
            "etiqueta": partes[1].strip(),
        })
    valores = [opcion["valor"] for opcion in opciones]
    if len(opciones) < 2 or len(set(valores)) != len(valores):
        raise ValueError("Incluye al menos dos opciones con valores únicos.")
    if len(opciones) > 255:
        raise ValueError("Una actividad admite como máximo 255 opciones.")
    return opciones


def _parsear_pasos(texto):
    pasos = []
    for linea in _lineas(texto):
        partes = linea.split("|", 1)
        if len(partes) != 2 or not all(parte.strip() for parte in partes):
            raise ValueError("Escribe cada paso como título|explicación.")
        pasos.append({"titulo": partes[0].strip(), "texto": partes[1].strip()})
    if not pasos:
        raise ValueError("Agrega al menos un paso a la lección.")
    return pasos


def _parsear_preguntas_evaluacion(texto):
    preguntas = []
    for linea in _lineas(texto):
        partes = linea.split("|")
        if len(partes) < 4:
            raise ValueError(
                "Cada línea debe tener pregunta y al menos tres opciones valor:texto."
            )
        pregunta = partes[0].strip()
        if not pregunta:
            raise ValueError("El texto de cada pregunta es obligatorio.")
        opciones = []
        respuestas_correctas = []
        for entrada in partes[1:]:
            valor, separador, etiqueta = entrada.partition(":")
            if not separador or not valor.strip() or not etiqueta.strip():
                raise ValueError("Cada alternativa debe escribirse como valor:texto.")
            etiqueta = etiqueta.strip()
            if etiqueta.endswith("*"):
                respuestas_correctas.append(valor.strip())
                etiqueta = etiqueta[:-1].rstrip()
            if not etiqueta:
                raise ValueError("Cada alternativa debe tener un texto visible.")
            if len(valor.strip()) > 80:
                raise ValueError("El valor de cada alternativa debe tener hasta 80 caracteres.")
            opciones.append({"valor": valor.strip(), "etiqueta": etiqueta})
        valores = [opcion["valor"] for opcion in opciones]
        if len(set(valores)) != len(valores) or len(respuestas_correctas) != 1:
            raise ValueError("Usa valores únicos y marca una sola respuesta correcta con *.")
        preguntas.append({
            "pregunta": pregunta,
            "opciones": opciones,
            "respuesta": respuestas_correctas[0],
        })
    if not preguntas:
        raise ValueError("Agrega al menos una pregunta a la evaluación.")
    if len(preguntas) > 255:
        raise ValueError("Una evaluación admite como máximo 255 preguntas.")
    return preguntas


def _slug_base(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", texto.lower()).strip("-")
    return slug[:110].strip("-") or "contenido"


def _imagenes_disponibles():
    carpeta = Path(app.root_path) / "static" / "images"
    return sorted(
        ruta.name for ruta in carpeta.glob("*.svg")
        if ruta.is_file()
    )


def _obtener_catalogo(incluir_inactivos=False):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    try:
        return cargar_catalogo(cursor, incluir_inactivos=incluir_inactivos)
    finally:
        cursor.close()
        conexion.close()


def _slug_disponible(cursor, tabla, base, excluir_id=None):
    if tabla not in {"cursos", "modulos", "lecciones", "evaluaciones"}:
        raise ValueError("Tipo de contenido no válido.")
    maximo = {"cursos": 80, "modulos": 120, "lecciones": 120, "evaluaciones": 80}[tabla]
    candidato = _slug_base(base)[:maximo].strip("-")
    sufijo = 2
    while True:
        consulta = f"SELECT id FROM {tabla} WHERE slug = %s"
        parametros = [candidato]
        if excluir_id is not None:
            consulta += " AND id <> %s"
            parametros.append(excluir_id)
        cursor.execute(consulta, tuple(parametros))
        if cursor.fetchone() is None:
            return candidato
        candidato = f"{_slug_base(base)[:maximo - len(str(sufijo)) - 1].strip('-')}-{sufijo}"
        sufijo += 1


def obtener_lecciones_completadas(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT leccion_slug
            FROM progreso_lecciones
            WHERE usuario_id = %s AND completada = 1
            """,
            (usuario_id,)
        )
        return {fila[0] for fila in cursor.fetchall()}
    finally:
        cursor.close()
        conexion.close()


@app.context_processor
def incluir_token_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["csrf_token"]}


@app.route('/')
def inicio():
    if "usuario_id" in session:
        rol = _rol_usuario_actual()
        if rol == "admin":
            return redirect(url_for("admin"))
        if rol == "estudiante":
            return redirect(url_for("panel"))
        session.clear()
        return redirect(url_for("login"))
    return render_template('inicio.html')

@app.route('/cursos')
@estudiante_requerido
def cursos():
    return redirect(url_for("panel"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET" and "usuario_id" in session:
        rol = _rol_usuario_actual()
        if rol == "admin":
            return redirect(url_for("admin"))
        if rol == "estudiante":
            return redirect(url_for("panel"))
        session.clear()

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                SELECT id, contrasena, contrasena_hash, rol, activo
                FROM usuarios
                WHERE usuario = %s
                """,
                (usuario,)
            )
            resultado = cursor.fetchone()

            if resultado:
                usuario_id, contrasena_antigua, contrasena_hash, rol, activo = resultado
                es_valida = (
                    check_password_hash(contrasena_hash, contrasena)
                    if contrasena_hash
                    else contrasena_antigua == contrasena
                )
                if es_valida and activo and rol in {"admin", "estudiante"}:
                    if not contrasena_hash:
                        cursor.execute(
                            """
                            UPDATE usuarios
                            SET contrasena_hash = %s, contrasena = NULL
                            WHERE id = %s
                            """,
                            (generate_password_hash(contrasena), usuario_id)
                        )
                    cursor.execute(
                        """
                        UPDATE usuarios
                        SET ultimo_inicio_sesion = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (usuario_id,)
                    )
                    conexion.commit()
                    session.clear()
                    session["usuario_id"] = usuario_id
                    session["usuario"] = usuario
                    session["rol"] = rol
                    return redirect(url_for("admin") if rol == "admin" else url_for("panel"))
        finally:
            cursor.close()
            conexion.close()

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos",
            usuario=usuario
        )

    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not usuario or len(usuario) > 50:
            return render_template(
                "registro.html",
                error="El usuario debe tener entre 1 y 50 caracteres.",
                usuario=usuario
            )
        if len(contrasena) < 8 or len(contrasena) > 128:
            return render_template(
                "registro.html",
                error="La contraseña debe tener entre 8 y 128 caracteres.",
                usuario=usuario
            )

        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (usuario, contrasena_hash)
                VALUES (%s, %s)
                """,
                (usuario, generate_password_hash(contrasena))
            )
            conexion.commit()
        except mysql.connector.IntegrityError as error:
            conexion.rollback()
            if error.errno == 1062:
                return render_template(
                    "registro.html",
                    error="Ese nombre de usuario ya está registrado.",
                    usuario=usuario
                )
            raise
        finally:
            cursor.close()
            conexion.close()

        return redirect(url_for("login", registrado="1"))

    return render_template("registro.html")

@app.route('/panel')
@estudiante_requerido
def panel():
    usuario = session['usuario']
    cursos, _, ordenes = _obtener_catalogo()
    total_lecciones = sum(len(orden) for orden in ordenes.values())
    lecciones_completadas = obtener_lecciones_completadas(session["usuario_id"])
    completadas = len(lecciones_completadas.intersection(
        slug for orden in ordenes.values() for slug in orden
    ))
    porcentaje = int((completadas / total_lecciones) * 100) if total_lecciones else 0

    return render_template(
        'panel.html',
        usuario=usuario,
        lecciones_completadas=completadas,
        total_lecciones=total_lecciones,
        porcentaje=porcentaje,
        cursos=cursos,
    )

@app.route('/progreso')
@estudiante_requerido
def progreso():
    cursos, _, ordenes = _obtener_catalogo()
    lecciones_completadas = obtener_lecciones_completadas(session["usuario_id"])
    todos_slugs = [slug for orden in ordenes.values() for slug in orden]
    total_lecciones = len(todos_slugs)
    completadas = len(lecciones_completadas.intersection(todos_slugs))
    porcentaje = int((completadas / total_lecciones) * 100) if total_lecciones else 0
    progreso_cursos = []
    for curso_slug, curso_actual in cursos.items():
        slugs_curso = ordenes.get(curso_slug, [])
        completadas_curso = len(lecciones_completadas.intersection(slugs_curso))
        total_curso = len(slugs_curso)
        progreso_cursos.append({
            "slug": curso_slug,
            "titulo": curso_actual["titulo"],
            "completadas": completadas_curso,
            "total": total_curso,
            "porcentaje": int((completadas_curso / total_curso) * 100) if total_curso else 0,
        })

    return render_template(
        'progreso.html',
        completadas=completadas,
        total_lecciones=total_lecciones,
        porcentaje=porcentaje,
        progreso_cursos=progreso_cursos
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

@app.route('/curso')
@app.route('/curso/<course_slug>')
@estudiante_requerido
def curso(course_slug='informatica-basica'):
    cursos, _, _ = _obtener_catalogo()
    curso_actual = cursos.get(course_slug)
    if curso_actual is None:
        abort(404)

    return render_template(
        'curso.html',
        curso=curso_actual,
        course_slug=course_slug,
        modulos=curso_actual['modulos'],
        lecciones_completadas=obtener_lecciones_completadas(session["usuario_id"])
    )

@app.route('/leccion/<slug>', methods=['GET', 'POST'])
@estudiante_requerido
def leccion(slug):
    _, lecciones, ordenes_curso = _obtener_catalogo()
    contenido = lecciones.get(slug)
    if contenido is None:
        abort(404)

    resultado_actividad = session.pop("resultado_actividad", None)
    if resultado_actividad and resultado_actividad["slug"] != slug:
        resultado_actividad = None
    usuario_id = session["usuario_id"]
    if request.method == 'POST':
        validar_csrf()
        respuesta = request.form.get('respuesta', '')
        opciones_validas = {
            valor for valor, _ in contenido["actividad"]["opciones"]
        }
        if respuesta not in opciones_validas:
            abort(400)
        es_correcta = respuesta == contenido['actividad']['respuesta']
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            if es_correcta:
                cursor.execute(
                    """
                    INSERT INTO progreso_lecciones
                        (usuario_id, curso_slug, leccion_slug, completada, intentos, ultima_actividad, completada_en)
                    VALUES (%s, %s, %s, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE
                        completada = 1,
                        intentos = intentos + 1,
                        ultima_actividad = CURRENT_TIMESTAMP,
                        completada_en = COALESCE(completada_en, CURRENT_TIMESTAMP)
                    """,
                    (usuario_id, contenido["curso"], slug)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO progreso_lecciones
                        (usuario_id, curso_slug, leccion_slug, completada, intentos, ultima_actividad)
                    VALUES (%s, %s, %s, 0, 1, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE
                        intentos = intentos + 1,
                        ultima_actividad = CURRENT_TIMESTAMP
                    """,
                    (usuario_id, contenido["curso"], slug)
                )
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

        session["resultado_actividad"] = {
            "slug": slug,
            "respuesta": respuesta,
            "correcta": es_correcta,
        }
        return redirect(url_for('leccion', slug=slug))

    lecciones_completadas = obtener_lecciones_completadas(usuario_id)
    orden_curso = ordenes_curso[contenido['curso']]
    indice = orden_curso.index(slug)
    anterior = orden_curso[indice - 1] if indice > 0 else None
    siguiente = orden_curso[indice + 1] if indice < len(orden_curso) - 1 else None
    return render_template(
        'leccion.html',
        leccion=contenido,
        course_slug=contenido['curso'],
        resultado_actividad=resultado_actividad,
        completada=slug in lecciones_completadas,
        anterior=anterior,
        siguiente=siguiente,
        numero=indice + 1,
        total=len(orden_curso)
    )

@app.route('/evaluacion')
@estudiante_requerido
def evaluacion():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    try:
        evaluaciones = cargar_evaluaciones(cursor)
    finally:
        cursor.close()
        conexion.close()
    if not evaluaciones:
        return render_template("evaluaciones.html", evaluaciones=[])
    return render_template("evaluaciones.html", evaluaciones=evaluaciones)


@app.route("/evaluacion/<slug>", methods=["GET", "POST"])
@estudiante_requerido
def evaluacion_detalle(slug):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    try:
        evaluaciones = cargar_evaluaciones(cursor)
        evaluacion_actual = next(
            (item for item in evaluaciones if item["slug"] == slug),
            None
        )
        if evaluacion_actual is None:
            abort(404)

        if request.method == "POST":
            validar_csrf()
            respuestas = {}
            for pregunta in evaluacion_actual["preguntas"]:
                campo = f"pregunta_{pregunta['id']}"
                respuesta = request.form.get(campo)
                valores_validos = {
                    opcion["valor"] for opcion in pregunta["opciones"]
                }
                if respuesta not in valores_validos:
                    abort(400)
                respuestas[pregunta["id"]] = (
                    respuesta == pregunta["respuesta_correcta"]
                )

            puntos = sum(respuestas.values())
            total_preguntas = len(respuestas)
            cursor.execute(
                """
                INSERT INTO resultados_evaluaciones
                    (usuario_id, evaluacion_slug, puntos, total_preguntas, version)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    session["usuario_id"],
                    slug,
                    puntos,
                    total_preguntas,
                    evaluacion_actual["version"],
                )
            )
            conexion.commit()
            return render_template(
                "resultado.html",
                puntos=puntos,
                total_preguntas=total_preguntas,
                evaluacion=evaluacion_actual,
            )
    finally:
        cursor.close()
        conexion.close()

    return render_template("evaluacion.html", evaluacion=evaluacion_actual)


@app.route('/resultado', methods=['POST'])
@estudiante_requerido
def resultado():
    return redirect(url_for("evaluacion"))


@app.route("/admin")
@administrador_requerido
def admin():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                u.id,
                u.usuario,
                u.ultimo_inicio_sesion,
                COUNT(DISTINCT CASE WHEN p.completada = 1 THEN p.leccion_slug END) AS lecciones_completadas,
                COALESCE(SUM(p.intentos), 0) AS intentos_actividad,
                (
                    SELECT e.puntos
                    FROM resultados_evaluaciones e
                    WHERE e.usuario_id = u.id
                    ORDER BY e.creado_en DESC, e.id DESC
                    LIMIT 1
                ) AS ultimo_puntaje,
                (
                    SELECT e.total_preguntas
                    FROM resultados_evaluaciones e
                    WHERE e.usuario_id = u.id
                    ORDER BY e.creado_en DESC, e.id DESC
                    LIMIT 1
                ) AS total_preguntas,
                (
                    SELECT e.creado_en
                    FROM resultados_evaluaciones e
                    WHERE e.usuario_id = u.id
                    ORDER BY e.creado_en DESC, e.id DESC
                    LIMIT 1
                ) AS ultima_evaluacion
            FROM usuarios u
            LEFT JOIN progreso_lecciones p ON p.usuario_id = u.id
            WHERE u.rol = 'estudiante' AND u.activo = 1
            GROUP BY u.id, u.usuario, u.ultimo_inicio_sesion
            ORDER BY u.ultimo_inicio_sesion DESC, u.usuario
            """
        )
        estudiantes = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    estudiantes_activos = sum(
        estudiante["ultimo_inicio_sesion"] is not None
        for estudiante in estudiantes
    )
    lecciones_completadas = sum(
        estudiante["lecciones_completadas"] for estudiante in estudiantes
    )
    puntajes = [
        estudiante["ultimo_puntaje"] / estudiante["total_preguntas"] * 100
        for estudiante in estudiantes
        if estudiante["ultimo_puntaje"] is not None and estudiante["total_preguntas"]
    ]
    promedio_evaluacion = round(sum(puntajes) / len(puntajes)) if puntajes else None

    cursos, _, ordenes = _obtener_catalogo()
    total_lecciones = sum(len(slugs) for slugs in ordenes.values())
    return render_template(
        "admin.html",
        estudiantes=estudiantes,
        total_estudiantes=len(estudiantes),
        estudiantes_activos=estudiantes_activos,
        lecciones_completadas=lecciones_completadas,
        promedio_evaluacion=promedio_evaluacion,
        total_lecciones=total_lecciones,
        cursos=cursos,
    )


@app.route("/admin/estudiante/<int:usuario_id>")
@administrador_requerido
def admin_estudiante(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, usuario, ultimo_inicio_sesion
            FROM usuarios
            WHERE id = %s AND rol = 'estudiante'
            """,
            (usuario_id,)
        )
        estudiante = cursor.fetchone()
        if estudiante is None:
            abort(404)

        cursor.execute(
            """
            SELECT leccion_slug, intentos, completada, ultima_actividad, completada_en
            FROM progreso_lecciones
            WHERE usuario_id = %s
            """,
            (usuario_id,)
        )
        filas_progreso = {
            fila["leccion_slug"]: fila for fila in cursor.fetchall()
        }
        cursor.execute(
            """
            SELECT puntos, total_preguntas, creado_en, evaluacion_slug, version
            FROM resultados_evaluaciones
            WHERE usuario_id = %s
            ORDER BY creado_en DESC, id DESC
            """,
            (usuario_id,)
        )
        resultados = cursor.fetchall()
        for resultado in resultados:
            cursor.execute(
                "SELECT titulo FROM evaluaciones WHERE slug = %s",
                (resultado["evaluacion_slug"],)
            )
            nombre = cursor.fetchone()
            resultado["evaluacion_titulo"] = (
                nombre["titulo"] if nombre else resultado["evaluacion_slug"]
            )
    finally:
        cursor.close()
        conexion.close()

    cursos_catalogo, lecciones_catalogo, ordenes = _obtener_catalogo(incluir_inactivos=True)
    cursos_estudiante = []
    lecciones_estudiante_completadas = 0
    total_intentos = 0
    for curso_slug, curso in cursos_catalogo.items():
        lecciones = []
        for slug in ordenes[curso_slug]:
            progreso_leccion = filas_progreso.get(slug)
            lecciones_estudiante_completadas += bool(
                progreso_leccion and progreso_leccion["completada"]
            )
            if progreso_leccion:
                total_intentos += progreso_leccion["intentos"]
            lecciones.append({
                "titulo": lecciones_catalogo[slug]["titulo"],
                "intentos": progreso_leccion["intentos"] if progreso_leccion else 0,
                "completada": bool(progreso_leccion and progreso_leccion["completada"]),
                "ultima_actividad": progreso_leccion["ultima_actividad"] if progreso_leccion else None,
                "completada_en": progreso_leccion["completada_en"] if progreso_leccion else None,
            })
        cursos_estudiante.append({
            "titulo": curso["titulo"],
            "lecciones": lecciones,
        })

    return render_template(
        "admin_estudiante.html",
        estudiante=estudiante,
        cursos=cursos_estudiante,
        resultados=resultados,
        lecciones_completadas=lecciones_estudiante_completadas,
        total_lecciones=sum(len(slugs) for slugs in ordenes.values()),
        total_intentos=total_intentos,
    )


@app.route("/admin/gestion")
@administrador_requerido
def admin_gestion():
    return render_template("admin_gestion.html")


@app.route("/admin/usuarios", methods=["GET", "POST"])
@administrador_requerido
def admin_usuarios():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    usuario_edicion = None
    try:
        if request.method == "POST":
            validar_csrf()
            accion = request.form.get("accion")
            usuario_id = request.form.get("usuario_id", type=int)

            if accion in {"archivar", "restaurar"}:
                if usuario_id == session["usuario_id"]:
                    flash("No puedes desactivar tu propia cuenta de administración.", "error")
                else:
                    cursor.execute(
                        "SELECT rol, activo FROM usuarios WHERE id = %s",
                        (usuario_id,)
                    )
                    objetivo = cursor.fetchone()
                    if objetivo is None:
                        abort(404)
                    activo = 0 if accion == "archivar" else 1
                    if objetivo["rol"] == "admin" and objetivo["activo"] and not activo:
                        cursor.execute(
                            "SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin' AND activo = 1"
                        )
                        if cursor.fetchone()["total"] <= 1:
                            flash("Debe permanecer al menos una cuenta administradora activa.", "error")
                        else:
                            cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = %s", (usuario_id,))
                            conexion.commit()
                            flash("Cuenta administrativa archivada.", "success")
                    else:
                        cursor.execute("UPDATE usuarios SET activo = %s WHERE id = %s", (activo, usuario_id))
                        conexion.commit()
                        flash("Estado de la cuenta actualizado.", "success")
                return redirect(url_for("admin_usuarios"))

            nombre = request.form.get("usuario", "").strip()
            rol = request.form.get("rol", "")
            activo = request.form.get("activo") == "1"
            contrasena = request.form.get("contrasena", "")
            if not nombre or len(nombre) > 50 or rol not in {"estudiante", "admin"}:
                flash("Ingresa un usuario de hasta 50 caracteres y un rol válido.", "error")
            elif contrasena and not 8 <= len(contrasena) <= 128:
                flash("La contraseña debe tener entre 8 y 128 caracteres.", "error")
            elif accion == "crear" and not contrasena:
                flash("Para crear la cuenta debes indicar una contraseña de al menos 8 caracteres.", "error")
            else:
                if usuario_id:
                    cursor.execute("SELECT rol, activo FROM usuarios WHERE id = %s", (usuario_id,))
                    anterior = cursor.fetchone()
                    if anterior is None:
                        abort(404)
                    if usuario_id == session["usuario_id"] and (
                        rol != "admin" or not activo
                    ):
                        flash("No puedes cambiar tu propia cuenta para quitarte el acceso administrativo.", "error")
                    elif (
                        anterior["rol"] == "admin"
                        and anterior["activo"]
                        and (rol != "admin" or not activo)
                    ):
                        cursor.execute(
                            "SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin' AND activo = 1"
                        )
                        if cursor.fetchone()["total"] <= 1:
                            flash("Debe permanecer al menos una cuenta administradora activa.", "error")
                        else:
                            _guardar_usuario(cursor, conexion, usuario_id, nombre, rol, activo, contrasena)
                    else:
                        _guardar_usuario(cursor, conexion, usuario_id, nombre, rol, activo, contrasena)
                else:
                    cursor.execute(
                        """
                        INSERT INTO usuarios (usuario, contrasena_hash, rol, activo)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nombre, generate_password_hash(contrasena), rol, int(activo))
                    )
                    conexion.commit()
                return redirect(url_for("admin_usuarios"))

        editar_id = request.args.get("editar", type=int)
        if editar_id:
            cursor.execute(
                "SELECT id, usuario, rol, activo FROM usuarios WHERE id = %s",
                (editar_id,)
            )
            usuario_edicion = cursor.fetchone()
            if usuario_edicion is None:
                abort(404)
        cursor.execute(
            """
            SELECT id, usuario, rol, activo, ultimo_inicio_sesion
            FROM usuarios
            ORDER BY activo DESC, rol, usuario
            """
        )
        usuarios = cursor.fetchall()
    except mysql.connector.IntegrityError as error:
        conexion.rollback()
        if error.errno == 1062:
            flash("Ese nombre de usuario ya está en uso.", "error")
            cursor.execute(
                """
                SELECT id, usuario, rol, activo, ultimo_inicio_sesion
                FROM usuarios
                ORDER BY activo DESC, rol, usuario
                """
            )
            usuarios = cursor.fetchall()
        else:
            raise
    finally:
        cursor.close()
        conexion.close()
    return render_template(
        "admin_usuarios.html",
        usuarios=usuarios,
        usuario_edicion=usuario_edicion,
    )


def _guardar_usuario(cursor, conexion, usuario_id, nombre, rol, activo, contrasena):
    if contrasena:
        cursor.execute(
            """
            UPDATE usuarios
            SET usuario = %s, rol = %s, activo = %s, contrasena_hash = %s,
                contrasena = NULL
            WHERE id = %s
            """,
            (nombre, rol, int(activo), generate_password_hash(contrasena), usuario_id)
        )
    else:
        cursor.execute(
            """
            UPDATE usuarios
            SET usuario = %s, rol = %s, activo = %s
            WHERE id = %s
            """,
            (nombre, rol, int(activo), usuario_id)
        )
    conexion.commit()


@app.route("/admin/cursos", methods=["GET", "POST"])
@administrador_requerido
def admin_cursos():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    curso_edicion = None
    try:
        if request.method == "POST":
            validar_csrf()
            accion = request.form.get("accion")
            curso_id = request.form.get("curso_id", type=int)
            if accion in {"archivar", "restaurar"}:
                cursor.execute(
                    "UPDATE cursos SET activo = %s WHERE id = %s",
                    (0 if accion == "archivar" else 1, curso_id)
                )
                if cursor.rowcount == 0:
                    abort(404)
                conexion.commit()
                flash("Estado del curso actualizado.", "success")
                return redirect(url_for("admin_cursos"))
            titulo = request.form.get("titulo", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            if not titulo or len(titulo) > 150 or not descripcion:
                flash("Completa un título de hasta 150 caracteres y una descripción.", "error")
            elif curso_id:
                cursor.execute(
                    "UPDATE cursos SET titulo = %s, descripcion = %s WHERE id = %s",
                    (titulo, descripcion, curso_id)
                )
                conexion.commit()
                flash("Curso actualizado.", "success")
                return redirect(url_for("admin_cursos"))
            else:
                slug = _slug_disponible(cursor, "cursos", titulo)
                cursor.execute(
                    "INSERT INTO cursos (slug, titulo, descripcion) VALUES (%s, %s, %s)",
                    (slug, titulo, descripcion)
                )
                conexion.commit()
                flash("Curso creado.", "success")
                return redirect(url_for("admin_cursos"))

        if request.args.get("editar", type=int):
            cursor.execute("SELECT * FROM cursos WHERE id = %s", (request.args.get("editar", type=int),))
            curso_edicion = cursor.fetchone()
            if curso_edicion is None:
                abort(404)
        cursor.execute(
            """
            SELECT c.id, c.slug, c.titulo, c.descripcion, c.activo,
                   COUNT(m.id) AS total_modulos
            FROM cursos c
            LEFT JOIN modulos m ON m.curso_id = c.id
            GROUP BY c.id, c.slug, c.titulo, c.descripcion, c.activo
            ORDER BY c.id
            """
        )
        cursos = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
    return render_template("admin_cursos.html", cursos=cursos, curso_edicion=curso_edicion)


@app.route("/admin/modulos", methods=["GET", "POST"])
@administrador_requerido
def admin_modulos():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    modulo_edicion = None
    try:
        cursor.execute("SELECT id, slug, titulo, activo FROM cursos ORDER BY id")
        cursos = cursor.fetchall()
        if request.method == "POST":
            validar_csrf()
            accion = request.form.get("accion")
            modulo_id = request.form.get("modulo_id", type=int)
            if accion in {"archivar", "restaurar"}:
                cursor.execute(
                    "UPDATE modulos SET activo = %s WHERE id = %s",
                    (0 if accion == "archivar" else 1, modulo_id)
                )
                if cursor.rowcount == 0:
                    abort(404)
                conexion.commit()
                flash("Estado del módulo actualizado.", "success")
                return redirect(url_for("admin_modulos"))
            curso_id = request.form.get("curso_id", type=int)
            titulo = request.form.get("titulo", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            imagen = request.form.get("imagen", "")
            orden = request.form.get("orden", type=int) or 0
            if not any(c["id"] == curso_id and c["activo"] for c in cursos):
                flash("Selecciona un curso activo.", "error")
            elif not titulo or len(titulo) > 180 or not descripcion or imagen not in _imagenes_disponibles():
                flash("Completa el título, la descripción y una ilustración disponible.", "error")
            elif orden < 0:
                flash("El orden no puede ser negativo.", "error")
            elif modulo_id:
                cursor.execute(
                    """
                    UPDATE modulos
                    SET curso_id = %s, titulo = %s, descripcion = %s, imagen = %s, orden = %s
                    WHERE id = %s
                    """,
                    (curso_id, titulo, descripcion, imagen, orden, modulo_id)
                )
                conexion.commit()
                flash("Módulo actualizado.", "success")
                return redirect(url_for("admin_modulos"))
            else:
                curso_slug = next(c["slug"] for c in cursos if c["id"] == curso_id)
                slug = _slug_disponible(cursor, "modulos", f"{curso_slug}-{titulo}")
                cursor.execute(
                    """
                    INSERT INTO modulos (curso_id, slug, titulo, descripcion, imagen, orden)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (curso_id, slug, titulo, descripcion, imagen, orden)
                )
                conexion.commit()
                flash("Módulo creado.", "success")
                return redirect(url_for("admin_modulos"))

        modulo_id = request.args.get("editar", type=int)
        if modulo_id:
            cursor.execute("SELECT * FROM modulos WHERE id = %s", (modulo_id,))
            modulo_edicion = cursor.fetchone()
            if modulo_edicion is None:
                abort(404)
        cursor.execute(
            """
            SELECT m.id, m.slug, m.titulo, m.descripcion, m.imagen, m.orden,
                   m.activo, m.curso_id, c.titulo AS curso_titulo,
                   COUNT(l.id) AS total_lecciones
            FROM modulos m JOIN cursos c ON c.id = m.curso_id
            LEFT JOIN lecciones l ON l.modulo_id = m.id
            GROUP BY m.id, m.slug, m.titulo, m.descripcion, m.imagen,
                     m.orden, m.activo, m.curso_id, c.titulo
            ORDER BY c.id, m.orden, m.id
            """
        )
        modulos = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
    return render_template(
        "admin_modulos.html",
        cursos=cursos,
        modulos=modulos,
        modulo_edicion=modulo_edicion,
        imagenes=_imagenes_disponibles(),
    )


@app.route("/admin/lecciones", methods=["GET", "POST"])
@administrador_requerido
def admin_lecciones():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    leccion_edicion = None
    try:
        cursor.execute(
            """
            SELECT m.id, m.titulo, m.activo, c.titulo AS curso_titulo, c.activo AS curso_activo
            FROM modulos m JOIN cursos c ON c.id = m.curso_id
            ORDER BY c.id, m.orden, m.id
            """
        )
        modulos = cursor.fetchall()
        if request.method == "POST":
            validar_csrf()
            accion = request.form.get("accion")
            leccion_id = request.form.get("leccion_id", type=int)
            if accion in {"archivar", "restaurar"}:
                cursor.execute(
                    "UPDATE lecciones SET activo = %s WHERE id = %s",
                    (0 if accion == "archivar" else 1, leccion_id)
                )
                if cursor.rowcount == 0:
                    abort(404)
                conexion.commit()
                flash("Estado de la lección actualizado.", "success")
                return redirect(url_for("admin_lecciones"))

            modulo_id = request.form.get("modulo_id", type=int)
            titulo = request.form.get("titulo", "").strip()
            duracion = request.form.get("duracion", "").strip()
            introduccion = request.form.get("introduccion", "").strip()
            objetivos = _lineas(request.form.get("objetivos", ""))
            pregunta = request.form.get("actividad_pregunta", "").strip()
            respuesta = request.form.get("actividad_respuesta", "").strip()
            try:
                pasos = _parsear_pasos(request.form.get("pasos", ""))
                opciones = _parsear_opciones(request.form.get("opciones", ""))
            except ValueError as error:
                flash(str(error), "error")
            else:
                modulo_valido = any(
                    m["id"] == modulo_id and m["activo"] and m["curso_activo"]
                    for m in modulos
                )
                if (
                    not modulo_valido or not titulo or len(titulo) > 180
                    or not duracion or len(duracion) > 30 or not introduccion or not objetivos
                    or not pregunta or respuesta not in {op["valor"] for op in opciones}
                ):
                    flash("Completa los campos obligatorios y selecciona un módulo activo.", "error")
                elif leccion_id:
                    cursor.execute(
                        """
                        UPDATE lecciones
                        SET modulo_id = %s, titulo = %s, duracion = %s, introduccion = %s,
                            objetivos = %s, pasos = %s, actividad_pregunta = %s,
                            actividad_opciones = %s, actividad_respuesta = %s
                        WHERE id = %s
                        """,
                        (
                            modulo_id, titulo, duracion, introduccion, _serializar(objetivos),
                            _serializar(pasos), pregunta, _serializar(opciones), respuesta, leccion_id
                        )
                    )
                    conexion.commit()
                    flash("Lección actualizada.", "success")
                    return redirect(url_for("admin_lecciones"))
                else:
                    slug = _slug_disponible(cursor, "lecciones", titulo)
                    cursor.execute(
                        "SELECT COALESCE(MAX(orden), 0) + 1 AS siguiente FROM lecciones WHERE modulo_id = %s",
                        (modulo_id,)
                    )
                    orden = cursor.fetchone()["siguiente"]
                    cursor.execute(
                        """
                        INSERT INTO lecciones
                            (modulo_id, slug, titulo, duracion, introduccion, objetivos,
                             pasos, actividad_pregunta, actividad_opciones,
                             actividad_respuesta, orden)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            modulo_id, slug, titulo, duracion, introduccion,
                            _serializar(objetivos), _serializar(pasos), pregunta,
                            _serializar(opciones), respuesta, orden
                        )
                    )
                    conexion.commit()
                    flash("Lección creada.", "success")
                    return redirect(url_for("admin_lecciones"))

        leccion_id = request.args.get("editar", type=int)
        if leccion_id:
            cursor.execute(
                """
                SELECT l.*, m.titulo AS modulo_titulo, m.curso_id
                FROM lecciones l JOIN modulos m ON m.id = l.modulo_id
                WHERE l.id = %s
                """,
                (leccion_id,)
            )
            leccion_edicion = cursor.fetchone()
            if leccion_edicion is None:
                abort(404)
            leccion_edicion["objetivos"] = json.loads(leccion_edicion["objetivos"])
            leccion_edicion["pasos"] = json.loads(leccion_edicion["pasos"])
            leccion_edicion["actividad_opciones"] = json.loads(leccion_edicion["actividad_opciones"])
        cursor.execute(
            """
            SELECT l.id, l.slug, l.titulo, l.duracion, l.activo, m.titulo AS modulo_titulo,
                   c.titulo AS curso_titulo
            FROM lecciones l
            JOIN modulos m ON m.id = l.modulo_id
            JOIN cursos c ON c.id = m.curso_id
            ORDER BY c.id, m.orden, l.orden, l.id
            """
        )
        lecciones = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
    return render_template(
        "admin_lecciones.html",
        modulos=modulos,
        lecciones=lecciones,
        leccion_edicion=leccion_edicion,
    )


@app.route("/admin/evaluaciones", methods=["GET", "POST"])
@administrador_requerido
def admin_evaluaciones():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    evaluacion_edicion = None
    try:
        cursor.execute("SELECT id, slug, titulo FROM cursos WHERE activo = 1 ORDER BY id")
        cursos = cursor.fetchall()
        if request.method == "POST":
            validar_csrf()
            accion = request.form.get("accion")
            evaluacion_id = request.form.get("evaluacion_id", type=int)
            if accion in {"archivar", "restaurar"}:
                cursor.execute(
                    "UPDATE evaluaciones SET activo = %s WHERE id = %s",
                    (0 if accion == "archivar" else 1, evaluacion_id)
                )
                if cursor.rowcount == 0:
                    abort(404)
                conexion.commit()
                flash("Estado de la evaluación actualizado.", "success")
                return redirect(url_for("admin_evaluaciones"))
            titulo = request.form.get("titulo", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            curso_id = request.form.get("curso_id", type=int)
            curso_id = curso_id or None
            try:
                preguntas = _parsear_preguntas_evaluacion(request.form.get("preguntas", ""))
            except ValueError as error:
                flash(str(error), "error")
            else:
                if not titulo or len(titulo) > 180 or not descripcion:
                    flash("Completa el título y la descripción de la evaluación.", "error")
                elif curso_id and not any(c["id"] == curso_id for c in cursos):
                    flash("Selecciona un curso activo o una evaluación general.", "error")
                elif evaluacion_id:
                    cursor.execute(
                        """
                        UPDATE evaluaciones
                        SET titulo = %s, descripcion = %s, curso_id = %s, version = version + 1
                        WHERE id = %s
                        """,
                        (titulo, descripcion, curso_id, evaluacion_id)
                    )
                    cursor.execute(
                        "SELECT version FROM evaluaciones WHERE id = %s",
                        (evaluacion_id,)
                    )
                    version = cursor.fetchone()["version"]
                    cursor.execute(
                        "UPDATE preguntas_evaluacion SET activo = 0 WHERE evaluacion_id = %s",
                        (evaluacion_id,)
                    )
                    for orden, pregunta in enumerate(preguntas, start=1):
                        cursor.execute(
                            """
                            INSERT INTO preguntas_evaluacion
                                (evaluacion_id, pregunta, opciones, respuesta_correcta, orden, version, activo)
                            VALUES (%s, %s, %s, %s, %s, %s, 1)
                            """,
                            (
                                evaluacion_id, pregunta["pregunta"], _serializar(pregunta["opciones"]),
                                pregunta["respuesta"], orden, version
                            )
                        )
                    conexion.commit()
                    flash("Evaluación actualizada. Las preguntas anteriores quedan archivadas.", "success")
                    return redirect(url_for("admin_evaluaciones"))
                else:
                    slug = _slug_disponible(cursor, "evaluaciones", titulo)
                    cursor.execute(
                        """
                        INSERT INTO evaluaciones (curso_id, slug, titulo, descripcion)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (curso_id, slug, titulo, descripcion)
                    )
                    nuevo_id = cursor.lastrowid
                    for orden, pregunta in enumerate(preguntas, start=1):
                        cursor.execute(
                            """
                            INSERT INTO preguntas_evaluacion
                                (evaluacion_id, pregunta, opciones, respuesta_correcta, orden, version, activo)
                            VALUES (%s, %s, %s, %s, %s, 1, 1)
                            """,
                            (
                                nuevo_id, pregunta["pregunta"], _serializar(pregunta["opciones"]),
                                pregunta["respuesta"], orden
                            )
                        )
                    conexion.commit()
                    flash("Evaluación creada.", "success")
                    return redirect(url_for("admin_evaluaciones"))

        evaluacion_id = request.args.get("editar", type=int)
        if evaluacion_id:
            cursor.execute("SELECT * FROM evaluaciones WHERE id = %s", (evaluacion_id,))
            evaluacion_edicion = cursor.fetchone()
            if evaluacion_edicion is None:
                abort(404)
            cursor.execute(
                """
                SELECT pregunta, opciones, respuesta_correcta
                FROM preguntas_evaluacion
                WHERE evaluacion_id = %s AND activo = 1
                ORDER BY orden, id
                """,
                (evaluacion_id,)
            )
            evaluacion_edicion["preguntas"] = cursor.fetchall()
            for pregunta in evaluacion_edicion["preguntas"]:
                pregunta["opciones"] = json.loads(pregunta["opciones"])
        evaluaciones = cargar_evaluaciones(cursor, incluir_inactivas=True)
    finally:
        cursor.close()
        conexion.close()
    return render_template(
        "admin_evaluaciones.html",
        cursos=cursos,
        evaluaciones=evaluaciones,
        evaluacion_edicion=evaluacion_edicion,
    )


if __name__ == '__main__':
    app.run(debug=True)
    
    
    #python app.py