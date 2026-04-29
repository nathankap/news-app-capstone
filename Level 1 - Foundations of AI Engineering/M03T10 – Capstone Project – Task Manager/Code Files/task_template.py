# ===== Importing external modules ===========
'''This is the section where you will import modules'''

# ==== Login Section ====
# Implement the following functionality
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and passwords from the user.txt file
    - You can use a list or dictionary to store a list of usernames and
       passwords from the file.
    - Use a while loop to validate your user name and password.
'''
# Create dictionary for usernames and passwords
user_pass_dict = {}

# Open user.txt and populate dictionary with contents
try:
    with open("user.txt", "r") as file:
        for line in file:
            login = line.strip().split(", ")
            user_pass_dict[login[0]] = login[1]
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# Helper function for incorrect passwords
# Parameter: user_or_again
# - used for message to user.
# Example:
# If user_or again is "another username", then
# -> "Password incorrect. Try another username? (y/n)"
#
# Used for multiple loops
# Returns True for yes, False for no
def _try_again(user_or_again):
    while True:
        again = input(
            f"Password incorrect. Try {user_or_again}? (y/n)")
        # If yes, then return True to end password loop
        if again in ["y", "yes"]:
            return True
        # If no, then return False to restart password loop
        elif again in ["n", "no"]:
            return False


# Helper function for asking for password
def _ask_pass(username):
    while True:
        print(f"Username found: {username}")
        password = input("Please enter your password: ")
        # If password accepted, return True to end the loop
        if user_pass_dict[username] == password:
            print("\nUsername and password accepted!\n")
            print("*********************************\n\n")

            return True

        # If password not accepted, ask to try another username
        else:
            if (_try_again("another username")):
                return False


# Helper function for asking for username
def _ask_user():
    while True:
        username = input("Please enter your username: ")
        # If username exists, then asks for password
        if user_pass_dict.setdefault(username):
            if (_ask_pass(username)):
                return

        # If username does not exist, then ask for username again
        else:
            print("Username not found. Please try again.\n")


# Loop for asking for username and password
print("\n\n*********************************")
print("\nLog into your account\n\n")
_ask_user()


# Helper function for updated user.txt with new user & pass
def _update_new_user_pass():
    try:
        with open("user.txt", "a") as file:  # Open file as append
            # Append new line with user, pass
            file.write(f"\n{new_user}, {new_pass}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    print("MAIN MENU\n\n")
    menu = input(
        '''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
    ).lower()

    if menu == 'r':
        # Implement the following functionality
        '''This code block will add a new user to the user.txt file
        - You can use the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same
            - If they are the same, add them to the user.txt file,
              otherwise present a relevant message'''
        print("\n\n*********************************")
        print("\nREGISTER A USER\n\n")
        new_user = input("Please enter the new username: ")
        print(f"Username entered: {new_user}")
        new_pass = input("Please enter the new password: ")

        while True:
            new_pass_confirm = input("Please confirm the new password: ")
            if new_pass == new_pass_confirm:
                _update_new_user_pass()
                print("\nNew username and password successfully added!\n")
                break
            else:
                if not _try_again("again"):
                    print("\nNew username and password not added.\n")
                    break
        print("*********************************\n\n")

    elif menu == 'a':
        # TODO: Implement the following functionality
        '''This code block will allow a user to add a new task to task.txt file
        - You can use these steps:
            - Prompt a user for the following:
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not
              complete.
        '''
        pass  # Remove this once you implement the functionality

    elif menu == 'va':
        # TODO: Implement the following functionality
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in
              the PDF
            - It is much easier to read a file using a for loop.'''
        pass  # Remove this once you implement the functionality

    elif menu == 'vm':
        # TODO: Implement the following functionality
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF '''
        pass  # Remove this once you implement the functionality

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
