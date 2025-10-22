# -*- coding: utf-8 -*-
"""
Datamon — VS Code Launcher (rewired UI)
- Clean main menu + Math Checker submenu
- Centralized debug control via env or flag
- Uses class-based games (imported modules)
"""
from __future__ import annotations
import os
from typing import Dict

from math_checker import MathChecker, MathCheckerConfig
from number_guesser import NumberGuesser, NumberGuesserConfig
from memory_bank import MemoryBank, MemoryBankConfig

# --------------------------- Utils 🔧---------------------------
def env_debug() -> bool:
    v = os.getenv("DATAMON_DEBUG", "").strip().lower()
    return v in {"1", "true", "on", "yes"}

def clear():
    if os.getenv("DATAMON_NOCLEAR", ""):
        return
    os.system("cls" if os.name == "nt" else "clear")

def pause(msg="Press Enter to continue..."):
    try:
        input(msg)
    except EOFError:
        pass

# --------------------------- Player 🎮 ---------------------------
def new_player(name: str = "Player") -> Dict:
    return {
        "name": name,
        # Answer Checker history/score
        "answer_checker": [],
        "score_answer_checker": 0,
        # Memory Bank history/score (future extension)
        "memory_bank": [],
        "score_memory_bank": 0,
        # Number Guesser history/score
        "number_guesser": [],
        "score_number_guesser": 0,
    }

# --------------------------- Menus 📋---------------------------
def print_header(title: str):
    clear()
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)

def main_menu(player):
    while True:
        print_header(f"Datamon — Welcome, {player['name']}")
        print("1) Math Checker")
        print("2) Number Guesser")
        print("3) Memory Bank")
        print("4) Session Summary")
        print("0) Quit\n")

        choice = input("Select: ").strip()
        if choice == "1":
            math_checker_menu(player)
        elif choice == "2":
            launch_number_guesser(player)
        elif choice == "3":
            launch_memory_bank()
        elif choice == "4":
            show_summary(player)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            pause()

def math_checker_menu(player):
    # Build a MathChecker instance with shared debug env
    mc = MathChecker(MathCheckerConfig(
        min_num=0, max_num=100, retries=2,
        nonnegative_remainder=True,
        clear_between_screens=not bool(os.getenv("DATAMON_NOCLEAR", "")),
        debug=env_debug()
    ))

    while True:
        print_header("Math Checker")
        print("1) Addition")
        print("2) Subtraction")
        print("3) Multiplication")
        print("4) Division (q + r)")
        print("0) Back\n")
        choice = input("Select: ").strip()

        if choice == "1":
            mc.run_addition_session(player)
        elif choice == "2":
            mc.run_subtraction_session(player)
        elif choice == "3":
            mc.run_multiplication_session(player)
        elif choice == "4":
            mc.run_division_session(player)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
            pause()

def launch_number_guesser(player):
    ng = NumberGuesser(NumberGuesserConfig(
        clear_between_screens=not bool(os.getenv("DATAMON_NOCLEAR", "")),
        debug=env_debug()
    ))
    ng.run(player)

def launch_memory_bank():
    mb = MemoryBank(MemoryBankConfig(
        data_path="Data.txt",
        clear_between_screens=not bool(os.getenv("DATAMON_NOCLEAR", "")),
        debug=env_debug()
    ))
    mb.run()

def show_summary(player):
    print_header("Session Summary")
    # Basic tallies
    ac_hist = player.get("answer_checker", [])
    ng_hist = player.get("number_guesser", [])

    print(f"Player: {player['name']}")
    print(f"Answer Checker: {player.get('score_answer_checker', 0)} points — {len(ac_hist)} attempts logged")
    print(f"Number Guesser: {player.get('score_number_guesser', 0)} points — {len(ng_hist)} rounds played")
    print("\nRecent Answer Checker attempts (last 10):")
    for a in ac_hist[-10:]:
        mark = "✓" if a.get("correct") else "×"
        print(f"  [{mark}] {a.get('problem')} | you: {a.get('user_answer')} | correct: {a.get('correct_answer')}")

    print("\nRecent Number Guesser rounds (last 5):")
    for r in ng_hist[-5:]:
        status = "WIN" if r.get("won") else "LOSE"
        rng = r.get("range", {})
        print(f"  [{status}] {r.get('difficulty')} {rng.get('lo')}-{rng.get('hi')} | "
              f"used {r.get('attempts_used')} tries | +{r.get('points')} pts")

    pause()

# --------------------------- Entrypoint ---------------------------
def main():
    clear()
    print("Datamon — Modular Practice Suite")
    name = input("Enter player name (leave blank for 'Player'): ").strip() or "Player"
    player = new_player(name)
    main_menu(player)
    clear()
    print("Thanks for playing Datamon — see you next time!")

if __name__ == "__main__":
    main()
