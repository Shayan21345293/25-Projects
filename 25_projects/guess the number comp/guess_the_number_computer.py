import random

# Initializing the values
low = 1
high = 10
guesses = 0

user_name = input("What is your name: ")
print(f"HI {user_name}, WELCOME TO MY NUMBER GUESSING GAME!")
print("Think of a number between 1 to 10 and I will try to guess it.")
print("You can tell me if the number is too high (H), too low (L), or correct (C).")

while True:
    # Computer guesses a number
    guess = random.randint(low, high)
    guesses += 1

    # Showing the computer's guess
    print(f"My guess is {guess}")
    user_feedback = input("Is my guess too high (H), too low (L), or correct (C)? ").upper()

    if user_feedback == "C":
        print(f"Yay! I guessed it in {guesses} tries.")
        print("THIS GAME IS CREATED BY SHAYAN ALI")
        break
    elif user_feedback == "H":
        high = guess - 1  # Adjust the range
    elif user_feedback == "L":
        low = guess + 1  # Adjust the range
    else:
        print("Please enter a valid response (H, L, or C).")
