
import random
import string

letter=string.ascii_letters
digits=string.digits
symbols=string.punctuation
all_character =letter+digits+symbols
print("Welcome to my Password Generator!")
print("Generate a strong password EASILY")
try:
  password_lenght=int(input("ENTER THE LENGHT OF YOUR PASSWORD(minimum 6):"))
  if password_lenght < 6:
     print("Password lenght must be more than 6 character")
except ValueError:
  print("Invalid Input!")

password="".join(random.choice(all_character) for _ in range(password_lenght))

print(f"YOUR PASSWORD IS: {password}")
print(" THIS PASSWORD GENERATOR IS CREATED BY SHAYAN ALI")