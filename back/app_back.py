from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

import datetime

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


class Mensaje:
    def __init__(self, host, user, password, database):
        # Datos de conexión
        self.conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        # Cursor
        self.cursor = self.conexion.cursor()
        # Intenta ejecutar el uso de la base de datos, sino crea la misma
        try:
            self.cursor.execute(f'USE {database}')
        except mysql.connector.Error as e:
            if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f'CREATE DATABASE {database}')
                self.conexion.database = database
            else:
                raise e

        self.cursor.execute(''' 
                            CREATE TABLE if not EXISTS`patagonia`.`patagonia` (`ID` INT NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(50) NOT NULL , `email` VARCHAR(50) NOT NULL , `telefono` INT(12) NOT NULL , `asunto` VARCHAR(70) NOT NULL , `mensaje` TEXT NOT NULL , `fecha_envio` DATE NOT NULL , `visto` BOOLEAN NOT NULL DEFAULT FALSE , `fecha_visto` DATE NULL DEFAULT NULL , PRIMARY KEY (`ID`)) ENGINE = InnoDB;
                            ''')
        # Confirma los cambios
        self.conexion.commit()

        self.cursor.close()
        self.cursor = self.conexion.cursor(dictionary=True)

    # Cargar los datos
    def enviar_mensaje(self, nombre, email, telefono, asunto, mensaje_usuario):
        query = 'INSERT INTO patagonia(nombre,email,telefono,asunto,mensaje,fecha_envio,visto) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        fecha_envio = datetime.datetime.now()
        visto = False
        valores = (nombre, email, telefono, asunto,
                   mensaje_usuario, fecha_envio, visto)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        return True

    # Traer todos los mensajes

    def cargar_mensajes(self):
        self.cursor.execute('SELECT * from patagonia')
        mensajes = self.cursor.fetchall()
        return mensajes

    # Confirmar que un mensaje fue visto

    def mensaje_visto(self, id):
        fecha_visto = datetime.datetime.now()
        query = 'UPDATE patagonia SET visto = 1, fecha_visto = %s WHERE id = %s'
        valores = (fecha_visto, id)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar_mensaje(self, id):
        self.cursor.execute(f'DELETE FROM patagonia WHERE id = {id}')
        self.conexion.commit()
        return self.cursor.rowcount > 0


mensaje = Mensaje(host='localhost', user='root',
                  password='', database='patagonia')


@app.route('/mensajes', methods=['GET'])
def listar_mensajes():
    respuesta = mensaje.cargar_mensajes()
    return jsonify(respuesta)


@app.route('/mensajes', methods=['POST'])
def agregar_fila_bd():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    asunto = request.form['asunto']
    mensaje_escrito = request.form['mensaje']

    if mensaje.enviar_mensaje(nombre, email, telefono, asunto, mensaje_escrito):
        return jsonify({'mensaje': 'mensaje agregado'}), 201
    else:
        return jsonify({'mensaje': 'No fue posible agregar el mensaje'}), 400


@app.route('/mensajes/<int:id>', methods=['PUT'])
def mensaje_visto(id):
    if mensaje.mensaje_visto(id):
        return jsonify({'mensaje': 'estado del mensaje actualizado.'}), 200
    else:
        return jsonify({'mensaje': 'mensaje no encontrado'}), 403


@app.route('/mensajes/<int:id>', methods=['DELETE'])
def elminar_mensaje(id):
    if mensaje.eliminar_mensaje(id):
        return jsonify({'mensaje': 'mensaje eliminado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'no se encontro el mensaje'}), 404


if __name__ == '__main__':
    app.run(debug=True)
