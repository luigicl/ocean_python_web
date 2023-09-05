from flask import Flask, render_template

app = Flask("Meu App")

# Mock de um banco de dados de postagens
posts = [
    {
    "titulo": "Minha primiera postagem!",
    "texto": "Teste."
    },
      {
    "titulo": "Segundo post.",
    "texto": "Outro teste."
    }
]

@app.route('/')
def exibir_entradas():
    entradas = posts # Mock das postagens
    return render_template('exibir_entradas.html', entradas=entradas)


