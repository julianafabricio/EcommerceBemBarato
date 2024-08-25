from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Avelino493@localhost:3306/banco_bembarato'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'cavalo come arroz integral'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Cadastro(db.Model):
    __tablename__ = "cadastro"
    id_pessoa = db.Column('id_pessoa', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(45))
    email = db.Column('email', db.String(45))
    cpf= db.Column('CPF', db.String(45))
    telefone= db.Column('telefone', db.String(45))
    endereco= db.Column('endereco', db.String(45))
    numero_endereco= db.Column('numero_endereco', db.String(45))
    bairro=db.Column('bairro', db.String(45))
    cidade= db.Column('cidade', db.String(45))
    senha= db.Column ('senha', db.String(256))
 
    def __init__ (self, nome, email, cpf, telefone, endereco, numero_endereco, bairro, cidade,senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.numero_endereco = numero_endereco
        self.bairro = bairro
        self.cidade = cidade
        self.senha = senha

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id_pessoa)

class Categoria (db.Model):
    __tablename__ = "categoria"
    id_categoria= db.Column('id_categoria', db.Integer, primary_key=True)
    nome_categoria= db.Column('nome_categoria', db.String(45))

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria
    

class Anuncio (db.Model):
    __tablename__ = "anuncio"
    id_anuncio = db.Column('id_anuncio', db.Integer, primary_key=True)
    nome_produto= db.Column('nome_produto', db.String(45))
    descricao_produto= db.Column('descricao_produto', db.String(250))
    valor_produto= db.Column('valor_produto', db.String(45))
    quantidade = db.Column('data_anuncio', db.String(45))
    id_categoria= db.Column('id_categoria',db.Integer, db.ForeignKey("categoria.id_categoria"))

    def __init__(self, nome_produto, descricao_produto, valor_produto, quantidade, id_categoria):
        self.nome_produto = nome_produto
        self.descricao_produto = descricao_produto
        self.valor_produto = valor_produto
        self.quantidade = quantidade
        self.id_categoria = id_categoria

class Favorito (db.Model):
    __tablename__ = "favorito"
    id_favorito= db.Column('id_favorito', db.Integer, primary_key=True)
    
    def __init__(self):
       pass

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

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@login_manager.user_loader
def load_user(id_pessoa):
    return Cadastro.query.get(id_pessoa)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()

        user = Cadastro.query.filter_by(email=email, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/log/cadastro")
def cadastro():
       return render_template ('cadastro.html', pessoas=Cadastro.query.all())
    
@app.route("/log/caduser", methods=['POST'])
def caduser():
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    pessoas= Cadastro (request.form.get('nome'), request.form.get('email'), 
                                  request.form.get('cpf'), request.form.get ('telefone'),
                                  request.form.get('endereco'), request.form.get('numero_endereco'), request.form.get('bairro'),
                                    request.form.get('cidade'), hash)
    db.session.add(pessoas)
    db.session.commit()
    return redirect(url_for('cadastro'))

@app.route("/log/cadastro/detalhar/<int:id_pessoa>")
@login_required
def buscarusuario(id_pessoa):
    pessoa = Cadastro.query.get(id_pessoa)
    return pessoa.nome

@app.route("/log/cadastro/editar/<int:id_pessoa>", methods=['GET','POST'])
@login_required
def editarusuario(id_pessoa):
    pessoa = Cadastro.query.get(id_pessoa)
    if request.method == 'POST':
        pessoa.nome = request.form.get('nome')
        pessoa.email = request.form.get('email')
        pessoa.cpf = request.form.get('cpf')
        pessoa.telefone = request.form.get('telefone')
        pessoa.endereco = request.form.get('endereco')
        pessoa.numero_endereco = request.form.get('numero_endereco')
        pessoa.bairro = request.form.get('bairro')
        pessoa.cidade = request.form.get('cidade')
        pessoa.senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
        db.session.add(pessoa)
        db.session.commit()

        return redirect(url_for('cadastro'))

    return render_template('cadastroeditar.html', pessoa = pessoa)
   

@app.route("/log/cadastro/deletar/<int:id_pessoa>", methods=['GET','POST'])
@login_required
def deletarusuario(id_pessoa):
    pessoa = Cadastro.query.get(id_pessoa)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('cadastro'))

@app.route("/produtos/categoria")
def categoria():
    return render_template ('categoria.html')

@app.route("/produtos/categoria/eletronicos")
def eletronicos():
    return render_template('eletronicos.html')
                           
@app.route("/produtos/categoria/casaedecoracao")
def casaedecoracao():
    return render_template('casaedecoracao.html')

@app.route("/produtos/categoria/camaebanho")
def camaebanho():
    return render_template('camaebanho.html')


@app.route("/produtos/anuncio")
def anuncio():
    return render_template ('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all() )

@app.route("/produtos/novoanuncio", methods=['POST'])
@login_required
def novoanuncio():
    anuncio = Anuncio(request.form.get('nome_produto'), request.form.get('descricao_produto'),
                      request.form.get('valor_produto'),request.form.get('quantidade'),request.form.get('cat'))
        
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/produtos/anuncio/detalhar/<int:id_anuncio>", methods=['GET','POST'])
@login_required
def buscaranuncio(id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    if anuncio is None:
        return "Anúncio não encontrado", 404
    return anuncio.nome_produto

@app.route("/produtos/anuncio/editar/<int:id_anuncio>", methods=['GET','POST'])
@login_required
def editaranuncio (id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    if request.method == 'POST':
        anuncio.nome_produto =  request.form.get ('nome_produto')
        anuncio.descricao_produto = request.form.get ('descricao_produto')
        anuncio.valor_produto = request.form.get ('valor_produto')
        anuncio.quantidade = request.form.get ('quantidade')
        anuncio.id_categoria = request.form.get ('cat')
        db.session.add(anuncio)
        db.session.commit()

        return redirect(url_for('anuncio'))

    return render_template ('anuncioeditar.html', anuncio = anuncio, categorias = Categoria.query.all() )


@app.route("/produtos/anuncio/deletar/<int:id_anuncio>", methods=['GET','POST'])
@login_required
def deletaranuncio (id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))
    
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