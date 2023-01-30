from flask import Flask, jsonify, send_file,render_template
from psycopg2 import connect,extras

app= Flask(__name__)

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