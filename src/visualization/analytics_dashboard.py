import os
import re
from collections import Counter

import matplotlib.pyplot as plt


# =========================
# LOAD ALL TEXT FILES
# =========================

def load_all_text():

    extracted_folder = "data/extracted_text"

    combined_text = ""

    for file in os.listdir(extracted_folder):

        if file.endswith(".txt"):

            file_path = os.path.join(
                extracted_folder,
                file
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                combined_text += f.read() + " "

    return combined_text


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):

    # lowercase
    text = text.lower()

    # remove urls
    text = re.sub(
        r'http\S+',
        '',
        text
    )

    # keep only letters and spaces
    text = re.sub(
        r'[^a-zA-Z\s]',
        ' ',
        text
    )

    # remove extra spaces
    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    # remove giant broken words
    words = text.split()

    cleaned_words = [
        word for word in words
        if len(word) < 20
    ]

    cleaned_text = " ".join(cleaned_words)

    return cleaned_text


# =========================
# KEYWORD EXTRACTION
# =========================

def extract_keywords(text):

    stopwords = {
        "the", "and", "of", "to", "in", "a",
        "for", "is", "on", "that", "with",
        "as", "are", "this", "by", "an",
        "be", "from", "or", "at", "we",
        "can", "our", "their", "these",
        "using", "used", "have", "has",
        "were", "which", "also", "such",
        "into", "than", "them", "they",
        "will", "been", "more", "other",
        "some", "many", "most"
    }

    words = text.split()

    filtered_words = [
        word for word in words
        if word not in stopwords
        and len(word) > 3
    ]

    keyword_counts = Counter(filtered_words)

    return keyword_counts.most_common(10)


# =========================
# CREATE CHART
# =========================

def create_chart(keywords):

    labels = [
        item[0]
        for item in keywords
    ]

    counts = [
        item[1]
        for item in keywords
    ]

    plt.figure(figsize=(12, 6))

    plt.bar(labels, counts)

    plt.xlabel("Keywords")

    plt.ylabel("Frequency")

    plt.title("Top Research Keywords")

    plt.xticks(rotation=45)

    os.makedirs(
        "visualizations",
        exist_ok=True
    )

    output_path = (
        "visualizations/keyword_analysis.png"
    )

    plt.tight_layout()

    plt.savefig(output_path)

    print("\nVisualization saved successfully!")
    print(f"Saved at: {output_path}")


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    print("\nLoading research papers...\n")

    text = load_all_text()

    print("Cleaning text...\n")

    cleaned_text = clean_text(text)

    print("Extracting keywords...\n")

    keywords = extract_keywords(cleaned_text)

    print("Top Keywords:\n")

    for keyword, count in keywords:

        print(f"{keyword}: {count}")

    create_chart(keywords)