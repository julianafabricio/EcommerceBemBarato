from flask import Flask, make_response, request
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/log/cadastro")
def cadastro():
    return render_template ('cadastro.html')

@app.route("/log/caduser", methods=['post'])
def caduser():
    return request.form


@app.route("/log/acesso")
def acesso():
    return render_template ('acesso.html')

@app.route("/produtos/categoria")
def categoria():
    return render_template ('categoria.html')

@app.route("/produtos/busca")
def busca():
    return render_template ('busca.html')

@app.route("/produtos/anuncio")
def anuncio():
    return render_template ('anuncio.html')

@app.route("/produtos/perguntas")
def perguntas():
    return render_template ('perguntas.html')

@app.route("/relatorios/compras")
def relcompras():
    return render_template ('relcompras.html')

@app.route("/relatorios/vendas")
def relvendas():
    return render_template ('relvendas.html')

