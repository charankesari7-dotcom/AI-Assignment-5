"""
kg_demo.py
----------
Knowledge Graph Demo (Pure Python Implementation)
Author: Student Submission

A Knowledge Graph (KG) is a graph-structured data model where:
  - NODES represent entities (people, places, concepts)
  - EDGES represent relationships between entities
  - Each node/edge can have PROPERTIES (attributes)

This demo implements a small KG for an AI domain using Python
dicts to represent the graph structure. In production, this would
be stored in Neo4j or as RDF triples in a triple store.

Example KG: AI Research Domain
  Entities: Researchers, Universities, Papers, Topics
  Relations: WORKS_AT, PUBLISHED, RESEARCHES, CITES
"""


class KnowledgeGraph:
    """
    A simple in-memory Knowledge Graph using adjacency lists.
    Supports nodes with properties and labelled directed edges.
    """

    def __init__(self):
        self.nodes = {}   # {node_id: {type, properties}}
        self.edges = []   # list of {from, to, relation, properties}

    def add_node(self, node_id, node_type, **properties):
        """Add or update a node."""
        self.nodes[node_id] = {"type": node_type, "properties": properties}

    def add_edge(self, from_node, to_node, relation, **properties):
        """Add a directed edge between two nodes."""
        self.edges.append({
            "from": from_node,
            "to": to_node,
            "relation": relation,
            "properties": properties,
        })

    def query_by_type(self, node_type):
        """Return all nodes of a given type."""
        return {nid: data for nid, data in self.nodes.items()
                if data["type"] == node_type}

    def query_neighbors(self, node_id, relation=None):
        """
        Return all nodes connected from node_id.
        Optionally filter by relation type.
        """
        results = []
        for edge in self.edges:
            if edge["from"] == node_id:
                if relation is None or edge["relation"] == relation:
                    results.append((edge["to"], edge["relation"]))
        return results

    def query_incoming(self, node_id, relation=None):
        """Return all nodes that connect TO node_id."""
        results = []
        for edge in self.edges:
            if edge["to"] == node_id:
                if relation is None or edge["relation"] == relation:
                    results.append((edge["from"], edge["relation"]))
        return results

    def find_path(self, start, end, visited=None):
        """
        Simple DFS path finding from start to end.
        Returns path as list of node_ids or None if not found.
        """
        if visited is None:
            visited = set()
        if start == end:
            return [start]
        visited.add(start)
        for (neighbor, _) in self.query_neighbors(start):
            if neighbor not in visited:
                path = self.find_path(neighbor, end, visited)
                if path:
                    return [start] + path
        return None

    def print_summary(self):
        """Print a summary of the graph."""
        print(f"Knowledge Graph Summary:")
        print(f"  Nodes : {len(self.nodes)}")
        print(f"  Edges : {len(self.edges)}")
        print(f"  Types : {set(d['type'] for d in self.nodes.values())}")


