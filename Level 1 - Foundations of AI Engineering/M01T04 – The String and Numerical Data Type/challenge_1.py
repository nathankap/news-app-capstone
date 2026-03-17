side1 = input("Enter the length of the first side of the triangle: ")
side2 = input("Enter the length of the second side of the triangle: ")
side3 = input("Enter the length of the third side of the triangle: ")

s = (side1 + side2 + side3) / 2
area = (s * (s - int(side1)) * (s - int(side2)) * (s - int(side3))) ** 0.5
print(f"The area of the triangle is: {area}")