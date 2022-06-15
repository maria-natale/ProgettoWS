from flask import Flask, render_template, request, session, jsonify
import json
from dbManager import dbManager
from utils import Coltivazione, Encoder


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
    viafirenze=["via rossi","via umberto I","via garibaldi"]
    viapompei=["via della rimembranza","via vittorio emanuele III"]
    viaanzio=["via barbuti","via isolella"]
    
    return render_template('index.html', coltivazioni = coltivazioni, terrenipercitta=terrenipercitta,viafirenze=viafirenze,viaanzio=viaanzio,viapompei=viapompei, citta = citta)


@app.route('/search_coltivazione', methods=['GET'])
def handle_data():
    args = request.args
    nome_coltivazione = args["col"]
    
    coltivazione = dbManager.getColtivazione(nome_coltivazione)
    return render_template('visualizza_coltivazione.html', coltivazione = coltivazione)


@app.route('/search_territoriCitta', methods=['GET'])
def search_territoriCitta():
    args = request.args
    nome_citta = args["c"]
    territorijson=[]
    terrenijson=[]
    territori, terreni = dbManager.getTerreniCitta(nome_citta)
    for territorio in territori:
        if len(territorio.coltivazioni_compatibili)>0:
            print(territorio.coltivazioni_compatibili[0])
    for territorio in territori:
        territorijson.append(Encoder().encode(territorio))
    for terreno in terreni:
        terrenijson.append(Encoder().encode(terreno))
    
    return render_template('visualizza_terreni_citta.html', citta=nome_citta, territori = territorijson, terreni = terrenijson)


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
        terreno=terreno-5
        citta="Pompei"
    elif (terreno == 3 or terreno ==4):
        print(terreno)
        terreno=terreno-3
        print(terreno)
        citta="Anzio"

    terreno=dbManager.getTerritoriCittà(citta)[terreno]
    
    oracolo=dbManager.askTerritorioColtivazione(coltivazione,terreno)
    
    if oracolo:
        oracolo="si può coltivare"
    else:
        oracolo="non si può coltivare qui"
    if request.method == 'GET':
        message = {'oracolo':oracolo}
        return jsonify(message)


@app.route('/describe_coltivazione', methods=['GET'])
def describe_coltivazione():
    args = request.args
    coltivazione = args["col"]
    
    riferimenti = dbManager.describeColtivazione(coltivazione)
    return render_template('describe_coltivazione.html', graphN3 = riferimenti)

