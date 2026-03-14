import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

dataset = pd.read_csv("data/dataset.csv")

dataset.columns = dataset.columns.str.strip()

texts = dataset["text"]
labels = dataset["label"]

vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)


def predict_news(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    probability = model.predict_proba(text_vector).max()
    return {
        "prediction": prediction,
        "confidence": round(float(probability), 2)
    }