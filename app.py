from flask import Flask, render_template, request, session, abort, flash, redirect, url_for
from posts import posts

app = Flask(__name__) # nomeia o app com o nome do arquivo
app.config['SECRET_KEY'] = 'pudim'
app.config.from_object(__name__) # para que o python possa gerir o sqlite

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
    entradas = posts[::-1] # Mock das postagens, ordem inversa
    return render_template('exibir_entradas.html', entradas=entradas)


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
    if session.logado:
        novo_post = {
            "titulo": request.form['titulo'],
            "texto": request.form['texto']
        }
        posts.append(novo_post)
        flash("Post criado com sucesso!")
    return redirect(url_for('exibir_entradas'))

# @app.route('/posts/<int:id>')
# def exibir_entrada(id):
#     try:
#         entrada = posts[id - 1]
#         return render_template('exibir_entrada.html', entrada=entrada)
#     except Exception:
#         return abort(404)