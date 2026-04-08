class Adult:
    def __init__(self, name, age, eye_color, hair_color):
        self.name = name
        self.age = age
        self.eye_color = eye_color
        self.hair_color = hair_color

    def can_drive(self):
        print(f"{self.name} is {self.age} years old and can drive.")


class Child(Adult):
    def can_drive(self):
        print(f"{self.name} is {self.age} years old and cannot drive.")


name = input("Enter the name of the person: ")
age = int(input("Enter the age of the person: "))
eye_color = input("Enter the eye color of the person: ")
hair_color = input("Enter the hair color of the person: ")
if age >= 18:
    person = Adult(name, age, eye_color, hair_color)
else:
    person = Child(name, age, eye_color, hair_color)

person.can_drive()
