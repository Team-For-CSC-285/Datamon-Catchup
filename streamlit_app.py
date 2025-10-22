
# streamlit_app.py — Full Streamlit UI for Datamon
import streamlit as st
import random, time, json, os

st.set_page_config(page_title="Datamon — Streamlit", page_icon="🧮", layout="centered")

# ---------------- Player state ----------------
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Player",
        "answer_checker": [],
        "score_answer_checker": 0,
        "number_guesser": [],
        "score_number_guesser": 0,
        "memory_bank": [],
        "score_memory_bank": 0,
    }
player = st.session_state.player

st.title("Datamon — Streamlit")
player["name"] = st.text_input("Player name", value=player["name"])

tabs = st.tabs(["➕ Math Checker", "🔢 Number Guesser", "🧠 Memory Bank", "📊 Session Summary"])

# ---------------- Helpers ----------------
def new_math_problem(op_symbol):
    lo, hi = 0, 100
    if op_symbol == "÷ (q + r)":
        b = 0
        while b == 0:
            b = random.randint(1, hi)
        a = random.randint(lo, hi)
        q, r = divmod(a, b)
        return {"op": "/", "a": a, "b": b, "answer": (q, r)}
    else:
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        if op_symbol == "+": ans = a + b
        elif op_symbol == "-": ans = a - b
        else: ans = a * b
        return {"op": {"+": "+", "-" : "-", "×": "*", "*": "*"}[op_symbol], "a": a, "b": b, "answer": ans}

def safe_load(path: str) -> dict:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def safe_save(path: str, data: dict) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

# ---------------- Math Checker ----------------
with tabs[0]:
    st.subheader("Math Checker")
    colA, colB = st.columns(2)
    with colA:
        op = st.selectbox("Operation", ["+", "-", "*", "÷ (q + r)"])
    with colB:
        total = st.number_input("Problems this round", min_value=1, max_value=50, value=5, step=1)

    if "mc" not in st.session_state:
        st.session_state.mc = None

    if st.button("Start / Reset round", key="mc_start"):
        st.session_state.mc = {"op": op, "idx": 0, "total": total, "current": new_math_problem(op)}

    mc = st.session_state.mc
    if mc:
        cur = mc["current"]
        st.write(f"**Problem {mc['idx'] + 1} of {mc['total']}**")

        if cur["op"] == "/":
            st.write(f"Solve: **{cur['a']} ÷ {cur['b']}**")
            c1, c2 = st.columns(2)
            with c1:
                q = st.number_input("Quotient", step=1, format="%d", key=f"q_{mc['idx']}")
            with c2:
                r = st.number_input("Remainder", min_value=0, step=1, format="%d", key=f"r_{mc['idx']}")

            if st.button("Submit answer", key=f"mc_submit_{mc['idx']}"):
                correct = (int(q) == cur["answer"][0] and int(r) == cur["answer"][1])
                player["answer_checker"].append({
                    "problem": f"{cur['a']} ÷ {cur['b']}",
                    "user_answer": f"q={int(q)}, r={int(r)}",
                    "correct_answer": f"q={cur['answer'][0]}, r={cur['answer'][1]}",
                    "correct": bool(correct),
                })
                if correct: player["score_answer_checker"] += 1
                st.success("Correct! 🎉") if correct else st.error("Incorrect.")
                mc["idx"] += 1
                if mc["idx"] < mc["total"]:
                    mc["current"] = new_math_problem(op)
                else:
                    st.info("Round complete!")
                    st.session_state.mc = None
        else:
            sym = cur["op"]
            st.write(f"Solve: **{cur['a']} {sym} {cur['b']}**")
            ans = st.number_input("Your answer", step=1, format="%d", key=f"ans_{mc['idx']}")

            if st.button("Submit answer", key=f"mc_submit_{mc['idx']}"):
                correct = (int(ans) == cur["answer"])
                player["answer_checker"].append({
                    "problem": f"{cur['a']} {sym} {cur['b']}",
                    "user_answer": str(int(ans)),
                    "correct_answer": str(cur["answer"]),
                    "correct": bool(correct),
                })
                if correct: player["score_answer_checker"] += 1
                st.success("Correct! 🎉") if correct else st.error("Incorrect.")
                mc["idx"] += 1
                if mc["idx"] < mc["total"]:
                    mc["current"] = new_math_problem(op)
                else:
                    st.info("Round complete!")
                    st.session_state.mc = None

    st.caption(f"Score: {player['score_answer_checker']} | Attempts: {len(player['answer_checker'])}")

