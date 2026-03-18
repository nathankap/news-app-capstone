import math

print("Investment - to calculate the amount of interest you'll earn on your investment.")
print("Bond       - to calculate the amount you'll have to pay on a home loan.")

calculator = input("Choose either 'investment' or 'bond' from the menu above to proceed: ").lower()

if calculator == "investment":
    deposit = float(input("Enter the amount of money you are depositing: "))
    interest_rate = float(input("Enter the interest rate (as a percentage): ")) / 100
    years = int(input("Enter the number of years you plan to invest: "))
    interest_type = input("Choose either 'simple' or 'compound' interest: ").lower()

    if interest_type == "simple":
        total_amount = deposit * (1 + interest_rate * years)
        print(f"The total amount after {years} years will be: {total_amount:.2f}")
    elif interest_type == "compound":
        total_amount = deposit * math.pow((1 + interest_rate), years)
        print(f"The total amount after {years} years will be: {total_amount:.2f}")
    else:
        print("Invalid interest type. Please choose 'simple' or 'compound'.")

elif calculator == "bond":
    present_value = float(input("Enter the present value of the house: "))
    annual_interest_rate = float(input("Enter the annual interest rate (as a percentage): ")) / 100
    monthly_interest_rate = annual_interest_rate / 12
    months = int(input("Enter the number of months you plan to take to repay the bond: "))

    monthly_payment = (monthly_interest_rate * present_value) / (1 - math.pow((1 + monthly_interest_rate), -months))
    print(f"The monthly payment will be: {monthly_payment:.2f}")