"""Movie Recommendation System using spaCy's semantic similarity model.

This module reads movie descriptions from a text file and recommends the most
similar movie based on a user's target description (e.g. Planet Hulk).
"""

from pathlib import Path
import spacy

# Load spaCy's medium English model, which includes word vectors
nlp = spacy.load("en_core_web_md")

DEFAULT_MOVIES_PATH = Path(__file__).parent / "movies.txt"


def load_movies(file_path=DEFAULT_MOVIES_PATH):
    """Reads movie titles and descriptions from a text file.

    Parameters:
        file_path (str or Path): Path to the text file containing movie data.

    Returns:
        dict: A dictionary mapping movie titles (str) to descriptions (str).
    """
    movies = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                title, description = line.split(":", 1)
                movies[title.strip()] = description.strip()
    return movies


def recommend_movie(description, movies_file=DEFAULT_MOVIES_PATH):
    """Finds and returns the title of the movie most similar to the description.

    Parameters:
        description (str): Description of the movie watched by the user.
        movies_file (str or Path): Path to the text file containing candidate movies.

    Returns:
        str: Title of the movie with the highest semantic similarity score.
    """
    movies = load_movies(movies_file)
    target_doc = nlp(description)

    most_similar_title = None
    highest_similarity = -1.0

    print("--- Semantic Similarity Scores ---")
    for title, movie_desc in movies.items():
        doc = nlp(movie_desc)
        similarity = target_doc.similarity(doc)
        print(f"{title}: {similarity:.4f}")

        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_title = title

    print(f"\nHighest Similarity Score: {highest_similarity:.4f}")
    return most_similar_title


if __name__ == "__main__":
    planet_hulk_description = (
        "Will he save their world or destroy it? When the Hulk becomes too "
        "dangerous for the Earth, the Illuminati trick Hulk into a shuttle and "
        "launch him into space to a planet where the Hulk can live in peace. "
        "Unfortunately, Hulk lands on the planet Sakaar where he is sold into "
        "slavery and trained as a gladiator."
    )

    recommended = recommend_movie(planet_hulk_description)
    print(f"\nRecommended Movie to Watch Next: {recommended}")
