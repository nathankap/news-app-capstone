string_fav = input("What is your favorite restaurant? ")
int_fav = int(input("What is your favorite number? "))

print(f"Your favorite restaurant is {string_fav} and your favorite number is {int_fav}.")

# string_fav = int(string_fav)
# results in ValueError: invalid literal for int() with base 10: 'olive garden' 
# because the string "olive garden" cannot be converted to an integer since it contains non-numeric characters.