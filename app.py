from flask import Flask, jsonify, send_file,render_template, request,url_for,redirect,session
from psycopg2 import connect,extras
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import hashlib
import os
import psycopg2



"""
 ___  ________   ___  ________  ___  ________          ________  _______           ___       ________  ________           ________  ________  ________   _______      ___    ___ ___  ________  ________   _______   ________
|\  \|\   ___  \|\  \|\   ____\|\  \|\   __  \        |\   ___ \|\  ___ \         |\  \     |\   __  \|\   ____\         |\   ____\|\   __  \|\   ___  \|\  ___ \    |\  \  /  /|\  \|\   __  \|\   ___  \|\  ___ \ |\   ____\
\ \  \ \  \\ \  \ \  \ \  \___|\ \  \ \  \|\  \       \ \  \_|\ \ \   __/|        \ \  \    \ \  \|\  \ \  \___|_        \ \  \___|\ \  \|\  \ \  \\ \  \ \   __/|   \ \  \/  / | \  \ \  \|\  \ \  \\ \  \ \   __/|\ \  \___|_
 \ \  \ \  \\ \  \ \  \ \  \    \ \  \ \  \\\  \       \ \  \ \\ \ \  \_|/__       \ \  \    \ \   __  \ \_____  \        \ \  \    \ \  \\\  \ \  \\ \  \ \  \_|/__  \ \    / / \ \  \ \  \\\  \ \  \\ \  \ \  \_|/_\ \_____  \
  \ \  \ \  \\ \  \ \  \ \  \____\ \  \ \  \\\  \       \ \  \_\\ \ \  \_|\ \       \ \  \____\ \  \ \  \|____|\  \        \ \  \____\ \  \\\  \ \  \\ \  \ \  \_|\ \  /     \/   \ \  \ \  \\\  \ \  \\ \  \ \  \_|\ \|____|\  \
   \ \__\ \__\\ \__\ \__\ \_______\ \__\ \_______\       \ \_______\ \_______\       \ \_______\ \__\ \__\____\_\  \        \ \_______\ \_______\ \__\\ \__\ \_______\/  /\   \    \ \__\ \_______\ \__\\ \__\ \_______\____\_\  \
    \|__|\|__| \|__|\|__|\|_______|\|__|\|_______|        \|_______|\|_______|        \|_______|\|__|\|__|\_________\        \|_______|\|_______|\|__| \|__|\|_______/__/ /\ __\    \|__|\|_______|\|__| \|__|\|_______|\_________\
                                                                                                         \|_________|                                                |__|/ \|__|                                       \|_________|


"""


app= Flask(__name__)
app.static_folder = 'static'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


host = 'localhost'
port = 5432
database = 'goodtrip'
user = 'postgres'
password = 'david'




#---------------------------------------------------------------------------
# !                           esta funcion esta dise;ada para conectar la base de datos postgres con Python
#---------------------------------------------------------------------------

def getConexion():
    conexion = connect(host=host, port=port, database=database,
                       user=user, password=password)
    return conexion



#--------------------------------------------------------------------------------------------------------------------------
# *                                                     breakingpoin 
#--------------------------------------------------------------------------------------------------------------------------

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



@app.get('/goodtrip/usuarios/<id_usuario>')
def mostrarUsuario(id_usuario):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM usuario WHERE id_usuario = %s ', (id_usuario, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)

@app.delete('/goodtrip/usuarios/<id_usuario>')
def deleteUsuario(id_usuario):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM usuario WHERE id_usuario = %s RETURNING *', (id_usuario, ))
    usuarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(usuarioEliminado)



@app.put('/goodtrip/usuarios/<id_usuario>')
def updateUser(id_usuario):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
    
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    email =newUser ['email']
    clave = newUser['clave']
    sector =newUser ['sector']
    
    curSor.execute('UPDATE usuario SET nombre= %s, apellido= %s, email= %s, clave= %s,sector= %s RETURNING *',(nombre, apellido, email, clave,sector))
    userActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if userActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(userActualizado)



@app.route('/dashboard')
def dashboard():
    # Verificación de variable de sesión
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

