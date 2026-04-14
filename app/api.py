"""
RESTful API implementation using Flask.
"""

from flask import Flask, request, jsonify
from app.database import init_db, add_score, get_top_scorers, get_score_by_name
from app.auth import require_api_key

app = Flask(__name__)

@app.before_request
def setup():
    init_db()


@app.route("/scores", methods=["POST"])
@require_api_key
def post_score():
    """Endpoint: Saves a new test score to the database."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    first_name  = data.get("first_name", "").strip()
    second_name = data.get("second_name", "").strip()
    score       = data.get("score")

# Validate presence of required name fields and score
    if not first_name or not second_name:
        return jsonify({"error": "first_name and second_name are required."}), 400

    if score is None or not isinstance(score, int):
        return jsonify({"error": "score must be an integer."}), 400

    if score < 0 or score > 100:
        return jsonify({"error": "score must be between 0 and 100."}), 400

    record = add_score(first_name, second_name, score)
    return jsonify({"message": "Score added successfully.", "data": record}), 201


@app.route("/scores/top", methods=["GET"])
@require_api_key
def top_scores():
    scorers, max_score = get_top_scorers()

    if not scorers:
        return jsonify({"message": "No scores found."}), 404

    return jsonify({
        "top_score": max_score,
        "top_scorers": [s["full_name"] for s in scorers],
    }), 200


@app.route("/scores", methods=["GET"])
@require_api_key
def get_score():
    first_name  = request.args.get("first_name", "").strip()
    second_name = request.args.get("second_name", "").strip()

    if not first_name or not second_name:
        return jsonify({"error": "Provide both first_name and second_name as query params."}), 400

    result = get_score_by_name(first_name, second_name)

    if result is None:
        return jsonify({"error": f"No record found for {first_name} {second_name}."}), 404

    return jsonify(result), 200