def build_ai_research_kg():
    """
    Build a sample Knowledge Graph for the AI Research domain.

    Entities:
      Researchers: Turing, Minsky, LeCun, Bengio, Hinton
      Universities: MIT, Toronto, Montreal, NYU
      Topics: Neural Networks, Backprop, Deep Learning, Chess AI
      Papers: (simplified names)
    """
    kg = KnowledgeGraph()

    # ── Nodes ────────────────────────────────────────────────────────────────
    # Researchers
    kg.add_node("turing",  "Researcher", name="Alan Turing",      year_born=1912)
    kg.add_node("minsky",  "Researcher", name="Marvin Minsky",    year_born=1927)
    kg.add_node("lecun",   "Researcher", name="Yann LeCun",       year_born=1960)
    kg.add_node("bengio",  "Researcher", name="Yoshua Bengio",    year_born=1964)
    kg.add_node("hinton",  "Researcher", name="Geoffrey Hinton",  year_born=1947)

    # Universities
    kg.add_node("mit",      "University", name="MIT",             country="USA")
    kg.add_node("toronto",  "University", name="University of Toronto", country="Canada")
    kg.add_node("montreal", "University", name="Université de Montréal", country="Canada")
    kg.add_node("nyu",      "University", name="New York University",    country="USA")

    # Topics
    kg.add_node("nn",          "Topic", name="Neural Networks")
    kg.add_node("backprop",    "Topic", name="Backpropagation")
    kg.add_node("deep_learn",  "Topic", name="Deep Learning")
    kg.add_node("chess_ai",    "Topic", name="Chess AI")

    # Papers
    kg.add_node("computing_machinery", "Paper",
                title="Computing Machinery and Intelligence", year=1950)
    kg.add_node("imagenet_paper", "Paper",
                title="ImageNet Classification with Deep CNNs", year=2012)
    kg.add_node("lstm_paper", "Paper",
                title="Long Short-Term Memory", year=1997)

    # ── Edges ────────────────────────────────────────────────────────────────
    # WORKS_AT
    kg.add_edge("turing",  "mit",      "WORKS_AT")
    kg.add_edge("minsky",  "mit",      "WORKS_AT")
    kg.add_edge("hinton",  "toronto",  "WORKS_AT")
    kg.add_edge("bengio",  "montreal", "WORKS_AT")
    kg.add_edge("lecun",   "nyu",      "WORKS_AT")

    # RESEARCHES
    kg.add_edge("turing",  "chess_ai",   "RESEARCHES")
    kg.add_edge("minsky",  "nn",         "RESEARCHES")
    kg.add_edge("hinton",  "backprop",   "RESEARCHES")
    kg.add_edge("hinton",  "deep_learn", "RESEARCHES")
    kg.add_edge("lecun",   "deep_learn", "RESEARCHES")
    kg.add_edge("bengio",  "deep_learn", "RESEARCHES")

    # PUBLISHED
    kg.add_edge("turing",  "computing_machinery", "PUBLISHED")
    kg.add_edge("lecun",   "imagenet_paper",       "PUBLISHED")
    kg.add_edge("hinton",  "imagenet_paper",       "PUBLISHED")

    # TOPIC_OF (paper → topic)
    kg.add_edge("computing_machinery", "chess_ai",   "TOPIC_OF")
    kg.add_edge("imagenet_paper",      "deep_learn",  "TOPIC_OF")
    kg.add_edge("lstm_paper",          "nn",          "TOPIC_OF")

    # IS_RELATED_TO (topic → topic)
    kg.add_edge("backprop",   "nn",         "IS_RELATED_TO")
    kg.add_edge("deep_learn", "nn",         "IS_RELATED_TO")
    kg.add_edge("deep_learn", "backprop",   "IS_RELATED_TO")

    return kg


# ─── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    kg = build_ai_research_kg()
    kg.print_summary()

    print("\n1. All Researchers in KG:")
    for nid, data in kg.query_by_type("Researcher").items():
        print(f"   {data['properties']['name']} (id: {nid})")

    print("\n2. What does Hinton research?")
    for (neighbor, rel) in kg.query_neighbors("hinton", relation="RESEARCHES"):
        topic_name = kg.nodes[neighbor]["properties"]["name"]
        print(f"   {rel} → {topic_name}")

    print("\n3. Who works at MIT?")
    for (researcher, rel) in kg.query_incoming("mit", relation="WORKS_AT"):
        name = kg.nodes[researcher]["properties"]["name"]
        print(f"   {name}")

    print("\n4. Path from Turing → Deep Learning:")
    path = kg.find_path("turing", "deep_learn")
    if path:
        print("   " + " → ".join(path))
    else:
        print("   No path found")

    print("\n5. Who published the ImageNet paper?")
    for (researcher, rel) in kg.query_incoming("imagenet_paper", relation="PUBLISHED"):
        name = kg.nodes[researcher]["properties"]["name"]
        print(f"   {name}")
