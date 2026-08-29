import spacy


def print_word_similarities(nlp_model):
    """Print similarity scores for the required word comparisons."""
    words = {
        "cat": nlp_model("cat"),
        "monkey": nlp_model("monkey"),
        "banana": nlp_model("banana"),
    }

    print("Word similarities:")
    print(f"cat and monkey: {words['cat'].similarity(words['monkey']):.4f}")
    print(
        f"monkey and banana: "
        f"{words['monkey'].similarity(words['banana']):.4f}"
    )
    print(f"cat and banana: {words['cat'].similarity(words['banana']):.4f}")
    print()


def print_token_similarities(nlp_model):
    """Print pairwise similarities for the supplied tokens."""
    tokens = nlp_model("cat apple monkey banana")

    print("Token similarities:")
    for first_token in tokens:
        for second_token in tokens:
            similarity = first_token.similarity(second_token)
            print(
                f"{first_token.text} and {second_token.text}: "
                f"{similarity:.4f}"
            )
    print()


def print_sentence_similarities(nlp_model):
    """Compare the supplied sentences with a sentence about a cat and car."""
    sentence_to_compare = "Why is my cat on the car"
    sentences = [
        "where did my dog go",
        "Hello, there is my car",
        "I've lost my car in my car",
        "I'd like my boat back",
        "I will name my dog Diana",
    ]
    reference_sentence = nlp_model(sentence_to_compare)

    print(f"Similarities to: {sentence_to_compare}")
    for sentence in sentences:
        similarity = nlp_model(sentence).similarity(reference_sentence)
        print(f"{sentence}: {similarity:.4f}")
    print()


def print_document_similarities(documents, nlp_model, title):
    """Print pairwise similarity scores for a collection of documents."""
    processed_documents = [nlp_model(document) for document in documents]

    print(title)
    for first_index, first_document in enumerate(processed_documents, start=1):
        for second_index, second_document in enumerate(
            processed_documents, start=1
        ):
            similarity = first_document.similarity(second_document)
            print(
                f"Document {first_index} and document {second_index}: "
                f"{similarity:.4f}"
            )
    print()


def print_cross_collection_similarities(recipes, complaints, nlp_model):
    """Print similarities between every recipe and complaint."""
    processed_recipes = [nlp_model(recipe) for recipe in recipes]
    processed_complaints = [nlp_model(complaint) for complaint in complaints]

    print("Recipe and complaint similarities:")
    for recipe_index, recipe in enumerate(processed_recipes, start=1):
        for complaint_index, complaint in enumerate(processed_complaints, start=1):
            similarity = recipe.similarity(complaint)
            print(
                f"Recipe {recipe_index} and complaint {complaint_index}: "
                f"{similarity:.4f}"
            )
    print()


complaints = [
    "We bought a house in CA. Our mortgage was handled by a company "
    "called ki. Soon after the mortgage was sold to ABC. Shortly after "
    "that XYZ took over the mortgage. The other day we got a notice not "
    "to send our payment to them but to loi instead. This is all so "
    "frustrating and wreaks of the mortgage nightmare.",
    "I got approved for a loan to buy a house. I submitted everything I "
    "needed, paid for the inspection, and paid a good faith check. After "
    "all of that, they said I did not get approved for the loan.",
    "I recently pulled my credit report and noticed a collection listing "
    "from The University. I was never notified of this collection action "
    "or that I owed the debt.",
    "I am writing to dispute the information in my file. I contacted this "
    "agency to advise it to stop calling me because this case was dismissed "
    "in court in 2014.",
    "I have not had a phone since early 2007. I have tried to resolve my "
    "bill in the past but it keeps reposting an old bill.",
    "I posted-dated a check for my mortgage payment, but the check was "
    "cashed early, which cost me overdraft fees with my bank.",
]

recipes = [
    "Bake in the preheated oven, stirring every 20 minutes, until sugar "
    "mixture has baked and caramelized onto popcorn and cashews.",
    "Combine brown sugar, corn syrup, butter, salt, and cream of tartar "
    "in a large saucepan. Bring to a boil, stirring constantly.",
    "Lift marshmallow fudge out of the pan. Dip a knife in confectioners' "
    "sugar and slice fudge into squares.",
    "Melt butter in a medium saucepan over medium heat. Stir in condensed "
    "milk and chocolate chips until melted.",
    "Lightly grease a cookie sheet. Roll the marzipan into a rope and place "
    "it in the center of the dough.",
    "In a large bowl, cream together the butter and sugars. Stir in the eggs, "
    "vanilla, flour mixture, chocolate chips, and nuts.",
]

nlp_medium = spacy.load("en_core_web_md")

print("Using en_core_web_md")
print_word_similarities(nlp_medium)
print_token_similarities(nlp_medium)
print_sentence_similarities(nlp_medium)
print_document_similarities(complaints, nlp_medium, "Complaint similarities:")
print_document_similarities(recipes, nlp_medium, "Recipe similarities:")
print_cross_collection_similarities(recipes, complaints, nlp_medium)

# An additional example: related animals should be more similar than an animal
# and an unrelated vehicle when the model has meaningful word vectors.
print("Additional example using en_core_web_md:")
print(f"dog and cat: {nlp_medium('dog').similarity(nlp_medium('cat')):.4f}")
print(f"dog and boat: {nlp_medium('dog').similarity(nlp_medium('boat')):.4f}")
print()

nlp_small = spacy.load("en_core_web_sm")

print("Using en_core_web_sm")
print_word_similarities(nlp_small)

# Observation: with en_core_web_md, cat and monkey (0.3945) and monkey and
# banana (0.3741) are more similar than cat and banana (0.2334). This makes
# sense because cats and monkeys are both animals, while monkeys are commonly
# associated with bananas. In my own example, dog and cat are more similar
# than dog and boat because dogs and cats are both animals.
#
# When using en_core_web_sm, the similarity scores are noticeably different.
# For example, cat and monkey increased from 0.3945 to 0.5401, while cat and
# banana increased from 0.2334 to 0.5966. This happens because en_core_web_sm
# does not contain word vectors. Therefore, its similarity scores are based
# on other linguistic information and may be less useful for judging semantic
# similarity. The en_core_web_md model contains word vectors and is therefore
# better suited for this type of semantic similarity task.