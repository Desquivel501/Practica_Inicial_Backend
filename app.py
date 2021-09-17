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
        user = request.json['user']
        contraseña = request.json['password']
        cursor.execute("SELECT * FROM Usuarios WHERE Usuario = " + f"'{user}'")
        for usuario in cursor:
            if usuario[3] == user:
                if usuario[4] == contraseña:
                    objeto = {
                        'mensaje': 'Sesión iniciada con éxito',
                        'nombre': usuario[1],
                        'apellido': usuario[2],
                        'usuario': usuario[3],
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
    pass

        


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)
