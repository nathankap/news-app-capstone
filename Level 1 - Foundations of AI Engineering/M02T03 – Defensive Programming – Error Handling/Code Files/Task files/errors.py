# This example program is meant to demonstrate errors.
 
# There are some errors in this program. Run the program, look at the error messages, and find and fix the errors.

print ("Welcome to the error program") # syntax error: missing parentheses around print statement
print ("\n") # syntax error: unexpected indent

# Variables declaring the user's age, casting the str to an int, and printing the result
age_Str = "24"  # syntax error: needs to be = instead of ==
age = int(age_Str) # syntax error: string needs to be numerical characters
print("I'm " + age_Str + " years old.") # syntax error: age needs to be string

# Variables declaring additional years and printing the total years of age
years_from_now = 3 # syntax error: needs to be int not str
total_years = age + years_from_now

print("The total number of years:" + str(total_years)) # syntax error: no parentheses, total_years needs to be converted to a str

# Variable to calculate the total number of months from the given number of years and printing the result
total_months = total_years * 12 + 6 # syntax error: total_months needs to be calculated by multiplying total_years by 12
                                    # logical error: 6 months needs to be added to the total number of months calculated from total_years
print("In 3 years and 6 months, I'll be " + str(total_months) + " months old") # syntax error: no parentheses, total_months needs to be converted to a str, and the number of months needs to be calculated by adding 6 to total_years before multiplying by 12

#HINT, 330 months is the correct answer

