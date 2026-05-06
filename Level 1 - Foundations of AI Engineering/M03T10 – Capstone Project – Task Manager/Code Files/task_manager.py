# ===== Importing external modules =========== 
'''This is the section where you will import modules'''
from datetime import date, datetime
import os

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
            if os.path.getsize("tasks.txt") > 0: # Add new line if file contents exist
                file.write("\n")
            # Append new line with user, pass
            file.write(
                f"{assign_user}, {title_task}, {desc_task}, "
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

# Helper function for updating task to completed
def _mark_complete(chosen_task_title):
    while True:
        mark_as_complete = input("Change task as completed? (y/n) ")
        if mark_as_complete in ["y", "yes"]:
            try:
                with open("tasks.txt", "r") as file:  # Open file as read
                    lines = file.readlines()

                with open("tasks.txt", "w") as file:  # Open file as write
                    # Read line by line until task is found
                    for line in lines:
                        task = line.strip().split(",")
                        if task[1].strip() == chosen_task_title.strip():
                            # Update the line with task completed as "Yes"
                            line = (f"{task[0].strip()}, {task[1].strip()}, {task[2].strip()}, "
                                    f"{task[3].strip()}, {task[4].strip()}, Yes")
                        file.write(line)
                
                return True

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif mark_as_complete in ["n", "no"]:
            return False


# Helper function for editing username
def _edit_username(chosen_task_title):
    while True:
        new_user = input("Please enter new username to assign task. ")
        if new_user in user_pass_dict:
            try:
                with open("tasks.txt", "r") as file:  # Open file as read
                    lines = file.readlines()

                with open("tasks.txt", "w") as file:  # Open file as write
                    # Read line by line until task is found
                    for line in lines:
                        task = line.strip().split(",")
                        if task[1].strip() == chosen_task_title.strip():
                            # Update the line with new username
                            line = (f"{new_user.strip()}, {task[1].strip()}, {task[2].strip()}, "
                                    f"{task[3].strip()}, {task[4].strip()}, {task[5].strip()}")
                        file.write(line)
                return new_user

            except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            print("Invalid username. Please try again.")

# Helper function for editing due date
def _edit_due_date(chosen_task_title):
    while True:
        new_due_date = input("Please enter the new due date for the task. (YYYY-MM-DD) ")
        try:
            datetime.strptime(new_due_date, "%Y-%m-%d")
            try:
                with open("tasks.txt", "r") as file:  # Open file as read
                    lines = file.readlines()

                with open("tasks.txt", "w") as file:  # Open file as write
                    # Read line by line until task is found
                    for line in lines:
                        task = line.strip().split(",")
                        if task[1].strip() == chosen_task_title.strip():
                            # Update the line with new due date
                            line = (f"{task[0].strip()}, {task[1].strip()}, {task[2].strip()}, "
                                    f"{new_due_date}, {task[4].strip()}, {task[5].strip()}")
                        file.write(line)
                return new_due_date

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")
        


# Helper function for asking to edit username and due date, then print changes
def _edit_task(task_chosen_arr):
    while True:
        # Ask for user choice
        edit_task_input = input("\nPlease select one of the following options:\n"
                                "u - edit username of person to whom task is assigned\n"
                                "d - edit due date of the task\n"
                                "b - edit both username and due date\n"
                                "q - quit\n\n")

        # Use helper functions to edit username/due date
        if edit_task_input == 'u':
            old_user = task_chosen_arr[0]
            new_user = _edit_username(task_chosen_arr[1])
            print("\nUsername successfully edited!")
            print(f"{old_user} (old username) -> {new_user} (new username)")
            return True

        elif edit_task_input == 'd':
            old_due_date = task_chosen_arr[3]
            new_due_date = _edit_due_date(task_chosen_arr[1])
            print("\nDue date successfully edited!")
            print(f"{old_due_date} (old due date) -> {new_due_date} (new due date)")
            return True

        elif edit_task_input == 'b':
            old_user = task_chosen_arr[0]
            old_due_date = task_chosen_arr[3]
            new_user = _edit_username(task_chosen_arr[1])
            new_due_date = _edit_due_date(task_chosen_arr[1])
            print("\nUsername and due date successfully edited!")
            print(f"{old_user} (old username) -> {new_user} (new username)")
            print(f"{old_due_date} (old due date) -> {new_due_date} (new due date)")
            return True

        elif edit_task_input == 'q':
            print("\nTask unedited.\n")
            return False

        else:
            print("Invalid input.")
    

# PRACTICAL TASK - PART 3 FUNCTIONS
def reg_user():
    # Implement the following functionality
    '''This code block will add a new user to the user.txt file'''
    print("\n\n*********************************")
    print("\nREGISTER A USER\n\n")

    # Take user input, verify it does not already exist
    while True:
        new_user = input("Please enter the new username: ")
        if new_user in user_pass_dict:
            print(f"Username ({new_user}) already exists.")
        else:
            break

    print(f"Username entered: {new_user}")
    new_pass = input("Please enter the new password: ")

    # Loop for password confirmation
    while True:
        new_pass_confirm = input("Please confirm the new password: ")
        # If password is confirmed, then _update_new_user_pass()
        # to update user.txt
        if new_pass == new_pass_confirm:
            _update_new_user_pass(new_user, new_pass)
            user_pass_dict[new_user] = new_pass  # Update dictionary with new user/pass 
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

    # Loop for asking date
    while True:
        due_date_task = input("Please enter the due date of the task (YYYY-MM-DD): ")
    
        try:
            datetime.strptime(due_date_task, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")
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
        # Open tasks.txt
        with open("tasks.txt", "r") as file:
            
            # Print tasks.txt if it exists
            if os.path.getsize("tasks.txt") > 0:
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
            
            # Do not print if tasks.txt does not exist
            else:
                print("No tasks available.\n")

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
    my_tasks_arr = []  # List of current user's tasks
    try:
        # Open tasks.txt as "r"
        with open("tasks.txt", "r") as file:
            for line in file:  # Go line by line in file (task by task)
                task = line.strip().split(", ")  # Save task as list
                if current_user == task[0]:  # If the task is the current user's task
                    my_tasks_arr.append(task)  # Add to current user's tasks

                    # Print task information
                    print("\n______________________________________\n")
                    print(f"Task #{my_tasks_arr.index(task) + 1}:            {task[1]}")
                    print(f"Assigned to:        {task[0]}")
                    print(f"Date assigned:      {task[4]}")
                    print(f"Due date:           {task[3]}")
                    print(f"Task Complete?      {task[5]}")
                    print("Task description:")
                    print(f" {task[2]}")
                    print("\n______________________________________\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    if my_tasks_arr:  # If current user has tasks
        # Recursive, helper function for getting valid task number (OPTIONAL TASK)
        def get_valid_task_number():
            try:
                # Ask for user input
                choose_task_num = int(input("Please choose a task or '-1' to return to the main menu. "))

                # Base case
                if choose_task_num == -1:
                    return -1
                
                # Valid option
                elif 1 <= choose_task_num <= len(my_tasks_arr):
                    return choose_task_num
                
                # Invalid option calls function again
                else:
                    print("Invalid input. Please enter a valid task number.")
                    return get_valid_task_number()
            
            # Invalid option calls function again
            except ValueError:
                print("Invalid input. Please enter a valid task number.")
                return get_valid_task_number()

        while True:
            # Calls recursive function to get a valid task number
            choose_task_num = get_valid_task_number()

            # Base case
            if choose_task_num == -1:
                break

            task_chosen_arr = my_tasks_arr[choose_task_num - 1]  # Chosen task by user

            if task_chosen_arr[5].strip() == "Yes":  # If task is already marked as completed
                print(f"\nTask ({choose_task_num}) already completed.\n")
                break
            
            # Print selected task
            print("\nSelected task:")
            print("\n______________________________________\n")
            print(f"Task #{choose_task_num}:            {task_chosen_arr[1]}")
            print(f"Assigned to:        {task_chosen_arr[0]}")
            print(f"Date assigned:      {task_chosen_arr[4]}")
            print(f"Due date:           {task_chosen_arr[3]}")
            print(f"Task Complete?      {task_chosen_arr[5]}")
            print("Task description:")
            print(f" {task_chosen_arr[2]}")
            print("\n______________________________________\n")

            # Call _mark_complete to ask if user wants to mark task as complete
            if (_mark_complete(task_chosen_arr[1])):
                print(f"Task #{choose_task_num} marked as completed!\n")
                break

            # Call _edit_task to ask if user wants to edit username or due date
            if (_edit_task(task_chosen_arr)):
                print(f"(Task #{choose_task_num})\n")
                break

            # If user does not edit anything, brought back to selecting task

    else:
        print("\nNo tasks available.")


    print("\n*********************************\n\n")
    input("\nEnter any character to return to the main menu.\n")


def view_completed():
    '''
    This code block will read the task from task.txt file and
    print all completed tasks
    '''
    print("\n\n*********************************")
    print("\nVIEW COMPLETED TASKS\n\n")
    try:
        # Open tasks.txt
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip().split(", ")  # Check line by line (task by task)
                # Only print if task is marked as complete
                if task[5].strip() == "Yes":
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
    print("Tasks available:")
    try:
        # Open tasks.txt
        with open("tasks.txt", "r") as file:
            if os.path.getsize("tasks.txt") > 0:  # If tasks.txt exists
                # Print tasks.txt
                for line in file:
                    task = line.strip().split(", ")
                    print("\n______________________________________\n")
                    print(f"Task:               {task[1]}")
                    print(f"Assigned to:        {task[0]}")
                    print("Task description:")
                    print(f" {task[2]}")
                    print("______________________________________")
            else:
                print("No tasks available.\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    while True:
        # Ask for user input
        task_to_delete = input("\nPlease enter task title to be deleted: ")
        task_found = False  # Variable to detect if task is found

        try:
            # Open tasks.txt
            with open("tasks.txt", "r") as file:
                for line in file:  # Check line by line (task by task)
                    task = line.strip().split(", ")
                    if task_to_delete == task[1]:  # If user input matches task
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
                        # Call _del_task_file to delete task
                        if (_del_task_file(task_to_delete)):
                            print("\nTask succesfully deleted!")

                        # If _del_task_file returns false (user decided not to delete)
                        else:
                            print("\nTask not deleted.")

                        print("\n*********************************\n\n")
                        input("Enter any character to return "
                              "to the main menu.\n")
                        return

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # If user selected task was not found
        if not task_found:
            while True: # Loop to ask user to try again
                again = input(f"Task ({task_to_delete}) not found. "
                              "Try another task? (y/n)")
                if again in ["y", "yes"]:
                    break
                elif again in ["n", "no"]:
                    return


def gen_reps():
    '''
    This code block will read the tasks from task.txt file and
    generate tasks report and print.
    '''
    print("\n\n*********************************")
    print("\nGENERATE REPORTS\n\n")

    # Open and read task data
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task_arr = line.strip().split(", ")
                task_stats_dict["num_tasks"] += 1  # Count number of tasks
                user_task_dict[task_arr[0]][0] += 1  # Count number of tasks for user

                if task_arr[5].strip() == "Yes":  # Count number of completed tasks
                    task_stats_dict["completed_tasks"] += 1
                    user_task_dict[task_arr[0]][2] += 1

                else:  # Count number of uncompleted tasks
                    task_stats_dict["uncompleted_tasks"] += 1
                    user_task_dict[task_arr[0]][3] += 1
                    # Count number of overdue tasks
                    if date.today() > datetime.strptime(task_arr[3].strip(), "%Y-%m-%d").date():
                        task_stats_dict["overdue_tasks"] += 1
                        user_task_dict[task_arr[0]][4] += 1

    except Exception as e:
        print(f"An unexpected error occurred (opening tasks.txt): {e}")

    # Update user/task dictionary
    # Value of keys are [# of tasks,
    #                    % of total number of tasks assigned to user
    #                    % of completed tasks assigned to user
    #                    % of uncompleted tasks assigned to user
    #                    % of overdue tasks assigned to user]
    for user in user_task_dict:
        user_num_tasks = user_task_dict[user][0]    # # of user's tasks
        user_com_tasks = user_task_dict[user][2]    # # of user's completed tasks
        user_uncom_tasks = user_task_dict[user][3]  # # of user's uncompleted tasks
        user_over_tasks = user_task_dict[user][4]   # # of user's overdue tasks

        if user_num_tasks == 0:
            # % of total number of tasks assigned to user
            user_task_dict[user][1] = 0
            # % of completed tasks assigned to user
            user_task_dict[user][2] = 0
            # % of uncompleted tasks assigned to user
            user_task_dict[user][3] = 0
            # % of overdue tasks assigned to user
            user_task_dict[user][4] = 0
        else:
            # % of total number of tasks assigned to user
            user_task_dict[user][1] = user_num_tasks / task_stats_dict["num_tasks"] * 100
            # % of completed tasks assigned to user
            user_task_dict[user][2] = user_com_tasks / user_num_tasks * 100
            # % of uncompleted tasks assigned to user
            user_task_dict[user][3] = user_uncom_tasks / user_num_tasks * 100
            # % of overdue tasks assigned to user
            user_task_dict[user][4] = user_over_tasks / user_num_tasks * 100

    # Create Task Overview report and print
    try:
        with open("task_overview.txt", "w") as file:
            file.write(f"# of tasks:                           {task_stats_dict["num_tasks"]}\n"
                    f"# of completed tasks:                 {task_stats_dict["completed_tasks"]}\n"
                    f"# of uncompleted tasks:               {task_stats_dict['uncompleted_tasks']}\n"
                    f"# of uncompleted, overdue tasks:      {task_stats_dict['overdue_tasks']}\n"
                    f"% of tasks incomplete:               {task_stats_dict["completed_tasks"] / task_stats_dict['num_tasks'] * 100:.0f} %\n"
                    f"% of tasks overdue:                  {task_stats_dict['overdue_tasks'] / task_stats_dict['num_tasks'] * 100:.0f} %")
        print("Task Overview generated successfully.")
        
    except Exception as e:
        print(f"An unexpected error occurred (opening task_overview.txt): {e}")

    # Create User Overview report and print
    try:
        with open("user_overview.txt", "w") as file:
            for user in user_task_dict:
                file.write(f"User ({user}) Overview:\n"
                            f"# of tasks:                            {user_task_dict[user][0]}\n"
                            f"% of tasks assigned:                   {user_task_dict[user][1]:.0f} %\n"
                            f"% of completed tasks:                  {user_task_dict[user][2]:.0f} %\n"
                            f"% of uncompleted tasks:                {user_task_dict[user][3]:.0f} %\n"
                            f"% of overdue tasks:                    {user_task_dict[user][4]:.0f} %\n\n")
        print("\nUser Overview generated successfully.")


    except Exception as e:
        print(f"An unexpected error occurred (opening user_overview.txt): {e}")

    print("\n*********************************\n\n")
    
def disp_stats():
    '''
    This code block will print the stats of task overview and user overview.
    '''
    print("\n\n*********************************")
    print("\nDISPLAY STATISTICS\n\n")
    try: # If files exists
        # Print task overview
        print("Task Overview:\n")
        with open('task_overview.txt', 'r') as file:
            print(file.read())

        # Print user overviews
        print("\n\nUser Overviews:\n")
        with open('user_overview.txt', 'r') as file:
            print(file.read())
    
    # If files do not exist
    except FileNotFoundError:
        print("Reports not found. Generating reports now.\n")
        gen_reps()  # Call gen_reps() to generate reports

        # Print task overview
        print("Task Overview:\n")
        with open('task_overview.txt', 'r') as file:
            print(file.read())

        # Print user overviews
        print("\nUser Overviews:\n")
        with open('user_overview.txt', 'r') as file:
            print(file.read())
    
    print("\n*********************************\n\n")
    input("Enter any character to return to the main menu.\n")
    
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
    ds - display statistics
    gr - generate reports
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
        
        elif menu == 'ds':
            disp_stats()

        elif menu == 'gr':
            gen_reps()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")


# Create dictionary for usernames and passwords
user_pass_dict = {}

# Initialize values to be counted in reports
task_stats_dict = {
    "num_tasks": 0,
    "completed_tasks": 0,
    "uncompleted_tasks": 0,
    "overdue_tasks": 0
}

# Open user.txt and populate dictionary with contents
try:
    with open("user.txt", "r") as file:
        for line in file:
            login = line.strip().split(", ")
            user_pass_dict[login[0]] = login[1]
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Dictionary with user and tasks, keys copied from user/pass dictionary
    # Value of keys are [# of tasks assigned to user,
    #                    % of total number of tasks assigned to user
    #                    # of completed tasks assigned to user
    #                    # of uncompleted tasks assigned to user
    #                    # of overdue tasks assigned to user]
user_task_dict = {k: [0,0,0,0,0] for k in user_pass_dict}

# Loop for asking for username and password
print("\n\n*********************************")
print("\nLog into your account\n\n")
current_user = _ask_user()

if current_user == "admin":
    _admin_menu()
else:
    _non_admin_menu()
