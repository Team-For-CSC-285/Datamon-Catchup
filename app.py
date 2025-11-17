
# app.py — Datamon segmented Flask API

from __future__ import annotations
from flask import Flask, request, jsonify
import random

# Your existing modules
from math_checker import MathChecker
from number_guesser import NumberGuesser  
from memory_bank import MemoryBank


# ---------------- Player ----------------
def new_player(name: str = "API_Player"):
    return {
        "name": name,
        "answer_checker": [],
        "score_answer_checker": 0,
        "memory_bank": [],
        "score_memory_bank": 0,
        "number_guesser": [],
        "score_number_guesser": 0,
    }


player = new_player()

app = Flask(__name__)


# ======================================================
# MATH CHECKER: RANDOM PROBLEM + CHECK
# ======================================================

def generate_problem():
    """Return a random arithmetic problem and its correct answer."""
    a = random.randint(0, 20)
    b = random.randint(0, 20)
    op = random.choice(["+", "-", "*"])

    if op == "-" and b > a:
        a, b = b, a

    if op == "+":
        correct = a + b
    elif op == "-":
        correct = a - b
    else:
        correct = a * b

    return f"{a} {op} {b}", correct


@app.route("/math/problem", methods=["GET"])
def math_problem():
    problem, _ = generate_problem()
    return jsonify({
        "problem": problem,
        "hint": "Solve the expression"
    })


@app.route("/math/check", methods=["POST"])
def math_check():
    data = request.get_json(force=True)
    problem = data.get("problem", "")
    answer_raw = data.get("answer", None)

    # Parse "A op B"
    try:
        a_str, op, b_str = problem.split()
        a = float(a_str)
        b = float(b_str)
    except Exception:
        return jsonify({"error": "Invalid problem format"}), 400

    # Compute correct answer
    if op == "+":
        correct_answer = a + b
    elif op == "-":
        correct_answer = a - b
    elif op == "*":
        correct_answer = a * b
    else:
        return jsonify({"error": f"Unsupported operator '{op}'"}), 400

    # Parse user answer
    try:
        user_answer = float(answer_raw)
    except Exception:
        return jsonify({"error": "Answer must be numeric"}), 400

    is_correct = (user_answer == correct_answer)

    # Log attempt in a simple schema
    player.setdefault("answer_checker", []).append({
        "problem": problem,
        "user_answer": str(user_answer),
        "correct_answer": str(correct_answer),
        "correct": is_correct,
    })
    if is_correct:
        player["score_answer_checker"] = player.get("score_answer_checker", 0) + 1

    return jsonify({
        "problem": problem,
        "your_answer": user_answer,
        "correct_answer": correct_answer,
        "correct": is_correct,
        "score_answer_checker": player["score_answer_checker"],
    })


# ======================================================
# NUMBER GUESSER: SIMPLE API
# ======================================================

secret_game = {"value": None, "range": (1, 20)}


@app.route("/number/start", methods=["GET"])
def ng_start():
    lo, hi = secret_game["range"]
    secret_game["value"] = random.randint(lo, hi)
    return jsonify({
        "message": "Number Guesser started",
        "range": secret_game["range"]
    })


@app.route("/number/guess", methods=["POST"])
def ng_guess():
    data = request.get_json(force=True)
    guess = int(data.get("guess", 0))
    if secret_game["value"] is None:
        return jsonify({"error": "Start the game first at /number/start"}), 400

    secret = secret_game["value"]
    if guess == secret:
        player["score_number_guesser"] += 50
        return jsonify({"correct": True, "points": 50})
    else:
        return jsonify({
            "correct": False,
            "hint": "higher" if guess < secret else "lower"
        })


# ======================================================
# MEMORY BANK: USES memory_bank.py
# ======================================================

@app.route("/memory/problems/<name>", methods=["GET"])
def mb_get(name):
    mb = MemoryBank(MemoryBankConfig(data_path="Data.txt"))
    problems = mb.get_student_problems(name)
    return jsonify(problems)


