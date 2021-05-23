from flask import Flask, render_template
from scrapsteam import pesquisar


app = Flask(__name__)


@app.route("/<pesquisa>")
def teste(pesquisa):

    dados = pesquisar(pesquisa, 1, 50)

    return render_template("dados.html", dados = dados)


if __name__ == '__main__':
    app.run(debug = True)
    