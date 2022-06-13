from SPARQLWrapper import SPARQLWrapper, JSON, N3
from rdflib import Graph

from utils import CaratteristicheAmbientali, CaratteristicheClimatiche, CaratteristicheSuolo, Coltivazione, Precipitazioni, Temperatura

jena_endpoint = 'http://localhost:3030/ds/sparql'
dbpedia_endpoint = "http://dbpedia.org/sparql"

class dbManager:
    @staticmethod
    def getColtivazioni():
        sparql = SPARQLWrapper(jena_endpoint)
        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?nome
	            WHERE {
                    ?coltivazione a :coltivazione.
		            ?coltivazione :nome ?nome.}"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        coltivazioni = []
        for result in results["results"]["bindings"]:
            coltivazioni.append(result["nome"]["value"])
            print(result["nome"]["value"])
        return coltivazioni



    @staticmethod
    def getColtivazione(nome):
        sparql = SPARQLWrapper(jena_endpoint)
        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?nomelatino ?caratteristiche_ambientali ?link ?morfologia
	            WHERE {
                    ?coltivazione a :coltivazione.
		            ?coltivazione :nome "%s"^^xsd:string.
                    ?coltivazione :morfologia ?morfologia.
                    ?coltivazione :nomelatino ?nomelatino.
                    ?coltivazione :coltivazione_caratteristiche_ambientali ?caratteristiche_ambientali.
                    ?coltivazione rdfs:seeAlso ?link.}""" %nome
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result = results["results"]["bindings"][0]
        print(result['link']['value'])
        coltivazione = Coltivazione(nome, result['nomelatino']['value'],result['morfologia']['value'],
            result['link']['value'])

        caratteristiche_ambientali = result['caratteristiche_ambientali']['value']
        coltivazione.caratteristicheAmbientali = dbManager.getCaratteristicheAmbientali(caratteristiche_ambientali)

        source = coltivazione.link
        sparql = SPARQLWrapper(dbpedia_endpoint)
        sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/> 
        SELECT ?foto ?comment
        WHERE { 
                <"""+source+"""> dbo:thumbnail ?foto.
                <"""+source+"""> dbo:abstract ?comment.
                FILTER(LANG (?comment) = 'it' ) }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(len(results))
        for result in results["results"]["bindings"]:
            print(result["foto"]["value"])
            coltivazione.thumbnail = result["foto"]["value"]
            coltivazione.comment = result["comment"]["value"]
            
        return coltivazione


    @staticmethod
    def getCaratteristicheAmbientali(source):
        sparql = SPARQLWrapper(jena_endpoint)
        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?car_climatiche ?car_suolo
	            WHERE {
                    <"""+source+"""> a :caratteristiche_ambientali.
 		            <"""+source+"""> :ha_caratteristiche_climatiche ?car_climatiche.
                    <"""+source+"""> :ha_caratteristiche_suolo ?car_suolo.}"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result = results["results"]["bindings"][0]
        
        sourceCC = result['car_climatiche']['value']
        sourceCS = result['car_suolo']['value']
        caratteristicheClimatiche = dbManager.getCaratteristicheClimatiche(sourceCC)
        caratteristicheSuolo = dbManager.getCaratteristicheSuolo(sourceCS)
        caratteristiche_ambientali = CaratteristicheAmbientali(caratteristicheClimatiche, caratteristicheSuolo)
        return caratteristiche_ambientali

    
    @staticmethod
    def getCaratteristicheClimatiche(sourceCC):
        sparql = SPARQLWrapper(jena_endpoint)
        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?temperatura ?precipitazioni ?gradoUmidità
	            WHERE {
                    <"""+sourceCC+"""> a :caratteristiche_climatiche.
 		            <"""+sourceCC+"""> :ha_temperatura ?temperatura.
                    <"""+sourceCC+"""> :ha_precipitazioni ?precipitazioni.
                    <"""+sourceCC+"""> :gradoUmidità ?gradoUmidità.}"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result = results["results"]["bindings"][0]
        sourceTemperatura = result["temperatura"]["value"]
        sourcePrecipitazioni = result["precipitazioni"]["value"]
        gradoUmidità = result["gradoUmidità"]["value"]

        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?temperaturaMin ?temperaturaMax
	            WHERE {
                    <"""+sourceTemperatura+"""> a :temperatura.
 		            OPTIONAL {<"""+sourceTemperatura+"""> :temperaturaMin ?temperaturaMin.
                    <"""+sourceTemperatura+"""> :temperaturaMax ?temperaturaMax }
                    }"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result = results["results"]["bindings"][0]
        try:
            temperaturaMin = result["temperaturaMin"]["value"]
        except:
            temperaturaMin = None
        try:
            temperaturaMax = result["temperaturaMax"]["value"]
        except:
            temperaturaMax = None 
        temperatura = Temperatura(temperaturaMin, temperaturaMax)

        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?precipitazioniMin ?precipitazioniMax
	            WHERE {
                    <"""+sourcePrecipitazioni+"""> a :precipitazioni.
 		            OPTIONAL {<"""+sourcePrecipitazioni+"""> :precipitazioniMin ?precipitazioniMin.
                    <"""+sourcePrecipitazioni+"""> :precipitazioniMax ?precipitazioniMax }
                    }"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result = results["results"]["bindings"][0]
        try:
            precipitazioniMin = result["precipitazioniMin"]["value"]
        except:
            precipitazioniMin = None
        try:
            precipitazioniMax = result["precipitazioniMax"]["value"]
        except:
            precipitazioniMax = None 
        precipitazioni = Precipitazioni(precipitazioniMin, precipitazioniMax)
        return CaratteristicheClimatiche(precipitazioni, temperatura, gradoUmidità)


    @staticmethod
    def getCaratteristicheSuolo(sourceCS):
        sparql = SPARQLWrapper(jena_endpoint)
        sparql.setQuery("""
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2022/5/coltivazioni2#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?altitudine ?drenaggio ?pendenza ?fertilità ?tessitura
	            WHERE {
                    <"""+sourceCS+"""> a :caratteristiche_del_suolo.
 		            <"""+sourceCS+"""> :altitudine ?altitudine.
                    <"""+sourceCS+"""> :drenaggio ?drenaggio.
                    <"""+sourceCS+"""> :fertilità ?fertilità.
                    <"""+sourceCS+"""> :pendenza ?pendenza.
                    <"""+sourceCS+"""> :tessitura ?tessitura.}"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(sourceCS)
        result = results["results"]["bindings"][0]
        altitudine = result["altitudine"]["value"]
        fertilità = result["fertilità"]["value"]
        drenaggio = result["drenaggio"]["value"]
        pendenza = result["pendenza"]["value"]
        tessitura = result["tessitura"]["value"]
        caratteristiche_suolo = CaratteristicheSuolo(pendenza, altitudine, drenaggio, fertilità, tessitura)
        return caratteristiche_suolo


    @staticmethod
    def describeColtivazione(source):
        sparql = SPARQLWrapper(dbpedia_endpoint)
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            DESCRIBE <"""+source+""">
                WHERE { <"""+source+"""> dbo:wikiPageWikiLink ?x
                FILTER ( LANG (?x) = 'it' ) } LIMIT 1
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        riferimenti = []
        sparql.setReturnFormat(N3)
        sparql.setReturnFormat(N3)
        results = sparql.query().convert()
        g = Graph()
        graphN3 = g.parse(data=results, format="n3")
        for s, p, o in graphN3.triples((None, None, None)):
            print(f'{s} {p} {o}')
        return graphN3


dbManager.getColtivazione("Lino")
