-- Ejecuta una sola vez con root en plataforma_educativa_v2.
-- Conserva cuentas e historiales existentes; las bajas se gestionan con activo=0.
-- Después ejecuta `python inicializar_contenido.py` desde la carpeta del proyecto
-- con el entorno de la aplicación activo, para cargar cursos y evaluación inicial.

USE plataforma_educativa_v2;

ALTER TABLE usuarios
    ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;

ALTER TABLE resultados_evaluaciones
    ADD COLUMN version INT NOT NULL DEFAULT 1;

CREATE TABLE cursos (
    id INT NOT NULL AUTO_INCREMENT,
    slug VARCHAR(80) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_cursos_slug (slug)
) ENGINE=InnoDB;

CREATE TABLE modulos (
    id INT NOT NULL AUTO_INCREMENT,
    curso_id INT NOT NULL,
    slug VARCHAR(120) NOT NULL,
    titulo VARCHAR(180) NOT NULL,
    descripcion TEXT NOT NULL,
    imagen VARCHAR(120) NOT NULL,
    orden INT NOT NULL DEFAULT 0,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_modulos_slug (slug),
    KEY idx_modulos_curso_orden (curso_id, orden),
    CONSTRAINT fk_modulos_curso
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE lecciones (
    id INT NOT NULL AUTO_INCREMENT,
    modulo_id INT NOT NULL,
    slug VARCHAR(120) NOT NULL,
    titulo VARCHAR(180) NOT NULL,
    duracion VARCHAR(30) NOT NULL,
    introduccion TEXT NOT NULL,
    objetivos JSON NOT NULL,
    pasos JSON NOT NULL,
    actividad_pregunta TEXT NOT NULL,
    actividad_opciones JSON NOT NULL,
    actividad_respuesta VARCHAR(80) NOT NULL,
    orden INT NOT NULL DEFAULT 0,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_lecciones_slug (slug),
    KEY idx_lecciones_modulo_orden (modulo_id, orden),
    CONSTRAINT fk_lecciones_modulo
        FOREIGN KEY (modulo_id) REFERENCES modulos(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE evaluaciones (
    id INT NOT NULL AUTO_INCREMENT,
    curso_id INT NULL,
    slug VARCHAR(80) NOT NULL,
    titulo VARCHAR(180) NOT NULL,
    descripcion TEXT NOT NULL,
    version INT NOT NULL DEFAULT 1,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_evaluaciones_slug (slug),
    CONSTRAINT fk_evaluaciones_curso
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE preguntas_evaluacion (
    id INT NOT NULL AUTO_INCREMENT,
    evaluacion_id INT NOT NULL,
    pregunta TEXT NOT NULL,
    opciones JSON NOT NULL,
    respuesta_correcta VARCHAR(80) NOT NULL,
    orden INT NOT NULL DEFAULT 0,
    version INT NOT NULL DEFAULT 1,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    KEY idx_preguntas_evaluacion_orden (evaluacion_id, orden),
    CONSTRAINT fk_preguntas_evaluacion
        FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;
