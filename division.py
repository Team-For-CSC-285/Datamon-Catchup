

# Ask for numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Calculate the correct answer
correct_answer = num1 / num2

# Ask the user for their guess
guess = float(input(f"What is {num1} divided by {num2}? "))

# Check if guess is correct
if guess == correct_answer:
    print("✅ Correct!")
else:
    print(f"❌ Incorrect. The correct answer is {correct_answer}.")
