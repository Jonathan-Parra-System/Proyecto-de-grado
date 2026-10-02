-- Inicialización de una base nueva para la plataforma.
-- Ejecutar con una cuenta administradora de MySQL (por ejemplo, root).
-- No elimina ni modifica la base plataforma_educativa existente.
-- Para habilitar la gestión de contenido, luego ejecuta una sola vez
-- migracion_gestion_administrativa.sql y `python inicializar_contenido.py`.

CREATE DATABASE IF NOT EXISTS plataforma_educativa_v2
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE plataforma_educativa_v2;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(255) NULL,
    contrasena_hash VARCHAR(255) NULL,
    email VARCHAR(254) NULL,
    celular VARCHAR(16) NULL,
    genero VARCHAR(32) NULL,
    edad TINYINT UNSIGNED NULL,
    fecha_nacimiento DATE NULL,
    email_verificado TINYINT(1) NULL DEFAULT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'estudiante',
    ultimo_inicio_sesion DATETIME NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_usuario (usuario),
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tokens_seguridad_correo (
    id BIGINT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    proposito VARCHAR(20) NOT NULL,
    token_hash CHAR(64) NOT NULL,
    expira_en DATETIME NOT NULL,
    usado_en DATETIME NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_tokens_seguridad_hash (token_hash),
    KEY idx_tokens_seguridad_usuario (usuario_id, proposito, usado_en),
    CONSTRAINT fk_tokens_seguridad_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS solicitudes_seguridad_correo (
    id BIGINT NOT NULL AUTO_INCREMENT,
    ip_hash CHAR(64) NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_solicitudes_correo_ip_fecha (ip_hash, creado_en),
    KEY idx_solicitudes_correo_fecha (creado_en)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS progreso_lecciones (
    usuario_id INT NOT NULL,
    curso_slug VARCHAR(60) NOT NULL,
    leccion_slug VARCHAR(100) NOT NULL,
    completada TINYINT(1) NOT NULL DEFAULT 0,
    intentos INT NOT NULL DEFAULT 0,
    ultima_actividad DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    completada_en DATETIME NULL,
    PRIMARY KEY (usuario_id, leccion_slug),
    KEY idx_progreso_curso (curso_slug),
    CONSTRAINT fk_progreso_lecciones_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS resultados_evaluaciones (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    evaluacion_slug VARCHAR(60) NOT NULL,
    puntos TINYINT UNSIGNED NOT NULL,
    total_preguntas TINYINT UNSIGNED NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_resultados_usuario_fecha (usuario_id, creado_en),
    CONSTRAINT fk_resultados_evaluaciones_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
