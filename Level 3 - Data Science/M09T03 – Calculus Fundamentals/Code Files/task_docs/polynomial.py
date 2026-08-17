# Get inputs from the user
coefficient = float(input("Enter the coefficient of x: "))
power = int(input("Enter the power to raise x: "))
x = float(input(
    "Enter the x-coordinate of the point where you would like "
    "to calculate the gradient: "
))

# Apply the power rule
derivative_coefficient = coefficient * power
derivative_power = power - 1

# Calculate the gradient at the given x-coordinate
gradient = derivative_coefficient * (x ** derivative_power)

# Display the result
print(
    f"The derivative of the polynomial {coefficient:g}x^{power} "
    f"is {derivative_coefficient:g}x^{derivative_power}. "
    f"The gradient at the point x = {x:g} is {gradient:g}."
)