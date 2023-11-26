from rdflib import Graph,Namespace, RDF, Literal
from rdflib.plugins.sparql import prepareQuery

loaded_rdf_graph = Graph()
loaded_rdf_graph.parse("pressure.ttl", format="turtle")

sosa = Namespace("http://www.w3.org/ns/sosa/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

sparql_query = prepareQuery("""
    SELECT ?observation ?pressure ?timestamp
    WHERE {
        ?observation rdf:type sosa:Observation ;
                     sosa:hasSimpleResult ?pressure ;
                     sosa:resultTime ?timestamp .
    }
    ORDER BY ?timestamp
""", initNs={'rdf': RDF, 'sosa': sosa, 'xsd': xsd})

results = loaded_rdf_graph.query(sparql_query)

for result in results:
    print(f"Observation: {result['observation']}")
    print(f"Pressure: {result['pressure']}")
    print(f"Timestamp: {result['timestamp']}")
    print("-----")


