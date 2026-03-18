sum = 0
count = 0
number = 1
while number != 0 and number != -1: 
    number = int(input("Enter any integer (or -1 to stop): "))
    if number == 0 or number == -1:
        break
    sum += number
    count += 1

if count > 0:
    average = sum / count
    print(f"The average of the entered numbers is: {average}")