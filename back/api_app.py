#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS


# Instalar con pip install mysql-connector-python
import mysql.connector

# No es necesario instalar, es parte del sistema standard de Python
import os
import time, datetime
#--------------------------------------------------------------------


app = Flask(__name__)

# Permitir acceso desde cualquier origen externo
CORS(app, resources={r"/*": {"origins": "*"}}) 

class Mensaje:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE if not EXISTS patagonia (`ID` INT NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(50) NOT NULL , `email` VARCHAR(50) NOT NULL , `telefono` INT(12) NOT NULL , `asunto` VARCHAR(70) NOT NULL , `mensaje` TEXT NOT NULL , `fecha_envio` DATE NOT NULL , `visto` BOOLEAN NOT NULL DEFAULT FALSE , `fecha_visto` DATE NULL DEFAULT NULL, gestion varchar(500) DEFAULT NULL, PRIMARY KEY (`ID`)) ENGINE = InnoDB;
            ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def enviar_mensaje(self, nombre, email, telefono, asunto, mensaje_usuario):
        sql = "INSERT INTO patagonia(nombre, email, telefono, asunto, mensaje, fecha_envio) VALUES (%s, %s, %s, %s, %s, %s)"
        fecha_envio = datetime.datetime.now()
        valores = (nombre, email, telefono, asunto, mensaje_usuario, fecha_envio)
        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def listar_mensajes(self):
        self.cursor.execute("SELECT * FROM patagonia")
        mensajes = self.cursor.fetchall()
        return mensajes

    #----------------------------------------------------------------
    def responder_mensaje(self, id, gestion):
        fecha_gestion = datetime.datetime.now()
        sql = "UPDATE patagonia SET visto = 1, fecha_visto = %s, gestion = %s WHERE id = %s"
        valores = (fecha_gestion, gestion, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def eliminar_mensaje(self, id):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM patagonia WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_mensaje(self, id):
         sql = f"SELECT id, nombre, apellido, telefono, email, mensaje, fecha_envio, leido, gestion, fecha_gestion FROM patagonia WHERE id = {id}"
         self.cursor.execute(sql)
         return self.cursor.fetchone()


# Creamos el objeto
mensaje = Mensaje(host='NahueOli.mysql.pythonanywhere-services.com', user='NahueOli', password='sqlbaseOli1605', database='NahueOli$patagoniaPython')



#--------------------------------------------------------------------
@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    respuesta = mensaje.listar_mensajes()
    return jsonify(respuesta)


#--------------------------------------------------------------------
@app.route("/mensajes", methods=["POST"])
def agregar_fila_bd():
    #Recojo los datos del form
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    asunto = request.form['asunto']
    mensaje_escrito = request.form['mensaje']  

    if mensaje.enviar_mensaje(nombre, email, telefono, asunto, mensaje_escrito):
        return jsonify({"mensaje": "Mensaje agregado"}), 201
    else:
        return jsonify({"mensaje": "No fue posible registrar el mensaje"}), 400
  

#--------------------------------------------------------------------
@app.route("/mensajes/<int:id>", methods=["PUT"])
def responder_mensaje(id):
    #Recojo los datos del form
    gestion = request.form.get("gestion")
    
    if mensaje.responder_mensaje(id, gestion):
        return jsonify({"mensaje": "Mensaje modificado"}), 200
    else:
        return jsonify({"mensaje": "Mensaje no encontrado"}), 403


#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)



