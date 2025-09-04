# train.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils import resample
import pickle

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("dataset/depression_dataset_reddit_cleaned.csv")

print("Before balancing:\n", df["is_depression"].value_counts())

# Balance dataset (upsample minority)
df_majority = df[df.is_depression == 0]
df_minority = df[df.is_depression == 1]

df_minority_upsampled = resample(df_minority,
                                 replace=True,
                                 n_samples=len(df_majority),
                                 random_state=42)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

print("After balancing:\n", df_balanced["is_depression"].value_counts())

# ==========================
# Train-Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    df_balanced["clean_text"], df_balanced["is_depression"],
    test_size=0.2, random_state=42
)

# ==========================
# Vectorizer + Model
# ==========================
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=200)
model.fit(X_train_tfidf, y_train)

# ==========================
# Evaluation
# ==========================
y_pred = model.predict(X_test_tfidf)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ==========================
# Save Model + Vectorizer
# ==========================
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved!")
