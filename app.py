# app.py
# Minimal Datamon Flask API (bare-bones)

from flask import Flask, request, jsonify
import random

from math_checker import MathChecker, MathCheckerConfig

app = Flask(__name__)

# ---------------- Basic Datamon-style state ----------------

# Single in-memory player for now (bare minimum)
player = {
    "name": "API_Player",
    "answer_checker": [],
    "score_answer_checker": 0
}

# Use MathChecker only for logging format + helpers
mc = MathChecker(MathCheckerConfig(
    min_num=0,
    max_num=100,
    retries=0,                     # no retries in API version
    nonnegative_remainder=True,
    clear_between_screens=False,
    debug=False,
    input_fn=lambda _="": "",      # not used in API
    print_fn=lambda *_, **__: None # silence prints
))

# ---------------- Helpers ----------------

def generate_problem():
    """
    Minimal: random +,-,* problem.
    """
    a = random.randint(0, 20)
    b = random.randint(0, 20)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        correct = a + b
    elif op == "-":
        # keep non-negative
        if b > a:
            a, b = b, a
        correct = a - b
    else:
        correct = a * b

    return f"{a} {op} {b}", correct


def parse_problem(problem: str):
    parts = problem.split()
    if len(parts) != 3:
        raise ValueError("Expected format like '10 + 5'.")
    a_str, op, b_str = parts
    a = float(a_str)
    b = float(b_str)
    return a, op, b

# ---------------- Routes ----------------

@app.route("/", methods=["GET"])
def home():
    # Simple "it works" endpoint
    return jsonify({
        "message": "Datamon minimal Flask API is running.",
        "hint": "GET /math/problem for a problem, POST /math/check to verify."
    })


@app.route("/math/problem", methods=["GET"])
def math_problem():
    """
    Returns one random problem, no answer.
    """
    problem, _ = generate_problem()
    return jsonify({
        "player": player["name"],
        "problem": problem
    })


@app.route("/math/check", methods=["POST"])
def math_check():
    """
    Check an answer.

    JSON body:
    {
      "problem": "10 * 5",
      "answer": 50
    }
    """
    data = request.get_json(silent=True) or {}
    problem = str(data.get("problem", "")).strip()
    answer_raw = data.get("answer", None)

    if not problem:
        return jsonify({"error": "Missing 'problem'."}), 400
    if answer_raw is None:
        return jsonify({"error": "Missing 'answer'."}), 400

    # Parse the problem
    try:
        a, op, b = parse_problem(problem)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Only support +, -, * in this bare-min version
    if op == "+":
        correct_answer = a + b
    elif op == "-":
        correct_answer = a - b
    elif op == "*":
        correct_answer = a * b
    else:
        return jsonify({"error": f"Unsupported operator '{op}'. Use +, -, *."}), 400

    # Coerce user answer to float
    try:
        user_answer = float(answer_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Answer must be numeric."}), 400

    is_correct = (user_answer == correct_answer)

    # Log using MathChecker schema
    mc._record_attempt(
        player=player,
        problem_str=problem,
        user_str=str(user_answer),
        correct_str=str(correct_answer),
        is_correct=is_correct
    )

    return jsonify({
        "player": player["name"],
        "problem": problem,
        "your_answer": user_answer,
        "correct_answer": correct_answer,
        "correct": is_correct,
        "score_answer_checker": player["score_answer_checker"]
    })


# ---------------- Entrypoint ----------------

if __name__ == "__main__":
    app.run(debug=True)
