from flask import Flask, render_template, request, session

from dbManager import dbManager

app = Flask(__name__,static_folder="templates/static")
@app.route("/")
def hello():
    coltivazioni = dbManager.getColtivazioni()
    return render_template('index.html', coltivazioni = coltivazioni)


@app.route('/search_coltivazione', methods=['GET'])
def handle_data():
    args =request.args
    nome_coltivazione = args["col"]
    print(nome_coltivazione)
    return render_template('visualizza_coltivazione.html')
