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
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    text = data.get("text", "").strip()
    source = data.get("source", "").strip()

    if not text:
        return jsonify({"error": "Field 'text' is required and cannot be empty"}), 400
    try:
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

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)  