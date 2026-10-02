-- Ejecuta una sola vez en plataforma_educativa_v2 antes de desplegar
-- el formulario de registro con datos de perfil.
-- Existing accounts keep these fields empty until they are edited.

USE plataforma_educativa_v2;

ALTER TABLE usuarios
    ADD COLUMN email VARCHAR(254) NULL,
    ADD COLUMN celular VARCHAR(16) NULL,
    ADD COLUMN genero VARCHAR(32) NULL,
    ADD COLUMN edad TINYINT UNSIGNED NULL,
    ADD COLUMN fecha_nacimiento DATE NULL,
    ADD UNIQUE KEY uq_usuarios_email (email);
