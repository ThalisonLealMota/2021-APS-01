from flask import Flask, render_template, redirect, url_for, request
from scrapsteam import pesquisar


app = Flask(__name__)


@app.route("/pesquisa/Term=<pesquisa>&Tipobusca=<ordem>&Quantidade=<qttd>")
def teste(pesquisa, ordem, qttd):

    dados = pesquisar(pesquisa, ordem, qttd)
        
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



if __name__ == '__main__':
    app.run(debug = True)
    