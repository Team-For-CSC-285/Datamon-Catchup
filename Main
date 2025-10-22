import os

###################################################################################################################
'''                      Examples of objects that will go inside the lists in Player dict below!!!        
 
    "answer_checker": [
        {
            "problem": "2 + 2",
            "user_answer": 4,
            "correct_answer": 4,
            "correct": True
        },
        {
            "problem": "5 * 3",
            "user_answer": 16,
            "correct_answer": 15,
            "correct": False
        },
        {
            "problem": "10 / 2",
            "user_answer": 5,
            "correct_answer": 5,
            "correct": True
        }
    ]

'''
###################################################################################################################

# Player data for now (We will add more to this as we go)
player = {
    "name": "Unknown",
    "answer_checker": [],
    "memory_bank": [],
    "number_guesser": [],
    "score_answer_checker": 0,
    "score_memory_bank": 0,
    "score_number_guesser": 0
}



# Helper methods
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
    
# Used https://www.asciiart.eu/text-to-ascii-art
def print_starting_screen():
    logo = r"""
++--------------------------------------------------++
++--------------------------------------------------++
||    __        __   _                              ||
||    \ \      / /__| | ___ ___  _ __ ___   ___     ||
||     \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \    ||
||      \ V  V /  __/ | (_| (_) | | | | | |  __/    ||
||       \_/\_/ \___|_|\___\___/|_| |_| |_|\___|    ||
||                                                  ||
||                   _                              ||
||                  | |_ ___                        ||
||                  | __/ _ \                       ||
||                  | || (_) |                      ||
||                   \__\___/                       ||
||                                                  ||
||   ____        _                              _   ||
||  |  _ \  __ _| |_ __ _ _ __ ___   ___  _ __ | |  ||
||  | | | |/ _` | __/ _` | '_ ` _ \ / _ \| '_ \| |  ||
||  | |_| | (_| | || (_| | | | | | | (_) | | | |_|  ||
||  |____/ \__,_|\__\__,_|_| |_| |_|\___/|_| |_(_)  ||
||                                                  ||
++--------------------------------------------------++
++--------------------------------------------------++
                                                               
    """
    print(logo)
    input("Press any key to continue...")
    clear_terminal()


def print_menu():
    logo = r"""
.-----------------------------------------------------------------------------.
|                                                                             |
| ____        _                                       __  __                  |
||  _ \  __ _| |_ __ _ _ __ ___   ___  _ __    _     |  \/  | ___ _ __  _   _ |
|| | | |/ _` | __/ _` | '_ ` _ \ / _ \| '_ \  (_)    | |\/| |/ _ \ '_ \| | | ||
|| |_| | (_| | || (_| | | | | | | (_) | | | |  _     | |  | |  __/ | | | |_| ||
||____/ \__,_|\__\__,_|_| |_| |_|\___/|_| |_| (_)    |_|  |_|\___|_| |_|\__,_||
|                                                                             |
'-----------------------------------------------------------------------------'                                                       
    """
    print(logo)
    print(f"\t\t\t\tPLAYER: {player['name']}\n")
    print("1] Answer Checker")
    print("2] Memory Bank")
    print("3] Number Guesser")
    print("0] Exit\n")

def create_player_menu():
    logo = r"""
.------------------------------------------------------------------------------------------------------------------.
|                                                                                                                  |
| ____        _                                        ____                _         ____  _                       |
||  _ \  __ _| |_ __ _ _ __ ___   ___  _ __    _      / ___|_ __ ___  __ _| |_ ___  |  _ \| | __ _ _   _  ___ _ __ |
|| | | |/ _` | __/ _` | '_ ` _ \ / _ \| '_ \  (_)    | |   | '__/ _ \/ _` | __/ _ \ | |_) | |/ _` | | | |/ _ \ '__||
|| |_| | (_| | || (_| | | | | | | (_) | | | |  _     | |___| | |  __/ (_| | ||  __/ |  __/| | (_| | |_| |  __/ |   |
||____/ \__,_|\__\__,_|_| |_| |_|\___/|_| |_| (_)     \____|_|  \___|\__,_|\__\___| |_|   |_|\__,_|\__, |\___|_|   |
|                                                                                                  |___/           |
|                                                                                                                  |
'------------------------------------------------------------------------------------------------------------------'                                                     
    """
    print(logo)
    player["name"] = input("What is your name?: ")

