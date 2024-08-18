from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Avelino493@localhost:3306/banco_bembarato'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = "pessoa"
    id_pessoa = db.Column('id_pessoa', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(45))
    email = db.Column('email', db.String(45))
    cpf= db.Column('CPF', db.String(45))
    telefone= db.Column('telefone', db.String(45))
 
    def __init__ (self, nome, email, cpf, telefone):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone


class Categoria (db.Model):
    __tablename__ = "categoria"
    id_categoria= db.Column('id_categoria', db.Integer, primary_key=True)
    nome_categoria= db.Column('nome_categoria', db.String(45))
    
    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria

class Anuncio (db.Model):
    __tablename__ = "anuncio"
    id_anuncio = db.Column('id_anuncio', db.Integer, primary_key=True)
    nome_anuncio= db.Column('nome_anuncio', db.String(45))
    descricao_anuncio= db.Column('descricao_anuncio', db.String(45))
    valor_anuncio= db.Column('valor_anuncio', db.String(45))
    data_anuncio= db.Column('data_anuncio', db.String(45))

    def __init__(self, nome_anuncio, descricao_anuncio, valor_anuncio, data_anuncio):
        self.nome_anuncio = nome_anuncio
        self.descricao_anuncio = descricao_anuncio
        self.valor_anuncio = valor_anuncio
        self.data_anuncio = data_anuncio

class Produtos (db.Model):
    __tablename__ = "produto"
    id_produto= db.Column('id_produto', db.Integer, primary_key=True)
    nome_produto= db.Column('nome_produto', db.String(45))
    descricao_produto= db.Column('descricao_produto', db.String(45))
    valor_produto= db.Column('valor_produto', db.String(45))
    cnpj_fabricante=db.Column ('cnpj_fabricante', db.String(45))
    
    def __init__(self, nome_produto, descricao_produto, valor_produto, cnpj_fabricante):
        self.nome_produto = nome_produto
        self.descricao_produto = descricao_produto
        self.valor_produto = valor_produto
        self.cnpj_fabricante = cnpj_fabricante

class Favorito (db.Model):
    __tablename__ = "favorito"
    id_favorito= db.Column('id_favorito', db.Integer, primary_key=True)
    
    def __init__(self):
       pass

class Endereço (db.Model):
    __tablename__ = "endereco"
    id_endereco= db.Column('id_endereco', db.Integer, primary_key=True)
    nome_endereco= db.Column('nome_endereco', db.String(45))
    numero_endereco= db.Column('numero_endereco', db.String(45))
    bairro=db.Column('bairro', db.String(45))
    cidade= db.Column('cidade', db.String(45))

    def __init__(self, nome_endereco, bairro, cidade):
        self.nome_endereco = nome_endereco
        self.bairro = bairro
        self.cidade = cidade

class Pergunta (db.Model):
    __tablename__ = "pergunta"
    id_pergunta= db.Column('id_pergunta', db.Integer, primary_key=True)
    texto_pergunta = db.Column('texto_pergunta', db.String(45))
    data_pergunta = db.Column ('data_pergunta', db.String (45))

    def __init__(self, texto_pergunta, data_pergunta):
        self.texto_pergunta = texto_pergunta
        self.data_pergunta = data_pergunta

class Envio (db.Model):
    __tablename__ = "envio"
    id_envio= db.Column('id_envio', db.Integer, primary_key=True)
    data_envio= db.Column('data_envio', db.String(45))
    status_envio= db.Column('status_envio', db.String(45))

    def __init__(self, data_envio, status_envio):
        self.data_envio = data_envio
        status_envio = status_envio

class Compra (db.Model):
    __tablename__ = "compra"
    id_compra= db.Column('id_compra', db.Integer, primary_key=True)
    valor_compra= db.Column('valor_compra', db.String(45))
    data_compra=db.Column ('data_compra', db.String(45))
    quantidade= db.Column('quantidade', db.String(45))

    def __init__(self, valor_compra, data_compra, quantidade):
        self.valor_compra = valor_compra
        self.data_compra = data_compra
        self.quantidade = quantidade
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/log/cadastro")
def cadastro():
       return render_template ('cadastro.html', pessoa=Pessoa.query.all())
    
@app.route("/log/caduser", methods=['POST'])
def caduser():
    pessoa= Pessoa (request.form.get('nome'), request.form.get('email'), 
                                  request.form.get('cpf'), request.form.get ('telefone'))
    db.session.add(pessoa)
    db.session.commit()
    print("cadastro realizado com sucesso")
    return redirect(url_for('cadastro'))
   
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