from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

# --------------------------------------------------------
# 🔹 CONFIGURACIÓN DE LA BASE DE DATOS
# --------------------------------------------------------
def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",            # Servidor local
            database="formulario",       # Nombre de tu base de datos
            user="postgres",             # Usuario de PostgreSQL
            password="sonic11isaac26"    # Tu contraseña (ajústala si es diferente)
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None


# --------------------------------------------------------
# 🔹 RUTAS DE LA APLICACIÓN
# --------------------------------------------------------

# Página principal con el formulario
@app.route('/')
def formulario():
    return render_template('formulario.html')  # Debe existir en la carpeta "templates"


# Ruta que recibe los datos del formulario
@app.route('/enviar', methods=['POST'])
def enviar():
    # Recibir datos del formulario HTML
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')

    conec = conectar()
    conexion = conec.cursor()
    if conec is None:
        return "No se pudo conectar a la base de datos."

    try:
        conexion.execute(

        """
        INSERT INTO user_info (nombre, apellido, direccion, telefono, correo, mensaje)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (nombre, apellido, direccion, telefono, correo, mensaje)
        )

        conec.commit()
        conec.close()

        return "<h3>Registro exitoso. Los datos se guardaron correctamente.</h3>"
    except Exception as e:
        print(f"Error al insertar: {e}")
        return f"Error al guardar los datos: {e}"


# --------------------------------------------------------
# 🔹 INICIO DEL SERVIDOR
# --------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
