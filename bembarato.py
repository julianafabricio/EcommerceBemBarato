from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://julianafabricio:Avelino493@localhost:3306/bembarato'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class pessoa(db.Model):
    __tablename__ = "pessoa"
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(45))
    email = db.Column('email', db.String(45))
    cpf= db.Column('CPF', db.String(45))
    telefone= db.Column('telefone', db.String(45))
    
    def __init__(self, nome, email, cpf, telefone):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone

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

if __name__ == 'bembarato':
        db.create_all()