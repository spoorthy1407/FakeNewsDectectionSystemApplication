import re

suspicious_patterns = {
    "miracle cure": "Miracle cures are often misinformation.",
    "doctors hate": "Clickbait health claim pattern.",
    "secret trick": "Unverified secret method claim.",
    "100% guaranteed": "Unrealistic promise often used in scams.",
    "big pharma": "Conspiracy narrative."
}


def highlight_claims(text):

    found = []

    for pattern in suspicious_patterns:

        if re.search(pattern, text.lower()):
            found.append(pattern)

    return found

def explain_claims(text):

    explanations = []

    for pattern in suspicious_patterns:

        if re.search(pattern, text.lower()):
            explanations.append(suspicious_patterns[pattern])

    return explanations