# ---------------- Number Guesser ----------------
with tabs[1]:
    st.subheader("Number Guesser")
    levels = {
        "Easy":   {"range": (1,10), "tries": 5},
        "Normal": {"range": (1,50), "tries": 7},
        "Hard":   {"range": (1,100),"tries": 9},
    }
    if "ng" not in st.session_state:
        st.session_state.ng = None

    col1, col2 = st.columns(2)
    with col1:
        diff = st.selectbox("Difficulty", list(levels.keys()), index=0)
    with col2:
        if st.button("Start / Reset round", key="ng_start"):
            lo, hi = levels[diff]["range"]
            st.session_state.ng = {
                "difficulty": diff,
                "lo": lo, "hi": hi,
                "tries_total": levels[diff]["tries"],
                "tries_used": 0,
                "secret": random.randint(lo, hi),
                "guesses": [],
                "won": False,
                "points": 0,
            }

    ng = st.session_state.ng
    if ng:
        st.write(f"Guess the number between **{ng['lo']}** and **{ng['hi']}**")
        st.write(f"Attempt **{ng['tries_used'] + 1}** of **{ng['tries_total']}**")
        guess = st.number_input("Your guess", min_value=ng["lo"], max_value=ng["hi"], step=1, format="%d", key=f"g_{ng['tries_used']}")

        if st.button("Submit guess", key=f"ng_submit_{ng['tries_used']}"):
            if not (ng["won"] or ng["tries_used"] >= ng["tries_total"]):
                ng["tries_used"] += 1
                if int(guess) == ng["secret"]:
                    ng["won"] = True
                    ng["guesses"].append({"guess": int(guess), "hint": "correct"})
                    pts = max(10, 100 - 10 * (len(ng["guesses"]) - 1))
                    if len(ng["guesses"]) <= 3: pts += 20
                    ng["points"] = pts
                    st.success(f"Correct! +{pts} pts 🎉")
                    player["number_guesser"].append({
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "difficulty": ng["difficulty"],
                        "range": {"lo": ng["lo"], "hi": ng["hi"]},
                        "secret": ng["secret"],
                        "guesses": ng["guesses"],
                        "won": True,
                        "attempts_used": ng["tries_used"],
                        "points": pts,
                    })
                    player["score_number_guesser"] += pts
                else:
                    hint = "higher" if int(guess) < ng["secret"] else "lower"
                    st.info(f"Nope — try **{hint}**.")
                    ng["guesses"].append({"guess": int(guess), "hint": hint})
                    if ng["tries_used"] == ng["tries_total"]:
                        st.warning(f"Out of tries! The number was **{ng['secret']}**.")
                        player["number_guesser"].append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "difficulty": ng["difficulty"],
                            "range": {"lo": ng["lo"], "hi": ng["hi"]},
                            "secret": ng["secret"],
                            "guesses": ng["guesses"],
                            "won": False,
                            "attempts_used": ng["tries_used"],
                            "points": 0,
                        })

        if ng["guesses"]:
            st.write("**History**")
            for g in ng["guesses"]:
                st.write(f"- {g['guess']} → {g['hint']}")

    st.caption(f"Score: {player['score_number_guesser']} | Rounds: {len(player['number_guesser'])}")

# ---------------- Memory Bank ----------------
with tabs[2]:
    st.subheader("Memory Bank")
    DATA_PATH = st.text_input("Data file path", value="Data.txt", help="JSON file storing problems per student.")

    sub_tabs = st.tabs(["Parent", "Student"])

    # Parent
    with sub_tabs[0]:
        st.write("Add or clear problems per student.")
        name = st.text_input("Student name").strip().capitalize()
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            problem = st.text_input("Problem (e.g., 7 + 5)")
        with pcol2:
            answer = st.text_input("Answer (e.g., 12)")

        if st.button("Add problem"):
            data = safe_load(DATA_PATH)
            if name and problem and answer:
                data.setdefault(name, []).append({"problem": problem, "answer": answer})
                if safe_save(DATA_PATH, data):
                    st.success(f"Added for {name}.")
                else:
                    st.error("Failed to save.")
            else:
                st.warning("Fill all fields.")

        if st.button("Clear all data", type="secondary"):
            if safe_save(DATA_PATH, {}):
                st.warning("All data cleared.")
            else:
                st.error("Failed to clear.")

        st.write("**Current Data:**")
        data = safe_load(DATA_PATH)
        if data:
            for nm, arr in data.items():
                st.markdown(f"**{nm}**")
                for item in arr:
                    st.write(f"- {item['problem']} = {item['answer']}")
        else:
            st.caption("No data yet.")

    # Student
    with sub_tabs[1]:
        sname = st.text_input("Your name", key="stu_name").strip().capitalize()
        if st.button("Start quiz"):
            st.session_state.mb = {"name": sname, "idx": 0, "score": 0, "problems": safe_load(DATA_PATH).get(sname, [])}

        if "mb" in st.session_state and st.session_state.mb:
            mb = st.session_state.mb
            probs = mb["problems"]
            if not probs:
                st.info("No problems found for your name. Ask a parent to add some.")
            elif mb["idx"] >= len(probs):
                st.success(f"Finished! Score: {mb['score']} / {len(probs)}")
                if st.button("Reset quiz"):
                    st.session_state.mb = None
            else:
                q = probs[mb["idx"]]
                st.write(f"Question {mb['idx'] + 1} of {len(probs)}")
                st.write(f"**{q['problem']}**")
                ans = st.text_input("Your answer", key=f"mb_ans_{mb['idx']}")
                if st.button("Submit answer", key=f"mb_submit_{mb['idx']}"):
                    if ans.strip().lower() == str(q['answer']).strip().lower():
                        st.success("Correct!")
                        mb["score"] += 1
                    else:
                        st.error("Incorrect.")
                    mb["idx"] += 1

# ---------------- Session Summary ----------------
with tabs[3]:
    st.subheader("Session Summary")
    ac_hist = player.get("answer_checker", [])
    ng_hist = player.get("number_guesser", [])
    st.write(f"**Answer Checker** — {player.get('score_answer_checker',0)} points · {len(ac_hist)} attempts")
    for a in ac_hist[-10:]:
        mark = "✅" if a["correct"] else "❌"
        st.write(f"- {mark} {a['problem']} | you: {a['user_answer']} | correct: {a['correct_answer']}")
    st.write("---")
    st.write(f"**Number Guesser** — {player.get('score_number_guesser',0)} points · {len(ng_hist)} rounds")
    for r in ng_hist[-5:]:
        status = "WIN" if r["won"] else "LOSE"
        st.write(f"- [{status}] {r['difficulty']} {r['range']['lo']}-{r['range']['hi']} | "
                 f"used {r['attempts_used']} tries | +{r['points']} pts")
