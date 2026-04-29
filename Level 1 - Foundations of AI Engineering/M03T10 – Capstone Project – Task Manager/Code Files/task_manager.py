# ===== Importing external modules ===========
'''This is the section where you will import modules'''
from datetime import date

# ==== Login Section ====
# Implement the following functionality
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and passwords from the user.txt file
    - You can use a list or dictionary to store a list of usernames and
       passwords from the file.
    - Use a while loop to validate your user name and password.
'''


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
                # Return username if login successful
                return username

        # If username does not exist, then ask for username again
        else:
            print("Username not found. Please try again.\n")


# Helper function for updated user.txt with new user & pass
def _update_new_user_pass(new_user, new_pass):
    try:
        with open("user.txt", "a") as file:  # Open file as append
            # Append new line with user, pass
            file.write(f"\n{new_user}, {new_pass}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Helper function for updated tasks.txt with new task info
def _update_new_task(assign_user, title_task, desc_task,
                     due_date_task, curr_date):
    try:
        with open("tasks.txt", "a") as file:  # Open file as append
            # Append new line with user, pass
            file.write(
                f"\n{assign_user}, {title_task}, {desc_task}, "
                f"{due_date_task}, {curr_date}, No"
            )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Helper function for deleting tasks in tasks.txt
def _del_task_file(task_to_delete):
    # Read tasks.txt
    with open("tasks.txt", "r") as file:
        lines = file.readlines()

    while True:
        delete = input("Delete task? (y/n)")
        # If yes, then rewrite tasks.txt without the task
        if delete in ["y", "yes"]:
            try:
                with open("tasks.txt", "w") as file:  # Open as w
                    # Rewrite entire file without the deleted task
                    for line in lines:
                        if line.strip():
                            task = line.strip().split(", ")
                            if task_to_delete != task[1]:
                                file.write(line)
                return True

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        # If no, then return False
        elif delete in ["n", "no"]:
            return False


# PRACTICAL TASK - PART 3 FUNCTIONS
def reg_user():
    # Implement the following functionality
    '''This code block will add a new user to the user.txt file'''
    print("\n\n*********************************")
    print("\nREGISTER A USER\n\n")

    # Take user input
    new_user = input("Please enter the new username: ")
    print(f"Username entered: {new_user}")
    new_pass = input("Please enter the new password: ")

    # Loop for password confirmation
    while True:
        new_pass_confirm = input("Please confirm the new password: ")
        # If password is confirmed, then _update_new_user_pass()
        # to update user.txt
        if new_pass == new_pass_confirm:
            _update_new_user_pass(new_user, new_pass)
            print("\nNew username and password successfully added!\n")
            break
        else:
            if not _try_again("again"):
                print("\nNew username and password not added.\n")
                break
    print("*********************************\n\n")
    input("\nEnter any character to return to the main menu.\n")


def add_task():
    '''This code block will allow a user to add a new task to
        tasks.txt file '''

    print("\n\n*********************************")
    print("\nADD TASK\n\n")

    # Loop for asking username
    while True:
        assign_user = input(
            "Please enter the username of the person whom the task is "
            "assigned to: ")
        # Check if username exists
        if user_pass_dict.setdefault(assign_user):
            print(f"Username ({assign_user}) entered.")
            break

        # If username does not exist, then ask for username again
        else:
            print("Username not found. Please try again.\n")

    # Ask for other task parameters
    title_task = input("Please enter the title of the task: ")
    desc_task = input("Please enter the description of the task: ")
    due_date_task = input("Please enter the due date of the task: ")
    curr_date = date.today()

    # Use _update_new_task() to add task to tasks.txt
    _update_new_task(assign_user, title_task, desc_task,
                     due_date_task, curr_date)

    # Print new task that was added
    print("\nTask successfully added!")
    print("_________________________________________\n")
    print(f"Task:               {title_task}")
    print(f"Assigned to:        {assign_user}")
    print(f"Date assigned:      {curr_date}")
    print(f"Due date:           {due_date_task}")
    print("Task Complete?      No")
    print("Task description:")
    print(f" {desc_task}")
    print("\n_________________________________________\n")
    input("\nEnter any character to return to the main menu.\n")


def view_all():
    '''This code block will read the task from task.txt file and
    print all tasks'''
    print("\n\n*********************************")
    print("\nVIEW ALL TASKS\n\n")
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip().split(", ")
                print("\n______________________________________\n")
                print(f"Task:               {task[1]}")
                print(f"Assigned to:        {task[0]}")
                print(f"Date assigned:      {task[4]}")
                print(f"Due date:           {task[3]}")
                print(f"Task Complete?      {task[5]}")
                print("Task description:")
                print(f" {task[2]}")
                print("\n______________________________________\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("*********************************\n\n")
    input("\nEnter any character to return to the main menu.\n")


def view_mine():
    '''This code block will read the tasks from task.txt file and
    print user's task(s)'''
    print("\n\n*********************************")
    print("\nVIEW MY TASKS\n\n")
    print(f"for user: ({current_user})")
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip().split(", ")
                if current_user == task[0]:
                    print("\n______________________________________\n")
                    print(f"Task:               {task[1]}")
                    print(f"Assigned to:        {task[0]}")
                    print(f"Date assigned:      {task[4]}")
                    print(f"Due date:           {task[3]}")
                    print(f"Task Complete?      {task[5]}")
                    print("Task description:")
                    print(f" {task[2]}")
                    print("\n______________________________________\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("*********************************\n\n")
    input("\nEnter any character to return to the main menu.\n")


def view_completed():
    '''
    This code block will read the task from task.txt file and
    print all completed tasks
    '''
    print("\n\n*********************************")
    print("\nVIEW COMPLETED TASKS\n\n")
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip().split(", ")
                if task[5] == "Yes":
                    print("\n______________________________________\n")
                    print(f"Task:               {task[1]}")
                    print(f"Assigned to:        {task[0]}")
                    print(f"Date assigned:      {task[4]}")
                    print(f"Due date:           {task[3]}")
                    print(f"Task Complete?      {task[5]}")
                    print("Task description:")
                    print(f" {task[2]}")
                    print("\n______________________________________\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("*********************************\n\n")
    input("\nEnter any character to return to the main menu.\n")


def delete_task():
    '''This code block will read the task from task.txt file and
    print the tasks then delete it
    '''
    print("\n\n*********************************")
    print("\nDELETE TASKS\n\n")
    while True:
        task_to_delete = input("Please enter task to be deleted: ")
        task_found = False
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    task = line.strip().split(", ")
                    if task_to_delete == task[1]:
                        task_found = True
                        print("\n______________________________________\n")
                        print(f"Task:               {task[1]}")
                        print(f"Assigned to:        {task[0]}")
                        print(f"Date assigned:      {task[4]}")
                        print(f"Due date:           {task[3]}")
                        print(f"Task Complete?      {task[5]}")
                        print("Task description:")
                        print(f" {task[2]}")
                        print("\n______________________________________\n")
                        if (_del_task_file(task_to_delete)):
                            print("\nTask succesfully deleted!")
                        else:
                            print("\nTask not deleted.")
                        print("*********************************\n\n")
                        input("\nEnter any character to return "
                              "to the main menu.\n")
                        return

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        if not task_found:
            while True:
                again = input(f"Task ({task_to_delete}) not found. "
                              "Try another task? (y/n)")
                if again in ["y", "yes"]:
                    break
                elif again in ["n", "no"]:
                    return


# Helper function for non-admin menu
def _non_admin_menu():
    while True:
        # Present the menu to the user and
        # make sure that the user input is converted to lower case.
        print("MAIN MENU\n\n")
        menu = input(
            '''Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : '''
        ).lower()

        if menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")


def _admin_menu():
    while True:
        # Present the menu to the user and
        # make sure that the user input is converted to lower case.
        print("ADMIN MAIN MENU\n\n")
        menu = input(
            '''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    vc - view completed tasks
    del - delete tasks
    e - exit
    : '''
        ).lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()

        elif menu == 'vc':
            view_completed()

        elif menu == 'del':
            delete_task()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")


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

# Loop for asking for username and password
print("\n\n*********************************")
print("\nLog into your account\n\n")
current_user = _ask_user()

if current_user == "admin":
    _admin_menu()
else:
    _non_admin_menu()
