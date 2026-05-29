"""
ontology_demo.py
----------------
Demonstrates how the Travel Planner reuses Knowledge Bases / Ontologies.
Author: Student Submission

In a full system, these knowledge bases would be stored as:
  - OWL/RDF files (Protégé ontologies)
  - SPARQL-queryable triple stores
  - Neo4j graph databases

Here we simulate the same structure using Python dicts and
demonstrate SPARQL-style querying with filter functions.

Ontologies used:
  1. Tourist Places Ontology  — place types, seasons, cost
  2. Food Recommendation KB   — regional food data
  3. Wine Ontology (adapted)  — pairs wine with regional cuisine
"""

# ─── Simulated Ontology Triples (Subject, Predicate, Object) ──────────────────
# Format mirrors RDF: (entity, property, value)

TOURIST_ONTOLOGY_TRIPLES = [
    ("Goa",      "hasType",      "beach"),
    ("Goa",      "hasType",      "nightlife"),
    ("Goa",      "hasType",      "heritage"),
    ("Goa",      "bestInMonth",  "November"),
    ("Goa",      "bestInMonth",  "December"),
    ("Goa",      "avgCostINR",   3000),
    ("Goa",      "hasRating",    4.5),

    ("Manali",   "hasType",      "mountains"),
    ("Manali",   "hasType",      "adventure"),
    ("Manali",   "bestInMonth",  "May"),
    ("Manali",   "bestInMonth",  "June"),
    ("Manali",   "avgCostINR",   2500),
    ("Manali",   "hasRating",    4.6),

    ("Jaipur",   "hasType",      "heritage"),
    ("Jaipur",   "hasType",      "culture"),
    ("Jaipur",   "bestInMonth",  "November"),
    ("Jaipur",   "bestInMonth",  "December"),
    ("Jaipur",   "avgCostINR",   2000),
    ("Jaipur",   "hasRating",    4.4),

    ("Munnar",   "hasType",      "nature"),
    ("Munnar",   "hasType",      "trekking"),
    ("Munnar",   "bestInMonth",  "October"),
    ("Munnar",   "bestInMonth",  "November"),
    ("Munnar",   "avgCostINR",   2200),
    ("Munnar",   "hasRating",    4.5),
]

FOOD_ONTOLOGY_TRIPLES = [
    ("Goa",    "hasFood", "Fish Curry Rice"),
    ("Goa",    "hasFood", "Bebinca"),
    ("Manali", "hasFood", "Siddu"),
    ("Manali", "hasFood", "Dham"),
    ("Jaipur", "hasFood", "Dal Baati Churma"),
    ("Jaipur", "hasFood", "Laal Maas"),
    ("Munnar", "hasFood", "Puttu & Kadala Curry"),
    ("Munnar", "hasFood", "Kerala Sadya"),
]

# Wine ontology adapted: pairing wine types with cuisine types
WINE_PAIRING_TRIPLES = [
    ("Fish Curry Rice",     "pairsWithWine", "Sauvignon Blanc"),
    ("Bebinca",             "pairsWithWine", "Moscato"),
    ("Dal Baati Churma",    "pairsWithWine", "Shiraz"),
    ("Laal Maas",           "pairsWithWine", "Merlot"),
    ("Puttu & Kadala Curry","pairsWithWine", "Chardonnay"),
    ("Kerala Sadya",        "pairsWithWine", "Pinot Grigio"),
    ("Siddu",               "pairsWithWine", "Riesling"),
    ("Dham",                "pairsWithWine", "Gewürztraminer"),
]


# ─── SPARQL-style Query Functions ─────────────────────────────────────────────

def query_places_by_type(place_type):
    """SELECT ?place WHERE { ?place hasType <place_type> }"""
    return list({s for s, p, o in TOURIST_ONTOLOGY_TRIPLES
                 if p == "hasType" and o == place_type})


def query_places_by_month(month):
    """SELECT ?place WHERE { ?place bestInMonth <month> }"""
    return list({s for s, p, o in TOURIST_ONTOLOGY_TRIPLES
                 if p == "bestInMonth" and o == month})


def query_food_for_place(place):
    """SELECT ?food WHERE { <place> hasFood ?food }"""
    return [o for s, p, o in FOOD_ONTOLOGY_TRIPLES if s == place and p == "hasFood"]


def query_wine_pairing(food_item):
    """SELECT ?wine WHERE { <food> pairsWithWine ?wine }"""
    return [o for s, p, o in WINE_PAIRING_TRIPLES if s == food_item and p == "pairsWithWine"]


def query_places_within_budget(max_cost):
    """SELECT ?place WHERE { ?place avgCostINR ?cost . FILTER(?cost <= max_cost) }"""
    places = set()
    for s, p, o in TOURIST_ONTOLOGY_TRIPLES:
        if p == "avgCostINR" and o <= max_cost:
            places.add(s)
    return list(places)


def full_recommendation(place_type, month, max_cost_inr):
    """
    Simulates a full ontology-driven recommendation:
      1. Query places by type
      2. Filter by month
      3. Filter by budget
      4. Return food + wine pairing for top result
    """
    by_type   = set(query_places_by_type(place_type))
    by_month  = set(query_places_by_month(month))
    by_budget = set(query_places_within_budget(max_cost_inr))

    # Intersection: places satisfying all three constraints
    matched = list(by_type & by_month & by_budget)

    if not matched:
        return {"error": "No place matches the given criteria."}

    # Pick first match (in practice, sort by rating)
    top = matched[0]
    foods = query_food_for_place(top)
    wine_pairings = {f: query_wine_pairing(f) for f in foods}

    return {
        "destination": top,
        "foods": foods,
        "wine_pairings": wine_pairings,
    }


# ─── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Ontology Query Demo ===\n")

    print("1. Beach destinations:")
    print("  ", query_places_by_type("beach"))

    print("\n2. Places good in November:")
    print("  ", query_places_by_month("November"))

    print("\n3. Places within ₹2500/day:")
    print("  ", query_places_within_budget(2500))

    print("\n4. Full Recommendation (heritage, November, ≤₹2500):")
    result = full_recommendation("heritage", "November", 2500)
    print(f"  Destination: {result.get('destination')}")
    print(f"  Foods: {result.get('foods')}")
    print("  Wine Pairings:")
    for food, wines in result.get("wine_pairings", {}).items():
        print(f"    {food} → {', '.join(wines) if wines else 'No pairing found'}")
