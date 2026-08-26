import sympy as sp


def calculate_gradient(function):
    x, y = sp.symbols("x y")

    # Parse the user-entered function
    f = sp.sympify(function)

    # Calculate partial derivatives
    df_dx = sp.diff(f, x)
    df_dy = sp.diff(f, y)

    return df_dx, df_dy


# Get function from user
function = input("Enter a two-term multivariable function: ")

# Calculate gradient
df_dx, df_dy = calculate_gradient(function)

# Display result
print(
    f"The gradient vector of the function f = {function} "
    f"is \u2207f = ({df_dx}, {df_dy})."
)