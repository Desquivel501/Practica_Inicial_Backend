from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pyodbc

# conn = pyodbc.connect('Driver={SQL Server};'
#     'Server=DESKTOP-0DSCFJO\SQLEXPRESS;'
#     'Database=anotherdatabase;'
#     'Trusted_Connection=yes;')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-D3E52S7\SQLEXPRESS;'
                      'Database=mydatabase;'
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

@app.route('/catedraticos', methods = ['GET'])
def getCatedraticos():

    cursor.execute('SELECT * FROM mydatabase.dbo.Catedraticos')
    Datos=[]
    for row in cursor:
        objeto = {
            "Nombre":row[1]
        }
        Datos.append(objeto)
    return jsonify(Datos)


@app.route('/cursos', methods = ['GET'])
def getCursos():

    cursor.execute('SELECT * FROM mydatabase.dbo.Cursos')
    Datos=[]
    for row in cursor:
        objeto = {
            "Nombre":row[1]
        }
        Datos.append(objeto)
    return jsonify(Datos)

@app.route("/publicacion", methods=["POST"])
def crearPublicacion():
    nombre = request.json['nombre']
    carnet = request.json['carnet']
    titulo = request.json['titulo']
    contenido = request.json['contenido']
    tipo = request.json['tipo']
    
    print(nombre, carnet, tipo, titulo, contenido)
    
    if tipo == "curso":
        curso = request.json['curso']
        sql = "INSERT INTO Publicaciones (NombreUsuario, CarnetUsuario, NombreCurso, NombreCatedratico, Titulo, Contenido) VALUES (?, ?, ?, ?, ?, ?)"
        val = (nombre, carnet, curso, None, titulo, contenido)
        cursor.execute(sql,val)
        conn.commit()
        return jsonify({"Mensaje":"Creado"})
        
    elif tipo == "catedratico":
        catedratico = request.json['catedratico']
        sql = "INSERT INTO Publicaciones (NombreUsuario, CarnetUsuario, NombreCurso, NombreCatedratico, Titulo, Contenido) VALUES (?, ?, ?, ?, ?, ?)"
        val = (nombre, carnet, None, catedratico, titulo, contenido)
        
        cursor.execute(sql,val)
        conn.commit()
        return jsonify({"Mensaje":"Creado"})
    
    return jsonify({"Mensaje":"ERROR"})



@app.route('/publicacion', methods = ['GET'])
def getPublicacion():

    cursor.execute('SELECT * FROM mydatabase.dbo.Publicaciones')
    Datos=[]
    for row in cursor:
        objeto = {
            "PostID":row[0],
            "CarnetUsuario":row[1],
            "NombreUsuario":row[2],
            "NombreCurso":row[3],
            "NombreCatedratico":row[4],
            "Titulo":row[5],
            "Contenido":row[6]
        }
        Datos.append(objeto)
    return jsonify(Datos)

    

        

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)
