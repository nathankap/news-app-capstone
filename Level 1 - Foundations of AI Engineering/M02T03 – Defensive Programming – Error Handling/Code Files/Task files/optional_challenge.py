add1 = input("Enter the first number: ")
add2 = input("Enter the second number: ")

print(f"The sum of the two numbers is: {int(add1) - int(add2)}") # logical error: should be add not subtract

numbers = [add1, add2]

print(f"the third number is: {numbers[2]}") # runtime error: indexing out of range