class Course:
    # Class attribute for the course name
    name = "Fundamentals of Computer Science"

    # Class attribute for the contact website
    contact_website = "www.hyperiondev.com"

    # Method to display contact details
    def contact_details(self):
        print("Please contact us by visiting", self.contact_website)

    def head_office_location(self):
        print("Our head office is located in Cape Town, South Africa.")


class OOPCourse(Course):
    def __init__(self):
        self.description = "OOP Fundamentals"
        self.trainer = "Mr Anon A. Mouse"

    def trainer_details(self):
        print(f"This course focuses on {self.description}")
        print(f"and is taught by {self.trainer}.")

    def show_course_id(self):
        print("Course ID: #12345")


# Example usage:
# Create an instance of the OOPCourse class
course_1 = OOPCourse()

# Call the contact_details method to display contact information
course_1.contact_details()
course_1.head_office_location()
course_1.trainer_details()
course_1.show_course_id()
