import pickle

# Load saved model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict_depression(text):
    # Convert input text to TF-IDF features
    text_tfidf = vectorizer.transform([text])
    
    # Predict
    prediction = model.predict(text_tfidf)[0]
    
    if prediction == 1:
        return "⚠️ Depressed"
    else:
        return "✅ Not Depressed"

if __name__ == "__main__":
    # Example inputs
    while True:
        user_input = input("\nEnter a social media post (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        result = predict_depression(user_input)
        print("Prediction:", result)
