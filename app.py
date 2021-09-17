from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
    'Server=DESKTOP-0DSCFJO\SQLEXPRESS;'
    'Database=anotherdatabase;'
    'Trusted_Connection=yes;')

cursor = conn.cursor()

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
def frontpage():
    return('Bienvenidos')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        cursor.execute("SELECT * FROM Usuarios")
        for usuario in cursor:
            print(usuario)
        user = request.json['user']
        contraseña = request.json['password']
        cursor.execute("SELECT * FROM Usuarios WHERE Usuario = " + f"'{user}'")
        for usuario in cursor:
            if usuario[2] == user:
                if usuario[3] == contraseña:
                    objeto = {
                        'mensaje': 'Sesión iniciada con éxito',
                        'nombre': usuario[0],
                        'apellido': usuario[1],
                        'usuario': usuario[2],
                        'exist': True
                    }
                    return(jsonify(objeto))
                else:
                    objeto = {
                        'mensaje': 'Contraseña incorrecta',
                        'exist': False
                    }
                    return(jsonify(objeto))
            else:
                objeto = {
                    'mensaje':'Usuario incorrecto',
                    'exist': False
                }
                return(jsonify(objeto))
        objeto = {
            'mensaje': 'Este usuario no existe',
            'exist': False
        }
        return(jsonify(objeto))

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        nombre = request.json['name']
        apellido = request.json['lastname']
        carnet = int(request.json['carnet'])
        user = request.json['user']
        contraseña = request.json['password']
        try:
            cursor.execute(f"""INSERT INTO Usuarios (Nombre, Apellido, Usuario, Contraseña, Carné) values('{nombre}','{apellido}','{user}','{contraseña}', {carnet})""")
            conn.commit()
            objeto = {
                'mensaje':'Usuario ingresado exitosamente'
            }
            
            return(jsonify(objeto))
        except:
            objeto = {
                'mensaje': 'El usuario ya existe en la base de datos'
            }
            return(jsonify(objeto))
                


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)
