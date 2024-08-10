from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p> BEM BARATO.COM </p>"

@app.route("/sobre")
def sobre():
    return "<h1> Bem Barato.com: O Seu Novo Destino para Anúncios e Compras Econômicas </h1>"


@app.route("/sobre/privacidade")
def privacidade():
    return "<h4>No Bem Barato.com, a sua privacidade é nossa prioridade. </h4>"