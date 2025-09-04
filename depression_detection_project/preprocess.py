import pandas as pd
import re
import string
import os

# File path
DATA_PATH = "dataset/depression_dataset_reddit_cleaned.csv"

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove extra spaces
    text = text.strip()
    return text

def load_and_preprocess():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Check columns
    if not {'clean_text', 'is_depression'}.issubset(df.columns):
        raise ValueError("Dataset must contain 'clean_text' and 'is_depression' columns")

    # Keep only required columns
    df = df[['clean_text', 'is_depression']]

    # Clean text
    df['clean_text'] = df['clean_text'].astype(str).apply(clean_text)

    # Save processed dataset
    processed_path = "dataset/processed_depression.csv"
    os.makedirs("dataset", exist_ok=True)
    df.to_csv(processed_path, index=False)

    print(f"✅ Preprocessing complete. Saved at: {processed_path}")
    print(df.head())
    return processed_path

if __name__ == "__main__":
    load_and_preprocess()
