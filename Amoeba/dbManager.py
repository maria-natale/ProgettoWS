from SPARQLWrapper import SPARQLWrapper, JSON

from utils import Coltivazione

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
        #nome = nome.strip('\n')
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
        coltivazione = Coltivazione(nome, result['nomelatino']['value'],result['morfologia']['value'],
            result['link']['value'], result['caratteristiche_ambientali']['value'])

        print(coltivazione.caratteristicheAmbientali)

        source = "http://dbpedia.org/resource/Durum"
        sparql = SPARQLWrapper(dbpedia_endpoint)
        sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?foto, ?comment
        WHERE { 
                <"""+source+"""> dbo:thumbnail ?foto.
                <"""+source+"""> rdfs:comment ?comment.
                FILTER(LANG (?comment) = 'it' ) } LIMIT 1
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["foto"]["value"])
            coltivazione.thumbnail = result["foto"]["value"]
            coltivazione.comment = result["comment"]["value"]
            
        return coltivazione

dbManager.getColtivazione("Lino")
