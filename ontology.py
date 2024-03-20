from owlready2 import *
import os
#Kevin Ruiz - 3/1/2024

def load_ontology(ontology_file_path):
    # Load ontology
    onto_path.append(os.path.dirname(ontology_file_path))
    onto = get_ontology("file://" + ontology_file_path).load()
    return onto
 
def get_metadata_comment(ontology):
    # Task 1: Get metadata comment
    query = """
    SELECT ?comment
    WHERE {{
        <http://purl.obolibrary.org/obo/doid.owl> rdf:type owl:Ontology .
        <http://purl.obolibrary.org/obo/doid.owl> rdfs:comment ?comment .
    }}
    """
    # Execute the query
    results = default_world.as_rdflib_graph().query_owlready(query)
    # Print the rdfs:comment value
    for row in results:
        for comment in row:
            print("Metadata Comment:", comment)

def calculate_avg_children_per_class(ontology):
    # Task 1: Calculate average number of children per class
    num_classes = 0
    total_children = 0

    for cls in ontology.classes():
        num_classes += 1
        total_children += len(list(cls.subclasses()))

    average_children_per_class = total_children / num_classes
    return average_children_per_class

def search_entity_by_oboid(ontology, oboid):
    # Task 2: Search entity by OBO ID
    entity = ontology.search_one(id=oboid)

    if entity:
        return entity
    else:
        return None

def search_entity_by_label(ontology, label):
    # Task 2: Search entity by label and output ancestors
    entity = ontology.search_one(label=label)

    if entity:
        ancestors = list(entity.ancestors())
        print(f"Ancestors of {entity}: {ancestors}")
    else:
        print(f"Entity with label {label} not found in the ontology.")

def create_and_save_ontology():
    # Task 3: Create and save custom ontology
    myonto = get_ontology("http://test.org/kevin.owl")

    with myonto:
        class DM(Thing):
            pass

        class T1DM(DM):
            pass

        class T2DM(DM):
            pass

    with myonto:
        insulin_dependent_diabetes = T1DM("insulin-dependent_diabetes_mellitus")

    # Save the ontology in RDF/XML format
    myonto.save(file="kevin.owl", format="rdfxml")

# Main execution
ontology_file_path = os.path.abspath("./Ontology/doid.owl")
ontology = load_ontology(ontology_file_path)

# Task 1: Get metadata comment and calculate average children per class
get_metadata_comment(ontology)
average_children = calculate_avg_children_per_class(ontology)
print("Average Number of Children per Class:", average_children)

# Task 2: Search entities and output subclasses/ancestors
entity_id = "DOID:9351"
found_entity = search_entity_by_oboid(ontology, entity_id)
if found_entity:
    print("Entity found:", found_entity)
    print("Subclasses:", list(found_entity.subclasses()))
else:
    print(f"Entity with OBO ID {entity_id} not found in the ontology.")

search_entity_by_label(ontology, "type 2 diabetes mellitus")

# Task 3: Create and save custom ontology
create_and_save_ontology()
