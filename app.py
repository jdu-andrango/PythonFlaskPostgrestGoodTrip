from flask import Flask, jsonify, send_file,render_template, request,url_for,redirect
from psycopg2 import connect,extras

app= Flask(__name__)



host = 'localhost'
port = 5432
database = 'goodtrip'
user = 'postgres'
password = 'david'


def getConexion():
    conexion = connect(host=host, port=port, database=database,
                       user=user, password=password)
    return conexion


@app.get('/goodtrip/comentario')
def comentary():

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('SELECT * FROM comentarios')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()

    return jsonify(comentarios)


@app.post('/goodtrip/comentario')
def crearComentario():

    nuevoComentario = request.get_json()

    nombre = nuevoComentario['nombre']
    apellido = nuevoComentario['apellido']
    sexo = nuevoComentario['sexo']
    nacionalidad = nuevoComentario['nacionalidad']
    observacion = nuevoComentario['observacion']
    conclucion = nuevoComentario['conclucion']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO comentarios (nombre, apellido, sexo, nacionalidad,observacion,conclucion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, sexo, nacionalidad, observacion, conclucion))
    newComentario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newComentario)


@app.get('/goodtrip/usuarios')
def getUsuario():
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('SELECT * FROM usuario')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()

    return jsonify(comentarios)


@app.post('/goodtrip/usuarios')
def createUsuario():

    nuevoUsuario = request.get_json()

    nombre = nuevoUsuario['nombre']
    apellido = nuevoUsuario['apellido']
    email = nuevoUsuario['email']
    clave = nuevoUsuario['clave']
    sector = nuevoUsuario['sector']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO usuario (nombre, apellido, email, clave,sector) VALUES (%s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, email, clave, sector))
    newUsuario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newUsuario)


@app.get('/goodtrip/comentario/<id>')
def taraerUsuario(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM comentarios WHERE id = %s ', (id, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)
    

@app.delete('/goodtrip/comentario/<id>')
def deleteComentario(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM comentarios WHERE id = %s RETURNING *', (id, ))
    comentarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if comentarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(comentarioEliminado)


@app.put('/goodtrip/comentario/<id>')
def updateUsuario(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
   
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    sexo = newUser['sexo']
    nacionalidad = newUser['nacionalidad']
    observacion = newUser['observacion']
    conclucion = newUser['conclucion']
    
    curSor.execute('UPDATE comentarios SET nombre= %s, apellido= %s, sexo= %s, nacionalidad= %s,observacion= %s,conclucion= %s RETURNING *',(nombre, apellido, sexo, nacionalidad,observacion,conclucion))
    usuarioActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(usuarioActualizado)

@app.route('/')
def home():
    return render_template ('home.html')

@app.route('/templates/register.html')
def register():
    return render_template ('register.html')

@app.route('/templates/login.html')
def login():
    return render_template ('login.html')

@app.route('/templates/sale.html')
def sale():
    return render_template ('sale.html')

@app.route('/templates/manta.html')
def manta():
    return render_template ('manta.html')

@app.route('/templates/atacames.html')
def atacames():
    return render_template ('atacames.html')

@app.route('/templates/galery.html')
def galery():
    return render_template ('galery.html')

@app.route('/templates/prueba.html')
def prueba():
    return render_template ('prueba.html')





if __name__=='__main__':
    app.run(debug=True)