import spacy


def display_sentence_analysis(sentence, nlp_model):
    """Print token and named-entity information for one sentence."""
    document = nlp_model(sentence)
    tokens = [token.text for token in document]

    print(f"Sentence: {sentence}")
    print(f"Tokens: {tokens}")

    if document.ents:
        print("Named entities:")
        for entity in document.ents:
            print(f"- {entity.text}: {entity.label_}")
    else:
        print("Named entities: None")

    print()
    return document.ents


nlp = spacy.load("en_core_web_sm")

# The first two sentences are garden-path examples from the provided reference.
gardenpathSentences = [
    "The old man the boat.",
    "The horse raced past the barn fell.",
    "Mary gave the child a Band-Aid.",
    "That Jill is never here hurts.",
    "The cotton clothing is made of grows in Mississippi.",
]

entity_labels = set()

for garden_path_sentence in gardenpathSentences:
    entities = display_sentence_analysis(garden_path_sentence, nlp)
    entity_labels.update(entity.label_ for entity in entities)

print("Entity label explanations:")
for entity_label in sorted(entity_labels):
    print(f"{entity_label}: {spacy.explain(entity_label)}")

# PERSON means people, including fictional people. It makes sense for Mary and
# Jill because both words are names of people in the sentences.
# GPE means countries, cities, and states. It makes sense for Mississippi because
# it is a state in the United States.