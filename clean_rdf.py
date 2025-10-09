from rdflib import Graph
import os
import sys

def split_turtle(input_file):
    base, ext = os.path.splitext(input_file)
    cleaned_file = f"{base}_cleaned{ext}"
    needs_curation_file = f"{base}_needs_curation{ext}"

    g_clean = Graph()
    bad_lines = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # Skip comments or empty lines
        if line.strip().startswith("#") or not line.strip():
            continue

        # Try parsing this line as its own graph
        g_tmp = Graph()
        try:
            g_tmp.parse(data=line, format="turtle")
            for triple in g_tmp:
                g_clean.add(triple)
        except Exception as e:
            bad_lines.append(line)

    # Save good triples
    g_clean.serialize(destination=cleaned_file, format="turtle")

    # Save bad triples (raw text, since they are not parseable RDF)
    with open(needs_curation_file, "w", encoding="utf-8") as f:
        f.writelines(bad_lines)

    print(f"Clean triples written to {cleaned_file}")
    print(f"Bad lines written to {needs_curation_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_turtle.py <file.ttl>")
        sys.exit(1)

    input_file = sys.argv[1]
    split_turtle(input_file)