print("Welcome to the calculator app!")
print("This app will perform basic arithmetic operations on two numbers.")
print("For previous equations, type 'history'.")

while True:
    user_input = input("Enter an equation (e.g., 2 + 3) or 'history': ")
    if user_input.lower() == "history":
        try:
            with open("history.txt", "r") as file:
                history = file.read()
                print("Calculation History:")
                print(history)
        except FileNotFoundError:
            print("No history found.")
        continue
    try:
        num1, operator, num2 = user_input.split()
        num1 = float(num1)
        num2 = float(num2)

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result = num1 / num2
        else:
            raise ValueError("Invalid operator. Please use +, -, *, or /.")
        print(f"{num1} {operator} {num2} = {result}")
        with open("history.txt", "a") as file:
            file.write(f"{num1} {operator} {num2} = {result}\n")
    except ValueError as ve:
        print(f"Value error: {ve}")
    except ZeroDivisionError as zde:
        print(f"Zero division error: {zde}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
