user_input = ""
incorrect_names = []
while user_input.lower() != "john":
    user_input = input("Please input a name: ")
    if user_input.lower() != "john":
        incorrect_names.append(user_input)

print("Incorrect names:", incorrect_names)