from flask import Flask, request, jsonify

from model import predict_news
from explainability import highlight_claims, explain_claims
from source_manager import is_trusted

app = Flask(__name__)

metrics = {
    "articles_analyzed": 0
}


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    text = data["text"]
    source = data["source"]

    prediction = predict_news(text)

    suspicious = highlight_claims(text)

    explanation = explain_claims(text)

    trusted = is_trusted(source)

    metrics["articles_analyzed"] += 1

    return jsonify({
        "prediction": prediction,
        "trusted_source": trusted,
        "suspicious_phrases": suspicious,
        "explanation": explanation,
        "metrics": metrics
    })


if __name__ == "__main__":
    app.run(debug=True)
    