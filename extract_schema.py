import argparse
import shexer
from shexer.shaper import Shaper
from shexer.consts import TURTLE, MIXED_INSTANCES, ALL_EXAMPLES

import importlib.metadata

print("sheXer version:", importlib.metadata.version("shexer"))

namespaces_dict = {
    "http://purl.org/dc/terms/": "dc",
    "http://rdfs.org/ns/void#": "void",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://purl.org/pav/": "pav",
    "http://www.w3.org/ns/dcat#": "dcat",
    "http://xmlns.com/foaf/0.1/": "foaf",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "<https://wsi-omero-prod-02.internal.sanger.ac.uk/": "omero",
    "<http://www.openmicroscopy.org/Schemas/OME/2016-06#": "ome",
}

def run(target_dir, path_to_file, namespaces):
    with open(path_to_file, "r", encoding="utf-8") as f:
        raw_graph = f.read()

    shaper = Shaper(
        raw_graph=raw_graph,
        all_classes_mode=True,
        input_format=TURTLE,
        namespaces_dict=namespaces,
        disable_exact_cardinality=False,
        detect_minimal_iri=True,
        examples_mode=ALL_EXAMPLES,
        instances_report_mode=MIXED_INSTANCES
    )

    result = shaper.shex_graph(
        rdfconfig_directory=target_dir,
        verbose=True,
        acceptance_threshold=0,
        string_output=True
    )

    print(result)

def main():
    parser = argparse.ArgumentParser(description="Run ShExer on an RDF Turtle file.")
    parser.add_argument("target_dir", help="The target directory for RDF configuration.")
    parser.add_argument("path_to_file", help="The path to the RDF Turtle file.")
    parser.add_argument("--namespaces", nargs='*', help="Namespaces to be used in the Shaper. Provide as key=value pairs.")

    args = parser.parse_args()

    # Convert namespaces from command line arguments to a dictionary
    namespaces = {}
    if args.namespaces:
        for namespace in args.namespaces:
            key, value = namespace.split('=')
            namespaces[key] = value
    else:
        namespaces = namespaces_dict

    run(args.target_dir, args.path_to_file, namespaces)

if __name__ == "__main__":
    main()
