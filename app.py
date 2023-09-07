from flask import Flask, render_template, request, session, flash, redirect, url_for

app = Flask(__name__) # nomeia o app com o nome do arquivo
app.config['SECRET_KEY'] = 'pudim'

# Mock de um banco de dados de postagens
posts = [
    {
    "titulo": "Minha primeira postagem!",
    "texto": "Texto do post 1."
    },
    {
    "titulo": "Segundo post.",
    "texto": "Texto do post 2."
    }
]

@app.route('/')
def exibir_entradas():
    entradas = posts # Mock das postagens
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