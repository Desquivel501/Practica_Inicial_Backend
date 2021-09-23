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
            "CarnetUsuario":row[2],
            "NombreUsuario":row[1],
            "NombreCurso":row[3],
            "NombreCatedratico":row[4],
            "Titulo":row[5],
            "Contenido":row[6]
        }
        Datos.append(objeto)
    return jsonify(Datos)

@app.route('/publicacion/filtro/<string:id>', methods = ['GET'])
def getPublicacionFiltro(id):
    filtro = id
    
    Datos=[]
    if filtro == "1":
        comando = 'SELECT * FROM mydatabase.dbo.Publicaciones WHERE NombreCurso IS NOT NULL'
    elif filtro == "2":
        comando = 'SELECT * FROM mydatabase.dbo.Publicaciones WHERE NombreCatedratico IS NOT NULL'
    else:
        comando = 'SELECT * FROM mydatabase.dbo.Publicaciones'

    cursor.execute(comando)
    for row in cursor:
        objeto = {
            "PostID":row[0],
            "CarnetUsuario":row[2],
            "NombreUsuario":row[1],
            "NombreCurso":row[3],
            "NombreCatedratico":row[4],
            "Titulo":row[5],
            "Contenido":row[6]
        }
        Datos.append(objeto)
    return jsonify(Datos)


@app.route('/publicacion/<string:id>', methods = ['GET'])
def getPublicacionIndividual(id):

    cursor.execute('SELECT * FROM mydatabase.dbo.Publicaciones')
    Datos=[]
    print(id)
    for row in cursor:

        # objeto = {"Mensaje":"No se encontro el post"}
        
        if int(row[0]) == int(id):
            objeto = {
                "PostID":row[0],
                "CarnetUsuario":row[2],
                "NombreUsuario":row[1],
                "NombreCurso":row[3],
                "NombreCatedratico":row[4],
                "Titulo":row[5],
                "Contenido":row[6],
                "Mensaje":"Done"
            } 
            
    return jsonify(objeto)

@app.route("/comentario", methods=["POST"])
def crearComentario():
    nombreUsuario = request.json['nombreUsuario']
    contenido = request.json['contenido']
    postId = request.json['postId']

    sql = "INSERT INTO Comentarios (NombreUsuario, Contenido, PostID) VALUES (?, ?, ?)"
    val = (nombreUsuario, contenido, postId)
    cursor.execute(sql,val)
    conn.commit()
    
    return jsonify({"Mensaje":"Creado"})


@app.route("/comentario/<string:id>", methods=["GET"])
def getComentarios(id):

    cursor.execute(f"SELECT * FROM mydatabase.dbo.Comentarios WHERE PostID={id}")
    datos = []
    found = False
    for row in cursor:
        print (row)
        found = True
        objeto = {
                "CommentID":row[0],
                "NombreUsuario":row[1],
                "Contenido":row[2],
                "PostID":row[3],
                "Mensaje":"Existe"
            } 
        datos.append(objeto)
    

    return jsonify(datos)


@app.route("/buscar/<string:carnet>", methods=["GET"])
def buscarUsuarios(carnet):

    cursor.execute(f"SELECT * FROM mydatabase.dbo.Usuarios WHERE Carnet={carnet}")
    found = False
    for row in cursor:
        found = True
        objeto = {
                "Nombre":row[0],
                "Apellido":row[1],
                "Carnet":row[2],
                "Contraseña":row[3],
                "Correo":row[4],
                "Mensaje":"Existe"
        } 
    if not found:
        objeto = {"Mensaje":"No Existe"}

    return jsonify(objeto)


@app.route('/publicacion/buscar/<string:cadena>', methods = ['GET'])
def getPublicacionBusqueda(cadena):

    cursor.execute('SELECT * FROM mydatabase.dbo.Publicaciones')
    Datos=[]
    print(id)
    
    for row in cursor:

        nombreCatedratico = str(row[4]).lower()
        nombreCurso = str(row[3]).lower()
        found = False
        
        if nombreCurso.find(cadena.lower()) >= 0:
            found = True
            
        if nombreCatedratico.find(cadena.lower()) >= 0:
            found = True

        if found or (cadena is None):
            objeto = {
                "PostID":row[0],
                "CarnetUsuario":row[2],
                "NombreUsuario":row[1],
                "NombreCurso":row[3],
                "NombreCatedratico":row[4],
                "Titulo":row[5],
                "Contenido":row[6],
            } 
            Datos.append(objeto)
            
    return jsonify(Datos)

    

        

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)
