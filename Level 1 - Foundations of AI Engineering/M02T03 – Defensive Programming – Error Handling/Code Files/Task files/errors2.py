# This example program is meant to demonstrate errors.
 
# There are some errors in this program. Run the program, look at the error messages, and find and fix the errors.

animal = "lion" # syntax error: needs to be in quotes
animal_type = "cub"
number_of_teeth = 16

full_spec = f"This is a {animal}. It is a {animal_type} and it has {number_of_teeth} teeth" # syntax error: needs f before quotes
                                                                                            # logical error: switch number of teeth and animal type
print(full_spec) # syntax errors: needs parentheses