class LoginForm(FlaskForm):
    email = StringField(validators=[
            InputRequired(), Length(min=4, max=222)], render_kw={"placeholder": "Email", "class": "form-control"})

    clave = PasswordField(validators=[
            InputRequired(), Length(min=8, max=222)], render_kw={"placeholder": "Password", "class": "form-control"})

    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})




@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = getConexion()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    form = LoginForm()
    if form.validate_on_submit():
        cur.execute('SELECT * FROM usuario WHERE email= %s', (form.email.data,))
        user = cur.fetchone()
        print(user)
        if user:
            for_clave_hash = form.clave.data
            print(for_clave_hash)
            if user['clave'] == for_clave_hash:
                return redirect(url_for('products'))
    return render_template('login.html', form=form)


@app.route('/')
def home():
    return render_template ('home.html')

@app.route('/templates/register.html')
def register():
    return render_template ('register.html')

@app.route('/templates/products.html')
def products():
    conexion= getConexion()
    curSor= conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM product')
    rows=curSor.fetchall()
    
    
    return render_template ('products.html',products=rows)

@app.route('/add',methods=['POST'])
def add__product_to_cart():
    conexion=getConexion()
    _quantity= int (request.form['quantity'])
    _code=request.form['code']
    print(_quantity)
    print(_code)
    #---------------------------------------------------------------------------------------------------
    #                                          validar los valores recibidos 
    #---------------------------------------------------------------------------------------------------
    if _quantity and _code and request.method=='POST':
        cursor= conexion.cursor(cursor_factory=extras.RealDictCursor)
        
        cursor.execute('SELECT * FROM product WHERE code = %s', (_code,))
        row = cursor.fetchone()
        
        itemArray = {row['code']:{'name':row['name'],'code':row['code'],'quantity':_quantity,'price':row['price'], 'image':row['image'],'total_price':_quantity * row['price']}}
       
        all_total_price= 0
        all_total_quantity= 0 
        
        session.modified=True
        
        if 'cart_item' in session:
            if row ['code'] in session ['cart_item']:
                for key, value in session ['cart_item'].items():
                    if row['code'] == key:
                        old_quantity= session['cart_item'][key]['quantity']
                        all_total_quantity= old_quantity = _quantity
                        session['cart_item'][key]['_quantity']=all_total_quantity
                        session['cart_item'][key]['total_price']=all_total_quantity* row['price'] 
        
            else:
                session['cart_item']= array_merge(session['cart_item'],itemArray)
                
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
           
        
       
        
        else:
            session['cart_item']=itemArray
            all_total_quantity = all_total_quantity + _quantity
            all_total_price=all_total_price=_quantity*row['price']
        
        
        session['all_total_quantity']= all_total_quantity
        session['all_total_price']= all_total_price
        
        
        
        
        return redirect(url_for('products'))
    else:
        return 'Error while adding item to cart'
    
    
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
        
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
         
        for item in session['cart_item'].items():
            if item[0] == code:    
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
         
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
             
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)

def array_merge(first_array, second_array):
    if isinstance(first_array, list)and isinstance(second_array,list):
        return first_array + second_array
    elif isinstance(first_array,dict)and isinstance(second_array,dict):
        return dict(list(first_array.items())+ list(second_array.items()))
    elif isinstance(first_array,set)and isinstance(second_array,set):
        return first_array.union(second_array)
    return False


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

@app.route('/templates/tonsupa.html')
def tonsupa():
    return render_template ('tonsupa.html')


@app.route('/templates/cotopaxi.html')
def cotopaxi():
    return render_template ('cotopaxi.html')




@app.route('/templates/banios.html')
def banios():
    return render_template ('banios.html')




#------------------------------------------------
# todo           comentario atacames
#------------------------------------------------ 

@app.get('/goodtrip/comentarioAtacames')
def comentaryAtacames():

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('SELECT * FROM comentarios_atacames')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()

    return jsonify(comentarios)


