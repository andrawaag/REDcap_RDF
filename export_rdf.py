#!/usr/bin/env python

from config import config
import requests
import json
import pprint
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import DC, FOAF, DCTERMS
from datetime import datetime

# Save graph with date-stamped filename
today = datetime.today().strftime("%Y_%m_%d")
filename = f"AHRIrc_{today}.ttl"

# Create a Graph
g = Graph()

AHRIRedcap = Namespace("https://population.ahri.org/api/")
AHRIRedcapRecord = Namespace("https://population.ahri.org/api/record/")
# SIO = Namespace("http://semanticscience.org/resource/")

fields = {
    'token': '13FBDF760E7E408C9E5162DF75CEE69A',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.json())

results = r.json()
#pprint.pprint(results)
print(len(results))

for row in results:
    # g.add((AHRIRedcap[row['record_id']], RDF.type, SIO["000088"]))
    for key, value in row.items():
        if value:  # Check if the value is not empty
            g.add((AHRIRedcapRecord[row['record_id']], AHRIRedcap[key], Literal(value)))

        if row['redcap_repeat_instrument'] != '':
            g.add((AHRIRedcap[key], RDFS.label, Literal(key)))
            g.add((AHRIRedcap[key], DCTERMS.isPartOf, AHRIRedcap[row["redcap_repeat_instrument"]]))

construct_query = """
PREFIX redcap: <https://population.ahri.org/api/>
PREFIX ex: <https://www.example.com/leap/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?record rdf:type ex:redcapRecord .
}
WHERE {
  ?record redcap:appraised_by ?appraiser .
}
"""
constructed_graph = g.query(construct_query)
for triple in constructed_graph:
    g.add(triple)
print(g.serialize(destination="data/"+filename, format="turtle"))

