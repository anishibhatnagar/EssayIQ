from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import textstat
from collections import Counter

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "EssayIQ Backend is running!"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/analyze", methods=["POST"])
def analyze_essay():
    data = request.get_json()

    if not data or not data.get("essay"):
        return jsonify({
            "error": "Essay text is required"
        }), 400

    essay = data["essay"].strip()

    # -----------------------------
    # Word Analysis
    # -----------------------------

    words = re.findall(r"\b[a-zA-Z]+\b", essay)
    word_count = len(words)

    # -----------------------------
    # Sentence Analysis
    # -----------------------------

    sentences = re.split(r"[.!?]+", essay)
    sentences = [s.strip() for s in sentences if s.strip()]

    sentence_count = len(sentences)

    # -----------------------------
    # Paragraph Analysis
    # -----------------------------

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", essay)
        if p.strip()
    ]

    paragraph_count = len(paragraphs)

    # -----------------------------
    # Average Sentence Length
    # -----------------------------

    if sentence_count > 0:
        average_sentence_length = round(
            word_count / sentence_count, 2
        )
    else:
        average_sentence_length = 0

    # -----------------------------
    # Vocabulary Diversity
    # -----------------------------

    lowercase_words = [word.lower() for word in words]

    unique_words = set(lowercase_words)

    if word_count > 0:
        vocabulary_diversity = round(
            len(unique_words) / word_count * 100,
            2
        )
    else:
        vocabulary_diversity = 0

    # -----------------------------
    # Repeated Words
    # -----------------------------

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "to", "of", "and", "in", "on", "for", "with",
        "that", "this", "it", "as", "be", "by", "or",
        "from", "at", "which", "but", "can", "will",
        "has", "have", "had", "their", "they", "them"
    }

    meaningful_words = [
        word for word in lowercase_words
        if word not in stop_words
    ]

    word_frequency = Counter(meaningful_words)

    repeated_words = [
        {
            "word": word,
            "count": count
        }
        for word, count in word_frequency.most_common(10)
        if count > 2
    ]

    # -----------------------------
    # Readability
    # -----------------------------

    readability_score = round(
        textstat.flesch_reading_ease(essay),
        2
    )

    # Keep readability within 0-100
    readability_score = max(
        0,
        min(100, readability_score)
    )

    # -----------------------------
    # Sentence Length Score
    # -----------------------------

    if 12 <= average_sentence_length <= 22:
        sentence_score = 100
    elif 8 <= average_sentence_length <= 30:
        sentence_score = 85
    elif 5 <= average_sentence_length <= 35:
        sentence_score = 70
    else:
        sentence_score = 55

    # -----------------------------
    # Vocabulary Score
    # -----------------------------

    if vocabulary_diversity >= 60:
        vocabulary_score = 100
    elif vocabulary_diversity >= 50:
        vocabulary_score = 90
    elif vocabulary_diversity >= 40:
        vocabulary_score = 80
    elif vocabulary_diversity >= 30:
        vocabulary_score = 70
    else:
        vocabulary_score = 60

    # -----------------------------
    # Overall Score
    # -----------------------------

    overall_score = round(
        (
            readability_score * 0.35
            + sentence_score * 0.25
            + vocabulary_score * 0.40
        ),
        2
    )

    # -----------------------------
    # Feedback
    # -----------------------------

    strengths = []
    improvements = []

    if readability_score >= 70:
        strengths.append(
            "The essay has good readability."
        )
    else:
        improvements.append(
            "Try using shorter and clearer sentences."
        )

    if vocabulary_score >= 80:
        strengths.append(
            "The essay demonstrates good vocabulary diversity."
        )
    else:
        improvements.append(
            "Try using a wider range of vocabulary."
        )

    if sentence_score >= 80:
        strengths.append(
            "Sentence length is generally well balanced."
        )
    else:
        improvements.append(
            "Some sentences may be too short or too long."
        )

    if paragraph_count >= 3:
        strengths.append(
            "The essay has a reasonable paragraph structure."
        )
    else:
        improvements.append(
            "Consider organizing the essay into more paragraphs."
        )

    return jsonify({
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "average_sentence_length": average_sentence_length,
        "vocabulary_diversity": vocabulary_diversity,
        "readability_score": readability_score,
        "sentence_score": sentence_score,
        "vocabulary_score": vocabulary_score,
        "overall_score": overall_score,
        "repeated_words": repeated_words,
        "strengths": strengths,
        "improvements": improvements
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)