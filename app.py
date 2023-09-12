from flask import Flask, render_template, g, request, session, abort, flash, redirect, url_for
from posts import posts
import sqlite3

app = Flask(__name__) # nomeia o app com o nome do arquivo
app.config['SECRET_KEY'] = 'pudim'
app.config.from_object(__name__) # para que o python possa gerir o sqlite
DATABASE = "banco.bd"

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.bd = conectar() # criar conexão com o BD

@app.teardown_request
def teardown_request(f): # essa função precisa de um argumento, então colocamos qqr coisa
    g.bd.close() # fechar a conexão com o BD



# Mock de um banco de dados de postagens
# posts = [
#     {
#     "titulo": "Minha primeira postagem!",
#     "texto": "Texto do post 1."
#     },
#     {
#     "titulo": "Segundo post.",
#     "texto": "Texto do post 2."
#     }
# ]

@app.route('/')
def exibir_entradas():
    # entradas = posts[::-1] # Mock das postagens, ordem inversa

    sql = " SELECT titulo, texto, data_criacao FROM posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)

    entrada = []

    for titulo, texto, data_criacao in resultado.fetchall():
        entrada.append({
            "titulo":titulo,
            "texto":texto,
            "data_criacao":data_criacao
        })

    return render_template('exibir_entradas.html', entradas=entrada)


@app.route('/login', methods=["GET", "POST"]) # se não declarar os métodos a rota aceita apenas GET
def login():
    erro = None
    if request.method == "POST":
       # o nome dos campos username e password foram definidos no login.html
       if request.form['username'] == "admin" and request.form['password'] == "admin":
           session['logado'] = True
           flash("Login realizado com sucesso!")
           return redirect(url_for('exibir_entradas'))
       erro = "Usuário ou senha inválidos"
    return render_template('login.html', erro=erro) # se não foi POST, vai ser GET, então não precisa de else


@app.route('/logout')
def logout():
    session.pop('logado') # remove os dados de login do dicionário da sessão
    flash("Logout efetuado com sucesso!")
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    if not session['logado']:
        abort(401)
    titulo = request.form.get('titulo')
    texto = request.form.get('texto')
    sql = "INSERT INTO posts (titulo, texto) values(?,?)"
    g.bd.execute(sql,[titulo, texto])
    g.bd.commit()
    flash("Post criado com sucesso!")
    return redirect(url_for('exibir_entradas'))

# @app.route('/posts/<int:id>')
# def exibir_entrada(id):
#     try:
#         entrada = posts[id - 1]
#         return render_template('exibir_entrada.html', entrada=entrada)
#     except Exception:
#         return abort(404)