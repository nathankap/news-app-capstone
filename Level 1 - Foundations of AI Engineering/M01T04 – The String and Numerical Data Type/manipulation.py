str_manip = input("Enter a string: ")
print(f"The string is {len(str_manip)} characters long.")

str_manip_copy = str_manip
last_char = str_manip[-1]
str_manip_copy = str_manip_copy.replace(last_char, "@")
print(str_manip_copy)

print(str_manip[:-4:-1])

print(str_manip[:3] + str_manip[-2:])