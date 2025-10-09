import rdflib

g = rdflib.Graph()
#g.parse('data/sanger-rdf-20250819_cleaned.ttl', format='turtle')
print(len(g))
g.parse('data/AHRI/AHRIrc_2025_09_17.ttl', format='turtle')

print(len(g))
g.parse('data/AHRI/all_ome_2025_09_23.nt', format='ntriples')
print(len(g))

g.serialize(destination='data/AHRI/combined_data.ttl', format='turtle')

# Define the SPARQL INSERT query
sparql_query = """
PREFIX ome: <http://www.openmicroscopy.org/rdf/2016-06/ome_core/>
PREFIX redcap: <https://population.ahri.org/api/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT {
    ?redcapRecord dc:identifier ?constructedURI ;
                  rdf:type redcap:record .
} WHERE {
    ?redcapRecord redcap:lab_id ?redCapId .
    BIND(URI(CONCAT("https://population.ahri.org/api/", REPLACE(STR(?redCapId), " ", ""))) AS ?constructedURI)
}
"""

# Get the number of triples before the update
num_triples_before = len(g)

# Execute the SPARQL INSERT query
g.update(sparql_query)

# Get the number of triples after the update
num_triples_after = len(g)

# Calculate the number of updates made
num_updates = num_triples_after - num_triples_before

# Print the number of updates made
print(f"Number of updates made: {num_updates}")

# Define the SPARQL INSERT query
sparql_query = """
PREFIX ome: <http://www.openmicroscopy.org/rdf/2016-06/ome_core/>

INSERT {
    ?omeRecord dc:identifier ?constructedURI . 
} 
WHERE {
    ?omeRecord ome:Map ?map .
    ?map ome:Key "lab_id_main" ;
         ome:Value  ?omeID.

    BIND(IRI(CONCAT("https://population.ahri.org/api/", ?omeID)) AS ?constructedURI)
}
"""

# Get the number of triples before the update
num_triples_before = len(g)

# Execute the SPARQL INSERT query
g.update(sparql_query)

# Get the number of triples after the update
num_triples_after = len(g)

# Calculate the number of updates made
num_updates = num_triples_after - num_triples_before

# Print the number of updates made
print(f"Number of updates made: {num_updates}")

# Serialize the updated graph to a file
g.serialize(destination='data/AHRI/combined_data_updated.ttl', format='turtle')