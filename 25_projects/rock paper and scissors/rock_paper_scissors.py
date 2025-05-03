# Project 4: Rock, Paper, Scissors Python Project, by SHAYAN ALI

import random

print("Welcome to the Rock, Paper, Scissors game!")
print("You will play against the computer. SO LET'S BEGIN!")

choices = ["R", "P", "S"]

while True:
    user_choice = input("Enter your choice - Rock (R), Paper (P), or Scissors (S), or 'Q' to quit: ").upper()

    if user_choice == 'Q':
        print("THANKS FOR PLAYING! Goodbye. 👋")
        break

    # Validating user choice
    if user_choice not in choices:
        print("Invalid choice! Please choose Rock (R), Paper (P), or Scissors (S).")
        continue

    # Computer makes a random choice
    computer_choice = random.choice(choices)
    print(f"Computer chose: {computer_choice}")

    # Determining the winner
    if user_choice == computer_choice:
        print("It's a tie!")
    elif (user_choice == "R" and computer_choice == "S") or \
         (user_choice == "P" and computer_choice == "R") or \
         (user_choice == "S" and computer_choice == "P"):
        print("Congratulations! You win! 🎉")
    else:
        print("You lose! Better luck next time. 😢")

    print("\n")