num_students = int(input("How many students are registering? "))
for i in range(num_students):
    student_id = str(input("Enter student ID: "))
    with open("students.txt", "a") as file:
        file.write(student_id + " ........... \n")