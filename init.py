from flask import Flask, render_template, redirect, url_for, request
from scrapsteam import pesquisar
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class jogos(db.Model):
    _id = db.Column("id",db.Integer, primary_key = True)
    titulo = db.Column(db.String(1000))
    preco = db.Column(db.Float)
    gameid = db.Column(db.Integer)
    lancamento = db.Column(db.String(1000))
    reviews = db.Column(db.Integer)
    imagem = db.Column(db.String(1000))
    href = db.Column(db.String(1000))

    def __init__ (self, titulo, preco, gameid, lancamento, reviews, imagem, href):
        self.titulo = titulo
        self.preco = preco
        self.gameid = gameid
        self.lancamento = lancamento
        self.reviews = reviews
        self.imagem = imagem
        self.href = href



@app.route("/pesquisa/Term=<pesquisa>&Tipobusca=<ordem>&Quantidade=<qttd>")
def teste(pesquisa, ordem, qttd):

    dados = pesquisar(pesquisa, ordem, qttd)
  
    for l in dados:
        for item in l:
            encontrar_jogo = jogos.query.filter_by(gameid = item['gameid']).first()
            
            if encontrar_jogo:
                encontrar_jogo.titulo = item['title']
                encontrar_jogo.preco = item['price']
                encontrar_jogo.lancamento = item['released']
                encontrar_jogo.reviews = item['reviews']
                encontrar_jogo.imagem = item['img']
                encontrar_jogo.href = item['href']
                db.session.commit()
                
            else:
                jogo = jogos(item['title'],
                             item['price'],
                             item['gameid'], 
                             item['released'],
                             item['reviews'],
                             item['img'],
                             item['href'])
                db.session.add(jogo)
                db.session.commit()
                
        
    return render_template("dados.html", dados = dados)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form["pesquisa"] == "":
            return render_template("base.html")
        else:
            strp = request.form["pesquisa"]
            ordenar = request.form["ordem"]
            quantidade = request.form["qttd"]
            return redirect(url_for("teste" , pesquisa=strp, ordem=ordenar, qttd=quantidade))

    else:
        return render_template("base.html")

@app.route("/listar")
def listar():
    
    items = jogos.query.all()
    return render_template("listar.html", lista=items)


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
    
