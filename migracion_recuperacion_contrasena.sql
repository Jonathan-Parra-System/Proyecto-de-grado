-- Ejecuta una sola vez en plataforma_educativa_v2 antes de desplegar
-- la verificación de correo y recuperación de contraseña.
-- Las cuentas existentes conservan email_verificado = NULL y pueden seguir
-- iniciando sesión; las cuentas nuevas deben confirmar su correo.

USE plataforma_educativa_v2;

ALTER TABLE usuarios
    ADD COLUMN email_verificado TINYINT(1) NULL DEFAULT NULL;

CREATE TABLE tokens_seguridad_correo (
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
