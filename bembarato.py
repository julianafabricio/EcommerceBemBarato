from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Avelino493@localhost:3306/banco_bembarato'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = "pessoa"
    id = db.Column('id_pessoa', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(45))
    email = db.Column('email', db.String(45))
    cpf= db.Column('CPF', db.String(45))
    telefone= db.Column('telefone', db.String(45))
    
    def __init__(self, nome, email, cpf, telefone):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone

class Usuario (db.Model):
    __tablename__ = "usuario"
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    login= db.Column('login', db.String(45))
    senha = db.Column('senha', db.String(45))
    tipo_usuario= db.Column('tipo_usuario', db.String(45))
    
    def __init__(self, login, senha, tipo_usuario):
        self.login = login
        self.senha = senha
        self.tipo_usuario = tipo_usuario

class Categoria (db.Model):
    __tablename__ = "categoria"
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nome_categoria= db.Column('nome_categoria', db.String(45))
    
    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria

class Anuncio (db.Model):
    __tablename__ = "anuncio"
    id = db.Column('id_anuncio', db.Integer, primary_key=True)
    nome_anuncio= db.Column('nome_anuncio', db.String(45))
    descricao_anuncio= db.Column('descricao_anuncio', db.String(45))
    valor_anuncio= db.Column('valor_anuncio', db.String(45))
    data_anuncio= db.Column('data_anuncio', db.String(45))

    def __init__(self, nome_anuncio, descricao_anuncio, valor_anuncio, data_anuncio):
        self.nome_anuncio = nome_anuncio
        self.descricao_anuncio = descricao_anuncio
        self.valor_anuncio = valor_anuncio
        self.data_anuncio = data_anuncio


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/log/cadastro")
def cadastro():
    return render_template ('cadastro.html')

@app.route("/log/caduser", methods=['POST'])
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

if __name__ == 'bembarato':
    with app.app_context():
        db.create_all()