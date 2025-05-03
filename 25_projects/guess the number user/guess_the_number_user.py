# Project 3: Guess the Number Game Python Project (User) BY SHAYAN ALI

import random

low = 1
high = 10
guesses = 0


pc_guess = random.randint(low, high)

print("Welcome to the Guess the Number Game!")
print(f"I have selected a number between {low} and {high}. Can you guess it?")

while True:
    try:
        user_guess = int(input("Enter your guess: "))
        guesses += 1

        if user_guess < low or user_guess > high:
            print(f"Please enter a number between {low} and {high}.")
        elif user_guess > pc_guess:
            print("Too high! Try again.")
        elif user_guess < pc_guess:
            print("Too low! Try again.")
        else:
            print(f"Congratulations! You guessed the number {pc_guess} in {guesses} attempts.")
            print("This game created by SHAYAN ALI")
            break
    except ValueError:
        print("Invalid input! Please enter a valid number.")

