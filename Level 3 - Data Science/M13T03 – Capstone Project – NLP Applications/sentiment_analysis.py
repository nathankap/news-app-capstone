"""
Sentiment Analysis on Amazon Product Reviews.

This script performs sentiment analysis and semantic similarity on the
Datafiniti Amazon Consumer Reviews dataset using spaCy and spacytextblob.
"""

import os
import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


def load_spacy_model() -> spacy.language.Language:
    """
    Load the spaCy medium English pipeline and add SpacyTextBlob component.

    Returns:
        spacy.language.Language: The initialized spaCy NLP pipeline.
    """
    nlp = spacy.load("en_core_web_md")
    if "spacytextblob" not in nlp.pipe_names:
        nlp.add_pipe("spacytextblob")
    return nlp


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the Amazon product reviews dataset from a CSV file.

    Args:
        file_path (str): Relative or absolute path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    return pd.read_csv(file_path)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the 'reviews.text' column and drop any missing or null values.

    Args:
        df (pd.DataFrame): Raw dataset.

    Returns:
        pd.DataFrame: Cleaned DataFrame with non-null reviews.
    """
    clean_data = df.dropna(subset=["reviews.text"]).copy()
    return clean_data


def preprocess_text(text: str, nlp: spacy.language.Language) -> str:
    """
    Preprocess raw review text by standardizing casing, stripping whitespace,
    and removing stopwords and punctuation using spaCy token attributes.

    Args:
        text (str): Raw review text.
        nlp (spacy.language.Language): Loaded spaCy NLP pipeline.

    Returns:
        str: Cleaned review string with stopwords and punctuation removed.
    """
    cleaned_string = str(text).lower().strip()
    doc = nlp(cleaned_string)
    filtered_tokens = [
        token.text
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(filtered_tokens)


def analyze_sentiment(review_text: str, nlp: spacy.language.Language) -> dict:
    """
    Predict the sentiment, polarity, and subjectivity of a product review.

    Args:
        review_text (str): Product review text.
        nlp (spacy.language.Language): spaCy pipeline with spacytextblob.

    Returns:
        dict: Sentiment label, polarity score, and subjectivity score.
    """
    cleaned_text = preprocess_text(review_text, nlp)
    doc = nlp(cleaned_text if cleaned_text else review_text)

    polarity = doc._.blob.polarity
    subjectivity = doc._.blob.subjectivity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "cleaned_text": cleaned_text,
    }


def compare_review_similarity(
    review_a: str, review_b: str, nlp: spacy.language.Language
) -> float:
    """
    Compare the semantic similarity between two reviews using spaCy word vectors.

    Args:
        review_a (str): First review text.
        review_b (str): Second review text.
        nlp (spacy.language.Language): spaCy NLP pipeline.

    Returns:
        float: Similarity score between 0.0 and 1.0.
    """
    doc_a = nlp(review_a)
    doc_b = nlp(review_b)
    return doc_a.similarity(doc_b)


def main() -> None:
    """Main execution function for sentiment analysis and testing."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_file = "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv"
    dataset_path = os.path.join(current_dir, dataset_file)

    if not os.path.exists(dataset_path):
        dataset_path = dataset_file

    print("=" * 70)
    print("STEP 1 & 3.1: Loading spaCy Model (en_core_web_md)...")
    print("=" * 70)
    nlp = load_spacy_model()
    print("spaCy model and SpacyTextBlob pipeline loaded successfully.")

    print("\n" + "=" * 70)
    print("STEP 2 & 3.2: Loading and Preprocessing Dataset...")
    print("=" * 70)
    raw_df = load_dataset(dataset_path)
    print(f"Dataset loaded: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns.")

    clean_df = preprocess_dataframe(raw_df)
    reviews_data = clean_df["reviews.text"]
    print(f"Cleaned dataset rows after removing missing values: {len(reviews_data)}")

    print("\n" + "=" * 70)
    print("STEP 3.3 & 3.4: Testing Model on Sample Product Reviews...")
    print("=" * 70)

    sample_indices = [0, 15, 64, 110, 245]
    for idx in sample_indices:
        if idx < len(reviews_data):
            raw_review = clean_df.iloc[idx]["reviews.text"]
            rating = clean_df.iloc[idx].get("reviews.rating", "N/A")
            result = analyze_sentiment(raw_review, nlp)

            print(f"\n[Sample Review #{idx}] (Actual Rating: {rating}/5)")
            print(f"Original Text : {raw_review[:120]}...")
            print(f"Cleaned Text  : {result['cleaned_text'][:120]}...")
            print(f"Sentiment     : {result['sentiment']}")
            print(f"Polarity      : {result['polarity']:.4f} (-1 to 1)")
            print(f"Subjectivity  : {result['subjectivity']:.4f} (0 to 1)")

    print("\n" + "=" * 70)
    print("STEP 3.5: Testing Semantic Similarity Between Two Reviews...")
    print("=" * 70)
    review_choice_1 = clean_df.iloc[0]["reviews.text"]
    review_choice_2 = clean_df.iloc[1]["reviews.text"]
    review_choice_3 = clean_df.iloc[15]["reviews.text"]

    sim_1_2 = compare_review_similarity(review_choice_1, review_choice_2, nlp)
    sim_1_3 = compare_review_similarity(review_choice_1, review_choice_3, nlp)

    print(f"\nReview A (Index 0) : {review_choice_1}")
    print(f"Review B (Index 1) : {review_choice_2}")
    print(f"Similarity Score (A vs B): {sim_1_2:.4f}")

    print(f"\nReview C (Index 15): {review_choice_3}")
    print(f"Similarity Score (A vs C): {sim_1_3:.4f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
