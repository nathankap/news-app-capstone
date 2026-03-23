names = []
dobs = []

with open("DOB.txt", "r") as file:
    for line in file:
        names.append(line.strip().split(" ")[0:2])
        dobs.append(line.strip().split(" ")[2:5])

print("Name")
for name in names:
    print(" ".join(name))
print("\nBirthdate")
for dob in dobs:
    print(" ".join(dob))
