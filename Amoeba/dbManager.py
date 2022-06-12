from SPARQLWrapper import SPARQLWrapper, JSON


class dbManager:
    @staticmethod
    def getColtivazioni():
        sparql = SPARQLWrapper('http://localhost:3030/ds/sparql')
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



dbManager().getColtivazioni()