@app.post('/goodtrip/comentarioAtacames')
def crearComentarioAtacames():

    nuevoComentario = request.get_json()

    nombre = nuevoComentario['nombre']
    apellido = nuevoComentario['apellido']
    sexo = nuevoComentario['sexo']
    nacionalidad = nuevoComentario['nacionalidad']
    observacion = nuevoComentario['observacion']
    conclucion = nuevoComentario['conclucion']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO comentarios_atacames (nombre, apellido, sexo, nacionalidad,observacion,conclucion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, sexo, nacionalidad, observacion, conclucion))
    newComentario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newComentario)
    

@app.get('/goodtrip/comentarioAtacames/<id>')
def taraerUsuarioAtacames(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM comentarios_atacames WHERE id = %s ', (id, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)
    

@app.delete('/goodtrip/comentarioAtacames/<id>')
def deleteComentarioAtacames(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM comentarios_atacames WHERE id = %s RETURNING *', (id, ))
    comentarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if comentarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(comentarioEliminado)


@app.put('/goodtrip/comentarioAtacames/<id>')
def updateUsuarioAtacames(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
   
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    sexo = newUser['sexo']
    nacionalidad = newUser['nacionalidad']
    observacion = newUser['observacion']
    conclucion = newUser['conclucion']
    
    curSor.execute('UPDATE comentarios_atacames SET nombre= %s, apellido= %s, sexo= %s, nacionalidad= %s,observacion= %s,conclucion= %s RETURNING *',(nombre, apellido, sexo, nacionalidad,observacion,conclucion))
    usuarioActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(usuarioActualizado)



#---------------------------------------------------------------------------------------------------
#                                          comentario tonsupa
#---------------------------------------------------------------------------------------------------





@app.get('/goodtrip/comentarioTonsupa')   #! Esta es la ruta de la peticion get a la base de datos  
def comentaryTonsupa():

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor) #! esto es un modulo de flask que me ayuda a transformar los datos que traigo de la base de datos a diccionario 

    curSor.execute('SELECT * FROM comentarios_tonsupa')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()

    return jsonify(comentarios)


@app.post('/goodtrip/comentarioTonsupa')
def crearComentarioTonsupa():

    nuevoComentario = request.get_json()

    nombre = nuevoComentario['nombre']
    apellido = nuevoComentario['apellido']
    sexo = nuevoComentario['sexo']
    nacionalidad = nuevoComentario['nacionalidad']
    observacion = nuevoComentario['observacion']
    conclucion = nuevoComentario['conclucion']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO comentarios_tonsupa (nombre, apellido, sexo, nacionalidad,observacion,conclucion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, sexo, nacionalidad, observacion, conclucion))
    newComentario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newComentario)
    

@app.get('/goodtrip/comentarioTonsupa/<id>')
def taraerUsuarioTonsupa(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM comentarios_tonsupa WHERE id = %s ', (id, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)
    

@app.delete('/goodtrip/comentarioTonsupa/<id>')
def deleteComentarioTonsupa(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM comentarios_tonsupa WHERE id = %s RETURNING *', (id, ))
    comentarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if comentarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(comentarioEliminado)


@app.put('/goodtrip/comentarioTonsupa/<id>')
def updateUsuarioTonsupa(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
   
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    sexo = newUser['sexo']
    nacionalidad = newUser['nacionalidad']
    observacion = newUser['observacion']
    conclucion = newUser['conclucion']
    
    curSor.execute('UPDATE comentarios_tonsupa SET nombre= %s, apellido= %s, sexo= %s, nacionalidad= %s,observacion= %s,conclucion= %s RETURNING *',(nombre, apellido, sexo, nacionalidad,observacion,conclucion))
    usuarioActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(usuarioActualizado)





#---------------------------------------------------------------------------------------------------
# !                                        comentario cotopaxi
#---------------------------------------------------------------------------------------------------



@app.get('/goodtrip/comentarioCotopaxi')   #! Esta es la ruta de la peticion get a la base de datos  
def comentaryCotopaxi():

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor) #! esto es un modulo de flask que me ayuda a transformar los datos que traigo de la base de datos a diccionario 
    curSor.execute('SELECT * FROM comentarios_cotopaxi')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()
    return jsonify(comentarios)


@app.post('/goodtrip/comentarioCotopaxi')
def crearComentarioCotopaxi():

    nuevoComentario = request.get_json()

    nombre = nuevoComentario['nombre']
    apellido = nuevoComentario['apellido']
    sexo = nuevoComentario['sexo']
    nacionalidad = nuevoComentario['nacionalidad']
    observacion = nuevoComentario['observacion']
    conclucion = nuevoComentario['conclucion']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO comentarios_cotopaxi (nombre, apellido, sexo, nacionalidad,observacion,conclucion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, sexo, nacionalidad, observacion, conclucion))
    newComentario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newComentario)
    