# Sprint 1?
def answer_checker():

    logo = r"""
.--------------------------------------------------------------------------------------------------------------------------.
| ____        _                                     _                                   ____ _               _             |
||  _ \  __ _| |_ __ _ _ __ ___   ___  _ __  _     / \   _ __  _____      _____ _ __   / ___| |__   ___  ___| | _____ _ __ |
|| | | |/ _` | __/ _` | '_ ` _ \ / _ \| '_ \(_)   / _ \ | '_ \/ __\ \ /\ / / _ \ '__| | |   | '_ \ / _ \/ __| |/ / _ \ '__||
|| |_| | (_| | || (_| | | | | | | (_) | | | |_   / ___ \| | | \__ \\ V  V /  __/ |    | |___| | | |  __/ (__|   <  __/ |   |
||____/ \__,_|\__\__,_|_| |_| |_|\___/|_| |_(_) /_/   \_\_| |_|___/ \_/\_/ \___|_|     \____|_| |_|\___|\___|_|\_\___|_|   |
'--------------------------------------------------------------------------------------------------------------------------'                                       
"""
    correct_count = 0
    total_problems = 5

    for i in range(1, total_problems + 1):
        num1 = None
        operator = None
        num2 = None

        # === STEP 1–3: Enter full problem ===
        while True:
            clear_terminal()
            print(logo)
            print(f"PLAYER: {player['name']}\t\tProblem {i} of {total_problems}\t\tSCORE: {correct_count} / {i-1}\n")
            display = ""
            display += str(num1) if num1 is not None else "_"
            display += " "
            display += operator if operator is not None else "_"
            display += " "
            display += str(num2) if num2 is not None else "_"
            print(f"{display}\n")

            # Ask for missing part
            if num1 is None:
                val = input("Enter first number: ").strip()
                if val.lstrip("-").isdigit():
                    num1 = int(val)
                else:
                    print("❌ Invalid number.")
                    input("Press Enter to try again...")
                    continue

            elif operator is None:
                val = input("Enter operator (+, -, *, /): ").strip()
                if val in ["+", "-", "*", "/"]:
                    operator = val
                else:
                    print("❌ Invalid operator.")
                    input("Press Enter to try again...")
                    continue

            elif num2 is None:
                val = input("Enter second number: ").strip()
                if val.lstrip("-").isdigit():
                    n2 = int(val)
                    if operator == "/" and n2 == 0:
                        print("❌ Cannot divide by zero.")
                        input("Press Enter to try again...")
                        continue
                    num2 = n2
                else:
                    print("❌ Invalid number.")
                    input("Press Enter to try again...")
                    continue

            # Stop once all 3 parts are valid
            if num1 is not None and operator is not None and num2 is not None:
                break

        # === SHOW FULL PROBLEM BEFORE ANSWERING ===
        clear_terminal()
        print(logo)
        print(f"PLAYER: {player['name']}\t\tProblem {i} of {total_problems}\t\tSCORE: {correct_count} / {i-1}\n")
        print(f"Problem: {num1} {operator} {num2}\n")

        # === STEP 4: Calculate correct answer ===
        if operator == "+":
            correct_answer = num1 + num2
            problem_str = f"{num1} + {num2}"
        elif operator == "-":
            correct_answer = num1 - num2
            problem_str = f"{num1} - {num2}"
        elif operator == "*":
            correct_answer = num1 * num2
            problem_str = f"{num1} * {num2}"
        elif operator == "/":
            correct_answer = num1 // num2
            remainder = num1 % num2
            problem_str = f"{num1} ÷ {num2}"

        # === STEP 5: User answers ===
        if operator == "/":
            # Quotient
            while True:
                q_str = input("Quotient: ").strip()
                if q_str.lstrip("-").isdigit():
                    user_answer = int(q_str)
                    break
                print("❌ Invalid number. Try again.")

            # Remainder
            while True:
                r_str = input("Remainder: ").strip()
                if r_str.lstrip("-").isdigit():
                    user_remainder = int(r_str)
                    break
                print("❌ Invalid number. Try again.")

            # Check answers
            if user_answer == correct_answer and user_remainder == remainder:
                print("✅ Correct!")
                correct = True
                correct_count += 1
            else:
                print("❌ Wrong! Try again...")
                # Retry
                while True:
                    q_str = input("Quotient: ").strip()
                    if q_str.lstrip("-").isdigit():
                        user_answer = int(q_str)
                        break
                while True:
                    r_str = input("Remainder: ").strip()
                    if r_str.lstrip("-").isdigit():
                        user_remainder = int(r_str)
                        break
                if user_answer == correct_answer and user_remainder == remainder:
                    print("✅ Correct on second try!")
                    correct = True
                    correct_count += 1
                else:
                    print(f"❌ Incorrect again. Correct answer: {correct_answer} R{remainder}")
                    correct = False

        else:
            # Single-number answer
            while True:
                ans_str = input("Your answer: ").strip()
                if ans_str.lstrip("-").isdigit():
                    user_answer = int(ans_str)
                    break
                print("❌ Invalid number. Try again.")

            if user_answer == correct_answer:
                print("✅ Correct!")
                correct = True
                correct_count += 1
            else:
                print("❌ Wrong! Try again...")
                while True:
                    ans_str = input("Your answer: ").strip()
                    if ans_str.lstrip("-").isdigit():
                        user_answer = int(ans_str)
                        break
                if user_answer == correct_answer:
                    print("✅ Correct on second try!")
                    correct = True
                    correct_count += 1
                else:
                    print(f"❌ Incorrect again. Correct answer: {correct_answer}")
                    correct = False

        # === STEP 6: Record attempt ===
        player["answer_checker"].append({
            "problem": problem_str,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": correct
        })

        input("\nPress Enter to continue...")

    # === STEP 7: ROUND SUMMARY ===
    clear_terminal()
    print(logo)
    print(f"PLAYER: {player['name']}")
    print(f"FINAL SCORE: {correct_count} : {total_problems}\n")
    player["score_answer_checker"] += correct_count
    print(f"Total accumulated score: {player['score_answer_checker']}\n")

    # === SIMPLE PROBLEM SUMMARY ===
    print("Problem Summary:")
    for i, attempt in enumerate(player["answer_checker"][-total_problems:], start=1):
        mark = "✅" if attempt["correct"] else "❌"
        problem = f"{attempt['problem']} = {attempt['correct_answer']}"
        problem_col = problem.ljust(12)  # pad to fixed width
        your_col = f"Your answer: {attempt['user_answer']}".ljust(18)
        print(f"{i}) {problem_col} {your_col} {mark}")
        

# Sprint 2?
def memory_bank():
    print("\n[Memory Bank]")
    print("This feature is coming soon!")

# Sprint 3?
def number_guesser():
    print("\n[Number Guesser]")
    print("This feature is coming soon!")


### Main method (where the game will loop) ###
def main():
#Setting up Game/Player
    print_starting_screen()
    create_player_menu()

# Game Loop starts here
    while True:
        clear_terminal()
        print_menu() # Edit menu in this function
        choice = input("Selected: ")

        # Check for valid input
        if not choice.isdigit():
            print("⚠️ Please enter a number!")
            input("Press Enter to continue...")
            continue

        choice = int(choice) #cast to integer
        clear_terminal()
        
        # Menu choices
        if choice == 1:
            answer_checker()
        elif choice == 2:
            memory_bank()
        elif choice == 3:
            number_guesser()
        elif choice == 0:
            print("\n👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option!")

        input("\nPress Enter to return to the menu...")

# Calls main to run the program
if __name__ == "__main__":
    main()