@app.route("/memory/submit", methods=["POST"])
def mb_submit():
    data = request.get_json(force=True)
    student = data.get("student", "")
    answers = data.get("answers", [])

    mb = MemoryBank(MemoryBankConfig(data_path="Data.txt"))
    problems = mb.get_student_problems(student)

    score = 0
    graded = []

    for ans, q in zip(answers, problems):
        correct = str(ans).lower() == q["answer"].lower()
        if correct:
            score += 1
        graded.append({
            "problem": q["problem"],
            "your_answer": ans,
            "correct_answer": q["answer"],
            "correct": correct
        })

    player["score_memory_bank"] += score

    return jsonify({
        "student": student,
        "score": score,
        "results": graded
    })


# ======================================================
# HUD (simple status screen)
# ======================================================

@app.route("/hud")
def hud():
    return f"""
    <html>
    <body style='background:black;color:#00FF00;font-family:monospace;padding:20px;'>
      <h1>Datamon HUD</h1>
      <p>Player: {player['name']}</p>
      <p>MathChecker Score: {player['score_answer_checker']}</p>
      <p>NumberGuesser Score: {player['score_number_guesser']}</p>
      <p>MemoryBank Score: {player['score_memory_bank']}</p>
    </body>
    </html>
    """


# ======================================================
# MATH CHECKER WEB UI (/play)
# ======================================================

@app.route("/play", methods=["GET"])
def play_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Datamon — Math Checker</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
          background: #0f172a;
          color: #e5e7eb;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 16px;
        }
        h1 { margin-bottom: 8px; }
        .card {
          background: #111827;
          padding: 24px 20px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0,0,0,.5);
          max-width: 420px;
          width: 100%;
        }
        button {
          padding: 8px 14px;
          border-radius: 999px;
          border: none;
          cursor: pointer;
          font-weight: 600;
          margin: 4px 4px 10px 0;
          background: #22c55e;
          color: #020817;
        }
        button.secondary {
          background: #374151;
          color: #e5e7eb;
        }
        input {
          padding: 8px 10px;
          border-radius: 10px;
          border: 1px solid #4b5563;
          background: #020817;
          color: #e5e7eb;
          width: 120px;
          margin-right: 8px;
        }
        .problem { font-size: 1.4rem; margin: 10px 0 6px; }
        .status { margin-top: 6px; min-height: 22px; }
        .score  { margin-top: 10px; font-size: .9rem; color: #9ca3af; }
      </style>
    </head>
    <body>
      <h1>Datamon — Math Checker</h1>
      <p>Practice +, −, × problems powered by your Flask API.</p>

      <div class="card">
        <button id="new-problem">🎲 New Problem</button>
        <div id="problem" class="problem">Click "New Problem" to start.</div>

        <div>
          <input id="answer" type="number" placeholder="Your answer" />
          <button id="submit" class="secondary">Check</button>
        </div>

        <div id="status" class="status"></div>
        <div id="score" class="score"></div>
      </div>

      <script>
        let currentProblem = null;

        async function fetchProblem() {
          const res = await fetch("/math/problem");
          const data = await res.json();
          currentProblem = data.problem;
          document.getElementById("problem").textContent = "Problem: " + data.problem;
          document.getElementById("status").textContent = "";
          document.getElementById("answer").value = "";
        }

        async function submitAnswer() {
          if (!currentProblem) {
            document.getElementById("status").textContent = "Get a problem first.";
            return;
          }
          const val = document.getElementById("answer").value;
          if (val === "") {
            document.getElementById("status").textContent = "Type an answer first.";
            return;
          }

          const res = await fetch("/math/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              problem: currentProblem,
              answer: Number(val)
            })
          });

          const data = await res.json();

          if (data.correct) {
            document.getElementById("status").textContent = "✅ Correct!";
          } else {
            document.getElementById("status").textContent =
              "❌ Incorrect. Correct answer: " + data.correct_answer;
          }

          if (typeof data.score_answer_checker !== "undefined") {
            document.getElementById("score").textContent =
              "Score: " + data.score_answer_checker;
          }

          await fetchProblem();
        }

        document.getElementById("new-problem").addEventListener("click", fetchProblem);
        document.getElementById("submit").addEventListener("click", submitAnswer);

        // Load initial problem
        fetchProblem();
      </script>
    </body>
    </html>
    """


# ======================================================
# NUMBER GUESSER WEB UI (/play-number)
# ======================================================

@app.route("/play-number", methods=["GET"])
def play_number_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Datamon — Number Guesser</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
          background: #020617;
          color: #e5e7eb;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 16px;
        }
        h1 { margin-bottom: 8px; }
        .card {
          background: #0f172a;
          padding: 20px 18px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0,0,0,.4);
          max-width: 400px;
          width: 100%;
        }
        button {
          padding: 8px 14px;
          border-radius: 999px;
          border: none;
          cursor: pointer;
          font-weight: 600;
          margin: 4px 4px 10px 0;
          background: #22c55e;
          color: #020617;
        }
        button.secondary {
          background: #374151;
          color: #e5e7eb;
        }
        input {
          padding: 8px 10px;
          border-radius: 10px;
          border: 1px solid #4b5563;
          background: #020817;
          color: #e5e7eb;
          width: 120px;
          margin-right: 8px;
        }
        .status { margin-top: 8px; min-height: 22px; }
        .range  { font-size: 0.9rem; color: #9ca3af; margin-bottom: 8px; }
      </style>
    </head>
    <body>
      <h1>Datamon — Number Guesser</h1>
      <p>Guess the secret number and earn points.</p>

      <div class="card">
        <button id="start">🎯 Start Game</button>
        <div id="range" class="range"></div>

        <div>
          <input id="guess" type="number" placeholder="Your guess" />
          <button id="submit" class="secondary">Guess</button>
        </div>

        <div id="status" class="status"></div>
      </div>

      <script>
        let gameActive = false;

        async function startGame() {
          const res = await fetch("/number/start");
          const data = await res.json();
          gameActive = true;
          document.getElementById("range").textContent =
            "Range: " + data.range[0] + " to " + data.range[1];
          document.getElementById("status").textContent = "Game started. Make a guess!";
        }

        async function submitGuess() {
          if (!gameActive) {
            document.getElementById("status").textContent = "Start the game first.";
            return;
          }
          const val = document.getElementById("guess").value;
          if (val === "") {
            document.getElementById("status").textContent = "Enter a guess.";
            return;
          }

          const res = await fetch("/number/guess", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ guess: Number(val) })
          });
          const data = await res.json();

          if (data.error) {
            document.getElementById("status").textContent = "Error: " + data.error;
            return;
          }

          if (data.correct) {
            document.getElementById("status").textContent =
              "✅ Correct! You earned " + data.points + " points. Start again for a new number.";
            gameActive = false;
          } else {
            document.getElementById("status").textContent =
              "❌ Nope, try " + data.hint + ".";
          }
        }

        document.getElementById("start").addEventListener("click", startGame);
        document.getElementById("submit").addEventListener("click", submitGuess);
      </script>
    </body>
    </html>
    """