@app.get('/goodtrip/comentarioCotopaxi/<id>')
def taraerUsuarioCotopaxi(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM comentarios_cotopaxi WHERE id = %s ', (id, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)
    

@app.delete('/goodtrip/comentarioCotopaxi/<id>')
def deleteComentarioCotopaxi(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM comentarios_cotopaxi WHERE id = %s RETURNING *', (id, ))
    comentarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if comentarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(comentarioEliminado)


@app.put('/goodtrip/comentarioCotopaxi/<id>')
def updateUsuarioCotopaxi(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
   
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    sexo = newUser['sexo']
    nacionalidad = newUser['nacionalidad']
    observacion = newUser['observacion']
    conclucion = newUser['conclucion']
    
    curSor.execute('UPDATE comentarios_cotopaxi SET nombre= %s, apellido= %s, sexo= %s, nacionalidad= %s,observacion= %s,conclucion= %s RETURNING *',(nombre, apellido, sexo, nacionalidad,observacion,conclucion))
    usuarioActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(usuarioActualizado)




#---------------------------------------------------------------------------------------------------
# !                                        comentario banios
#---------------------------------------------------------------------------------------------------



@app.get('/goodtrip/comentarioBanios')   #! Esta es la ruta de la peticion get a la base de datos  
def comentaryBanios():

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor) #! esto es un modulo de flask que me ayuda a transformar los datos que traigo de la base de datos a diccionario 
    curSor.execute('SELECT * FROM comentarios_banios')
    comentarios = curSor.fetchall()
    curSor.close()
    conexion.close()
    return jsonify(comentarios)


@app.post('/goodtrip/comentarioBanios')
def crearComentarioBanios():

    nuevoComentario = request.get_json()

    nombre = nuevoComentario['nombre']
    apellido = nuevoComentario['apellido']
    sexo = nuevoComentario['sexo']
    nacionalidad = nuevoComentario['nacionalidad']
    observacion = nuevoComentario['observacion']
    conclucion = nuevoComentario['conclucion']

    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

    curSor.execute('INSERT INTO comentarios_banios (nombre, apellido, sexo, nacionalidad,observacion,conclucion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * ',
                   (nombre, apellido, sexo, nacionalidad, observacion, conclucion))
    newComentario = curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    return jsonify(newComentario)
    

@app.get('/goodtrip/comentarioBanios/<id>')
def taraerUsuarioBanios(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM comentarios_banios WHERE id = %s ', (id, ))
    traerUsuario=curSor.fetchone()
    
    
    if traerUsuario is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerUsuario)
    return jsonify(traerUsuario)
    

@app.delete('/goodtrip/comentarioBanios/<id>')
def deleteComentarioBanios(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM comentarios_banios WHERE id = %s RETURNING *', (id, ))
    comentarioEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if comentarioEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(comentarioEliminado)


@app.put('/goodtrip/comentarioBanios/<id>')
def updateUsuarioBanios(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newUser= request.get_json()
   
    nombre = newUser['nombre']
    apellido = newUser['apellido']
    sexo = newUser['sexo']
    nacionalidad = newUser['nacionalidad']
    observacion = newUser['observacion']
    conclucion = newUser['conclucion']
    
    curSor.execute('UPDATE comentarios_banios SET nombre= %s, apellido= %s, sexo= %s, nacionalidad= %s,observacion= %s,conclucion= %s RETURNING *',(nombre, apellido, sexo, nacionalidad,observacion,conclucion))
    usuarioActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if usuarioActualizado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    

    return jsonify(usuarioActualizado)








if __name__=='__main__':
    app.run(debug=True)