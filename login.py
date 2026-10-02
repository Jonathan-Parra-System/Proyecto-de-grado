from conexion import conectar_db

conexion = conectar_db()

cursor = conexion.cursor()

# Pedir datos al usuario
usuario = input("Escribe tu usuario: ")
contrasena = input("Escribe tu contraseña: ")

# Consultar la tabla usuarios
sql = """
SELECT * FROM usuarios
WHERE usuario = %s AND contrasena = %s
"""

cursor.execute(sql, (usuario, contrasena))

resultado = cursor.fetchone()

# Comprobar login
if resultado:
    print("Login correcto")
else:
    print("Usuario o contraseña incorrectos")

cursor.close()
conexion.close()