# ======================================================
# MEMORY BANK WEB QUIZ (/memory/play)
# ======================================================

@app.route("/memory/play", methods=["GET"])
def memory_play_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Datamon — Memory Bank</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
          background: #020617;
          color: #e5e7eb;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 16px;
        }
        h1 { margin-bottom: 8px; }
        .card {
          background: #0f172a;
          padding: 20px 18px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0,0,0,.4);
          max-width: 520px;
          width: 100%;
        }
        label { font-size: 0.9rem; }
        input[type="text"], input[type="number"] {
          padding: 8px 10px;
          border-radius: 10px;
          border: 1px solid #4b5563;
          background: #020817;
          color: #e5e7eb;
          width: 100%;
          margin: 4px 0 10px;
        }
        button {
          padding: 8px 14px;
          border-radius: 999px;
          border: none;
          cursor: pointer;
          font-weight: 600;
          margin: 4px 4px 10px 0;
          background: #22c55e;
          color: #020617;
        }
        button.secondary {
          background: #374151;
          color: #e5e7eb;
        }
        .question {
          margin-top: 10px;
          padding-top: 8px;
          border-top: 1px solid #1f2937;
        }
        .status { margin-top: 8px; min-height: 22px; }
        .score  { margin-top: 10px; font-size: 0.9rem; color: #9ca3af; }
      </style>
    </head>
    <body>
      <h1>Datamon — Memory Bank</h1>
      <p>Enter the student's name, load their questions, and submit the quiz.</p>

      <div class="card">
        <label for="student">Student Name</label>
        <input id="student" type="text" placeholder="e.g. Example" />

        <button id="load">📥 Load Questions</button>

        <div id="questions"></div>

        <button id="submit" class="secondary">✅ Submit Quiz</button>

        <div id="status" class="status"></div>
        <div id="score" class="score"></div>
      </div>

      <script>
        let currentProblems = [];

        async function loadQuestions() {
          const name = document.getElementById("student").value.trim();
          const status = document.getElementById("status");
          const questionsDiv = document.getElementById("questions");
          const scoreDiv = document.getElementById("score");
          scoreDiv.textContent = "";
          status.textContent = "";

          if (!name) {
            status.textContent = "Enter a student name first.";
            return;
          }

          const res = await fetch("/memory/problems/" + encodeURIComponent(name));
          const data = await res.json();

          if (!data || !data.length) {
            status.textContent = "No problems found for '" + name + "'.";
            questionsDiv.innerHTML = "";
            currentProblems = [];
            return;
          }

          currentProblems = data;
          questionsDiv.innerHTML = "";

          data.forEach((q, idx) => {
            const block = document.createElement("div");
            block.className = "question";
            block.innerHTML = `
              <div><strong>Q${idx + 1}:</strong> ${q.problem}</div>
              <input type="text" id="answer-${idx}" placeholder="Your answer" />
            `;
            questionsDiv.appendChild(block);
          });

          status.textContent = "Questions loaded. Fill in your answers and click Submit.";
        }

        async function submitQuiz() {
          const name = document.getElementById("student").value.trim();
          const status = document.getElementById("status");
          const scoreDiv = document.getElementById("score");

          if (!name) {
            status.textContent = "Enter a student name first.";
            return;
          }
          if (!currentProblems.length) {
            status.textContent = "Load questions first.";
            return;
          }

          const answers = currentProblems.map((_, idx) => {
            const el = document.getElementById("answer-" + idx);
            return el ? el.value : "";
          });

          const res = await fetch("/memory/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              student: name,
              answers: answers
            })
          });

          const data = await res.json();

          if (data.error) {
            status.textContent = "Error: " + data.error;
            return;
          }

          status.textContent = "Quiz submitted.";
          scoreDiv.textContent = "Score: " + data.score + " / " + currentProblems.length;
        }

        document.getElementById("load").addEventListener("click", loadQuestions);
        document.getElementById("submit").addEventListener("click", submitQuiz);
      </script>
    </body>
    </html>
    """


# ======================================================
# HOME MENU (HTML)
# ======================================================

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Datamon — Home</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
          background: #020617;
          color: #e5e7eb;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 16px;
        }
        h1 { margin-bottom: 4px; }
        p  { margin-bottom: 20px; color: #9ca3af; }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 16px;
          max-width: 800px;
          width: 100%;
        }
        .card {
          background: #0f172a;
          border-radius: 16px;
          padding: 16px 14px;
          box-shadow: 0 10px 30px rgba(0,0,0,.4);
          border: 1px solid #1f2937;
        }
        .card h2 {
          font-size: 1.1rem;
          margin-bottom: 6px;
        }
        .card p {
          margin-bottom: 12px;
          font-size: 0.9rem;
          color: #9ca3af;
        }
        a.button {
          display: inline-block;
          padding: 8px 14px;
          border-radius: 999px;
          text-decoration: none;
          font-weight: 600;
          background: #22c55e;
          color: #020617;
        }
        a.button.secondary {
          background: #374151;
          color: #e5e7eb;
        }
      </style>
    </head>
    <body>
      <h1>Datamon — Dashboard</h1>
      <p>Select a game or view your status.</p>

      <div class="grid">
        <div class="card">
          <h2>➕ Math Checker</h2>
          <p>Practice addition, subtraction, and multiplication.</p>
          <a href="/play" class="button">Open Math Checker</a>
        </div>

        <div class="card">
          <h2>🔢 Number Guesser</h2>
          <p>Guess the secret number with higher/lower hints.</p>
          <a href="/play-number" class="button">Play Number Guesser</a>
        </div>

        <div class="card">
          <h2>🧠 Memory Bank</h2>
          <p>Use parent-made questions to run a quiz.</p>
          <a href="/memory/play" class="button">Start Memory Quiz</a>
        </div>

        <div class="card">
          <h2>📟 Status HUD</h2>
          <p>View your live Datamon scores in a HUD.</p>
          <a href="/hud" class="button secondary">Open HUD</a>
        </div>
      </div>
    </body>
    </html>
    """


# ======================================================
# RUNNER
# ======================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
