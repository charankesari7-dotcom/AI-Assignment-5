// neo4j_example.cql
// ------------------
// Cypher queries for the AI Research Knowledge Graph in Neo4j
// Author: Student Submission
//
// Neo4j uses the Cypher query language. Nodes are written as ()
// and relationships as -[]->.
// Run these in Neo4j Browser or Bloom after starting a local instance.

// ─── CREATE NODES ────────────────────────────────────────────────────────────

// Create Researchers
CREATE (:Researcher {id: 'turing',  name: 'Alan Turing',      year_born: 1912});
CREATE (:Researcher {id: 'minsky',  name: 'Marvin Minsky',    year_born: 1927});
CREATE (:Researcher {id: 'lecun',   name: 'Yann LeCun',       year_born: 1960});
CREATE (:Researcher {id: 'bengio',  name: 'Yoshua Bengio',    year_born: 1964});
CREATE (:Researcher {id: 'hinton',  name: 'Geoffrey Hinton',  year_born: 1947});

// Create Universities
CREATE (:University {id: 'mit',      name: 'MIT',                         country: 'USA'});
CREATE (:University {id: 'toronto',  name: 'University of Toronto',       country: 'Canada'});
CREATE (:University {id: 'montreal', name: 'Universite de Montreal',      country: 'Canada'});
CREATE (:University {id: 'nyu',      name: 'New York University',         country: 'USA'});

// Create Topics
CREATE (:Topic {id: 'nn',         name: 'Neural Networks'});
CREATE (:Topic {id: 'backprop',   name: 'Backpropagation'});
CREATE (:Topic {id: 'deep_learn', name: 'Deep Learning'});
CREATE (:Topic {id: 'chess_ai',   name: 'Chess AI'});

// Create Papers
CREATE (:Paper {id: 'turing_paper',   title: 'Computing Machinery and Intelligence', year: 1950});
CREATE (:Paper {id: 'imagenet_paper', title: 'ImageNet Classification with Deep CNNs', year: 2012});

// ─── CREATE RELATIONSHIPS ─────────────────────────────────────────────────────

MATCH (r:Researcher {id:'hinton'}), (u:University {id:'toronto'})
CREATE (r)-[:WORKS_AT]->(u);

MATCH (r:Researcher {id:'lecun'}),  (u:University {id:'nyu'})
CREATE (r)-[:WORKS_AT]->(u);

MATCH (r:Researcher {id:'bengio'}), (u:University {id:'montreal'})
CREATE (r)-[:WORKS_AT]->(u);

MATCH (r:Researcher {id:'turing'}), (t:Topic {id:'chess_ai'})
CREATE (r)-[:RESEARCHES]->(t);

MATCH (r:Researcher {id:'hinton'}), (t:Topic {id:'deep_learn'})
CREATE (r)-[:RESEARCHES]->(t);

MATCH (r:Researcher {id:'lecun'}), (t:Topic {id:'deep_learn'})
CREATE (r)-[:RESEARCHES]->(t);

MATCH (r:Researcher {id:'hinton'}), (p:Paper {id:'imagenet_paper'})
CREATE (r)-[:PUBLISHED]->(p);

MATCH (r:Researcher {id:'lecun'}), (p:Paper {id:'imagenet_paper'})
CREATE (r)-[:PUBLISHED]->(p);

MATCH (t1:Topic {id:'deep_learn'}), (t2:Topic {id:'nn'})
CREATE (t1)-[:IS_RELATED_TO]->(t2);

MATCH (t1:Topic {id:'backprop'}), (t2:Topic {id:'nn'})
CREATE (t1)-[:IS_RELATED_TO]->(t2);

// ─── SAMPLE QUERIES ──────────────────────────────────────────────────────────

// Q1: Find all researchers and their universities
MATCH (r:Researcher)-[:WORKS_AT]->(u:University)
RETURN r.name AS Researcher, u.name AS University;

// Q2: Find who researches Deep Learning
MATCH (r:Researcher)-[:RESEARCHES]->(t:Topic {name: 'Deep Learning'})
RETURN r.name;

// Q3: Find all papers published by Hinton
MATCH (r:Researcher {id:'hinton'})-[:PUBLISHED]->(p:Paper)
RETURN p.title, p.year;

// Q4: Find 2-hop path from Turing to Deep Learning
MATCH path = (:Researcher {id:'turing'})-[*..4]->(:Topic {id:'deep_learn'})
RETURN path LIMIT 5;

// Q5: Count researchers per university
MATCH (r:Researcher)-[:WORKS_AT]->(u:University)
RETURN u.name AS University, COUNT(r) AS ResearcherCount
ORDER BY ResearcherCount DESC;
