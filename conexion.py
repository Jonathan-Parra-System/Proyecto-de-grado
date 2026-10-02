import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar_db():
    configuracion = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    faltantes = [nombre for nombre, valor in configuracion.items() if not valor]
    if faltantes:
        raise RuntimeError(
            "Faltan variables de configuraci?n de base de datos: "
            + ", ".join(faltantes)
        )

    certificado_ca = os.getenv("DB_SSL_CA")
    if certificado_ca:
        configuracion.update(
            ssl_ca=certificado_ca,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
        )

    return mysql.connector.connect(**configuracion)


if __name__ == "__main__":
    conexion = conectar_db()
    print("Conexi?n exitosa")
    conexion.close()
