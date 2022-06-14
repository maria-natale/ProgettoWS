from flask import Flask, render_template, request, session, jsonify
import json
from dbManager import dbManager
from utils import Coltivazione

app = Flask(__name__,static_folder="templates/static")
app.jinja_env.filters['zip'] = zip
@app.route("/")
def hello():
    terrenipercitta={}
    coltivazioni = dbManager.getColtivazioni()
    citta = dbManager.getCittà()
    

    for i in citta:
        terrenipercitta[i.nome]=dbManager.getTerritoriCittà(i.nome)
        
    #print(json.dumps(terrenipercitta, indent=4))
    #terreni = dbManager.getTerreni()
    viafirenze=["via rossi","via sebillo","via garibaldi"]
    viapompei=["via casillo","via natale"]
    viaanzio=["via battistoni","via auguri"]
    
    return render_template('index.html', coltivazioni = coltivazioni, terrenipercitta=terrenipercitta,viafirenze=viafirenze,viaanzio=viaanzio,viapompei=viapompei)


@app.route('/search_coltivazione', methods=['GET'])
def handle_data():
    args = request.args
    nome_coltivazione = args["col"]
    
    coltivazione = dbManager.getColtivazione(nome_coltivazione)
    return render_template('visualizza_coltivazione.html', coltivazione = coltivazione)

@app.route('/askcoltivabile', methods=['GET'])
def askcoltavibile():
    args = request.args 
    coltivazione = args["col"]
    terreno = args["terr"]
    print(terreno)
    print("AAAAAAAAAAA")
    print(coltivazione)
    terreno=int(terreno)
    if (terreno<3):
        citta="Firenze"
    elif (terreno > 4):
        terreno=terreno-3
        citta="Anzio"
    else:
        terreno=terreno-5
        citta="Pompei"

    terreno=dbManager.getTerritoriCittà(citta)[terreno]
    print(terreno)
    oracolo=dbManager.askTerritorioColtivazione(coltivazione,terreno)
    print(oracolo)
    if request.method == 'GET':
        message = {'oracolo':oracolo}
        return jsonify(message)
@app.route('/describe_coltivazione', methods=['GET'])
def describe_coltivazione():
    args = request.args
    coltivazione = args["col"]
    
    riferimenti = dbManager.describeColtivazione(coltivazione)
    return render_template('describe_coltivazione.html', graphN3 = riferimenti)

